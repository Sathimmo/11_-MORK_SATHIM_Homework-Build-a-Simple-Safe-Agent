import ollama
from harness import authorize_action, MAX_ITERATIONS
from tools import search_book, check_availability, borrow_book
from schemas import SearchBookSchema, CheckAvailabilitySchema, BorrowBookSchema

TOOL_REGISTRY = {
    "search_book": search_book,
    "check_availability": check_availability,
    "borrow_book": borrow_book
}

TOOLS_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "search_book",
            "description": "Searches for books in the library inventory by title, author, or keywords like 'unavailable', 'borrowed', 'available', or 'all'.",
            "parameters": SearchBookSchema.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Checks stock availability and copy counts for a specific book ID. Use search_book first if the ID is unknown.",
            "parameters": CheckAvailabilitySchema.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "borrow_book",
            "description": "Borrows a book from the library for a user. Requires a valid user_id, book_id, and optional quantity.",
            "parameters": BorrowBookSchema.model_json_schema()
        }
    }
]


def run_agent(user_request: str, user_role: str):
    """Core agent loop that executes silently and outputs only the final answer."""
    iterations = 0
    system_prompt = (
        "You are a helpful Library Assistant connected to a PostgreSQL database. "
        "CRITICAL EXECUTION RULES:\n"
        "1. NEVER guess or invent ID numbers. If you do not know a book ID, use 'search_book' first to find the correct ID.\n"
        "2. When the user asks about unavailable or out-of-stock books, use 'search_book' with the exact keyword 'unavailable'.\n"
        "3. When the user asks about borrowed books, checkouts, or borrowings, use 'search_book' with the exact keyword 'borrowed'.\n"
        "4. STRICT BORROWING WORKFLOW:\n"
        "   - Step 1: Call `search_book` to find the exact `book_id`.\n"
        "   - Step 2: Immediately call `borrow_book` passing ONLY `user_id`, `book_id`, and `quantity`. NEVER pass a `keyword` argument to `borrow_book`.\n"
        "5. Handle typos or vague phrasing gracefully."
    )

    conversation_history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request}
    ]

    while iterations < MAX_ITERATIONS:
        iterations += 1

        try:
            response = ollama.chat(
                model='llama3.1',
                messages=conversation_history,
                tools=TOOLS_DEFINITION
            )
        except Exception as e:
            return f"Ollama Connection Error: {str(e)}. Make sure 'ollama run llama3.1' is active."

        response_message = response['message']
        content = response_message.get('content')
        tool_calls = response_message.get('tool_calls')

        if not tool_calls:
            if not content or content.strip() == "":
                content = "I have successfully processed your request via the library database."
            # Print only the final clean answer
            print(f"\n{content}\n")
            return content

        conversation_history.append(response_message)

        for tool_call in tool_calls:
            tool_name = tool_call['function']['name']
            arguments = tool_call['function']['arguments']

            if not authorize_action(user_role, tool_name):
                error_msg = f"Permission Denied: Role '{user_role}' cannot execute tool '{tool_name}'."
                conversation_history.append({"role": "tool", "content": error_msg})
                continue

            try:
                tool_func = TOOL_REGISTRY[tool_name]
                result = tool_func(**arguments)
                conversation_history.append({"role": "tool", "content": str(result)})
            except Exception as e:
                error_result = f"Error executing tool: {str(e)}"
                conversation_history.append({"role": "tool", "content": error_result})

    return "Stopping: Too many steps taken without resolution."