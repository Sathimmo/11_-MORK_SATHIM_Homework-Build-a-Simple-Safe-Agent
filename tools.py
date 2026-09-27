from data import get_db_connection
from datetime import datetime, timedelta


def search_book(keyword: str):
    """Searches the database for books by keyword, author, availability status, or active borrowings."""
    conn = get_db_connection()
    if not conn:
        return "[Database Error]: Could not connect to PostgreSQL."

    try:
        with conn.cursor() as cursor:
            kw_lower = keyword.lower().strip()

            if kw_lower in ["books", "all", "library", "list", ""]:
                query = "SELECT book_id, title, author, isbn, total_copies, available_copies FROM books;"
                cursor.execute(query)
            elif kw_lower in ["unavailable", "out of stock", "zero"]:
                query = "SELECT book_id, title, author, isbn, total_copies, available_copies FROM books WHERE available_copies = 0;"
                cursor.execute(query)
            elif kw_lower in ["borrowed", "checked out", "active borrowings", "borrowing"]:
                query = """
                        SELECT br.borrow_id, \
                               b.book_id, \
                               b.title, \
                               b.author, \
                               u.username, \
                               br.borrow_date, \
                               br.due_date, \
                               br.status
                        FROM borrowings br
                                 JOIN books b ON br.book_id = b.book_id
                                 JOIN users u ON br.user_id = u.user_id
                        WHERE br.status = 'ACTIVE'; \
                        """
                cursor.execute(query)
            elif kw_lower in ["available", "in stock"]:
                query = "SELECT book_id, title, author, isbn, total_copies, available_copies FROM books WHERE available_copies > 0;"
                cursor.execute(query)
            else:
                query = """
                        SELECT book_id, title, author, isbn, total_copies, available_copies
                        FROM books
                        WHERE title ILIKE %s \
                           OR author ILIKE %s; \
                        """
                search_term = f"%{keyword}%"
                cursor.execute(query, (search_term, search_term))

            results = cursor.fetchall()
            if results:
                return [dict(row) for row in results]
            return f"[Database Result]: No records found matching '{keyword}'."
    except Exception as e:
        return f"[Database Query Error]: {str(e)}"
    finally:
        conn.close()


def check_availability(book_id: int):
    """Checks the stock and available copy count for a specific book ID."""
    conn = get_db_connection()
    if not conn:
        return "[Database Error]: Could not connect to PostgreSQL."

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT book_id, title, author, available_copies, total_copies FROM books WHERE book_id = %s;",
                (book_id,))
            book = cursor.fetchone()
            if not book:
                return f"[Database Result]: Book ID #{book_id} does not exist in the library inventory. Use 'search_book' first to find valid IDs."
            return dict(book)
    except Exception as e:
        return f"[Database Query Error]: {str(e)}"
    finally:
        conn.close()


def borrow_book(user_id: int, book_id: int, quantity: int = 1):
    """Records book borrowing transactions, decreasing available copies."""
    conn = get_db_connection()
    if not conn:
        return "[Database Error]: Could not connect to PostgreSQL."

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT title, available_copies FROM books WHERE book_id = %s;", (book_id,))
            book = cursor.fetchone()
            if not book:
                return f"[Database Result]: Book ID #{book_id} not found."

            if book['available_copies'] < quantity:
                return f"[Database Result]: Sorry, only {book['available_copies']} copies of '{book['title']}' are available (requested {quantity})."


            cursor.execute("UPDATE books SET available_copies = available_copies - %s WHERE book_id = %s;",
                           (quantity, book_id,))

            due_date = datetime.now() + timedelta(days=14)
            borrow_ids = []

            for _ in range(quantity):
                cursor.execute(
                    "INSERT INTO borrowings (user_id, book_id, due_date, status) VALUES (%s, %s, %s, 'ACTIVE') RETURNING borrow_id;",
                    (user_id, book_id, due_date)
                )
                borrow_ids.append(cursor.fetchone()['borrow_id'])

            conn.commit()

            return f"Success! Borrowed {quantity} copy/copies of '{book['title']}'. Record IDs: {borrow_ids}. Due date: {due_date.strftime('%Y-%m-%d')}."
    except Exception as e:
        conn.rollback()
        return f"[Database Transaction Error]: {str(e)}"
    finally:
        conn.close()