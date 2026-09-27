from agent import run_agent
from data import check_db_connection


def main():
    print("==================================================")
    print("        Database-Backed Library Assistant Agent    ")
    print("==================================================\n")

    print("Checking database connection...")
    if not check_db_connection():
        print("\n[DB FAILURE] Please check if your database container is running and credentials are correct.")
        return

    print("\nLibrary Database is online and ready!\n")

    while True:
        role_input = input("Enter your role ('customer' or 'admin', or type 'exit' to quit program): ").strip().lower()

        if role_input in ["exit", "quit"]:
            print("Exiting application. Goodbye!")
            break

        if role_input not in ["admin", "customer"]:
            print("[Error]: Invalid role. Please type 'admin', 'customer', or 'exit'.\n")
            continue

        user_role = role_input.upper()
        print(f"\n[Role Locked]: {user_role}")
        print("Type your requests below. Type 'back', 'switch', 'exit', or 'quit' to return to role selection.")

        while True:
            user_request = input("\nEnter your request: ").strip()

            if not user_request:
                continue

            if user_request.lower() in ["back", "switch", "exit", "quit"]:
                print("\nReturning to role selection...\n")
                break

            run_agent(user_request, user_role)


if __name__ == "__main__":
    main()