from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import authors, categories, books

app = FastAPI(
    title="Book Management API",
    description="An API for managing a collection of books.",
    version="1.0.0"
)
# Include routes
app.include_router(authors.router, prefix="/api/v1/authors", tags=["Authors"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])

# Static files for covers images

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Management API!"}