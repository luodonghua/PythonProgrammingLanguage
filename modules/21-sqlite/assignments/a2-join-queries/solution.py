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
    rows = conn.execute(
        """
        SELECT b.title, a.name
        FROM books b JOIN authors a ON a.id = b.author_id
        ORDER BY b.title
        """
    )
    return [(row[0], row[1]) for row in rows]


def books_by_author(conn: sqlite3.Connection, author: str) -> list[str]:
    """Return the titles of the books written by `author`, oldest first
    (ties by title). An unknown author gives []. Pass the name as a parameter."""
    rows = conn.execute(
        """
        SELECT b.title
        FROM books b JOIN authors a ON a.id = b.author_id
        WHERE a.name = ?
        ORDER BY b.year, b.title
        """,
        (author,),
    )
    return [row[0] for row in rows]


def book_counts(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    """Return (author_name, number_of_books) for EVERY author, including those
    with 0 books. Order by count descending, then name.
    """
    rows = conn.execute(
        """
        SELECT a.name, COUNT(b.id) AS n
        FROM authors a LEFT JOIN books b ON b.author_id = a.id
        GROUP BY a.id
        ORDER BY n DESC, a.name
        """
    )
    return [(row[0], row[1]) for row in rows]


def authors_without_books(conn: sqlite3.Connection) -> list[str]:
    """Return the names of authors who have no books, in alphabetical order."""
    rows = conn.execute(
        """
        SELECT a.name
        FROM authors a LEFT JOIN books b ON b.author_id = a.id
        WHERE b.id IS NULL
        ORDER BY a.name
        """
    )
    return [row[0] for row in rows]


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
