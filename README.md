# Database-Backed Library Assistant Agent

## 1. Project Overview
The Database-Backed Library Assistant Agent is an intelligent, local AI-powered assistant (built using Python, Ollama/Llama 3.1, and PostgreSQL) designed to interact with a library management system. It enables users and administrators to search for books by title, author, or status, check stock availability, and manage multi-copy book borrowings directly through natural language processing and structured tool execution.

## 2. Available Tools
* **`search_book`**: Searches the library inventory database for books matching a keyword. Supports searching by title, author, or special keywords such as `available`, `unavailable`, and `borrowed` (to view active checkouts).
* **`check_availability`**: Queries stock counts and available copies for a specific book ID.
* **`borrow_book`**: Records a borrowing transaction for a user and book ID (supporting multi-copy requests), automatically updates available stock, and logs active records with due dates.

## 3. Agent Loop
The agent operates on an autonomous reasoning and execution loop:
1. **Decision**: The agent receives a natural language user request and analyzes it using local Llama 3.1 via Ollama.
2. **Action**: If a tool is required, the agent calls the appropriate function (`search_book`, `check_availability`, or `borrow_book`) with validated arguments.
3. **Observation**: The tool executes against the PostgreSQL database (`library_db`), and the result is fed back into the agent's conversation history to formulate a final response.

## 4. Permission Rule
Role-based access control (RBAC) is enforced to secure database operations:
* **CUSTOMER**: Allowed to search inventory, check book availability, and borrow books for their assigned user profile. Restricted from administrative overrides or viewing unauthorized system-wide logs.
* **ADMIN**: Granted full privileges across all available tools, including managing inventory views, inspecting active borrowings across all users, and executing elevated operations.

## 5. Safety, Validation & Guardrails
* **Input Validation**: Uses Pydantic models (`schemas.py`) to strictly validate tool arguments and parameter types before execution, preventing malformed inputs.
* **Error Handling**: Database transactions are wrapped in robust try-except blocks with automated rollbacks on failure to maintain database integrity.
* **Iteration Limits**: Controlled by a strict iteration guard (`MAX_ITERATIONS`) to prevent infinite reasoning loops or excessive tool-calling cycles.

## 6. Example Run
**User Request**: 
> `borrow 2 java books` (Logged in as `ADMIN`)

**Execution Flow**:
* **Iteration 1**: 
  * *Tool Called*: `search_book(keyword='java')`
  * *Tool Result*: `[{'book_id': 4, 'title': 'Java: The Complete Reference', 'author': 'Herbert Schildt', 'available_copies': 2}]`
* **Iteration 2**: 
  * *Tool Called*: `borrow_book(user_id=2, book_id=4, quantity=2)`
  * *Tool Result*: `Success! Borrowed 2 copy/copies of 'Java: The Complete Reference'. Due date: 2026-10-11.`
* **Final Agent Output**:
  > "Successfully borrowed 2 copies of 'Java: The Complete Reference' by Herbert Schildt. Your active borrowing records have been created with a due date of 2026-10-11."# 11_-MORK_SATHIM_Homework-Build-a-Simple-Safe-Agent
