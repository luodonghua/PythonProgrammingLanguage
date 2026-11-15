"""Assignment 2: Queries over two tables with JOIN.

The tests create this schema and fill it with data:

    authors(id INTEGER PRIMARY KEY, name TEXT NOT NULL)
    books(id INTEGER PRIMARY KEY, title TEXT NOT NULL,
          author_id INTEGER NOT NULL REFERENCES authors(id),
          year INTEGER NOT NULL)

Every function takes an open sqlite3 connection first and returns plain
Python data. Use ? placeholders for every value.
"""

import sqlite3


def books_with_authors(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    """Return (title, author_name) for every book, ordered by title."""
    # TODO: SELECT ... FROM books JOIN authors ON ... ORDER BY title.
    ...


def books_by_author(conn: sqlite3.Connection, author: str) -> list[str]:
    """Return the titles of the books written by `author`, oldest first
    (ties by title). An unknown author gives []. Pass the name as a parameter."""
    # TODO: JOIN and WHERE authors.name = ?
    ...


def book_counts(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    """Return (author_name, number_of_books) for EVERY author, including those
    with 0 books. Order by count descending, then name.
    """
    # TODO: LEFT JOIN, GROUP BY, COUNT(books.id) (not COUNT(*)).
    ...


def authors_without_books(conn: sqlite3.Connection) -> list[str]:
    """Return the names of authors who have no books, in alphabetical order."""
    # TODO: LEFT JOIN ... WHERE books.id IS NULL, or NOT EXISTS.
    ...


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.executescript(
        """
        CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT NOT NULL,
            author_id INTEGER NOT NULL REFERENCES authors(id), year INTEGER NOT NULL);
        INSERT INTO authors (name) VALUES ('Ann'), ('Bo');
        INSERT INTO books (title, author_id, year) VALUES ('Tides', 1, 2001);
        """
    )
    print(books_with_authors(db))
    print(book_counts(db))
