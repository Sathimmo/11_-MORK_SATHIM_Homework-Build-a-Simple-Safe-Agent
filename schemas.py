from pydantic import BaseModel, Field

class SearchBookSchema(BaseModel):
    keyword: str = Field(description="Keyword to search books by title, author, or availability status (e.g. 'unavailable', 'borrowed').")

class CheckAvailabilitySchema(BaseModel):
    book_id: int = Field(description="The unique numeric ID of the book to check.")

class BorrowBookSchema(BaseModel):
    user_id: int = Field(description="The ID of the user borrowing the book.")
    book_id: int = Field(description="The ID of the book being borrowed.")
    quantity: int = Field(default=1, description="The number of copies to borrow (default is 1).")