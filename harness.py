# Permission matrix mapping roles to permitted library tools
PERMISSIONS = {
    "customer": ["search_book", "check_availability"],
    "admin": ["search_book", "check_availability", "borrow_book"]
}

def authorize_action(role: str, tool_name: str) -> bool:
    """Verifies if a given role has permissions to execute a tool."""
    allowed_tools = PERMISSIONS.get(role.lower(), [])
    return tool_name in allowed_tools

MAX_ITERATIONS = 5