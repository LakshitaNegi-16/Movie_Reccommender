
import sqlite3
from pathlib import Path

# Keep the database and schema beside this Python file.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cinematch.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def connect_db():
    """Connect to the CineMatch database."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create all tables and add starter movies."""

    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with connect_db() as connection:
        connection.executescript(schema)

        sample_movies = [
            (
                1,
                "Interstellar",
                "Sci-Fi|Adventure|Drama",
                "A journey through space and time."
            ),
            (
                2,
                "Inception",
                "Sci-Fi|Action|Thriller",
                "A team enters people's dreams."
            ),
            (
                3,
                "The Notebook",
                "Romance|Drama",
                "A romantic story spanning many years."
            ),
            (
                4,
                "3 Idiots",
                "Comedy|Drama",
                "Three friends navigate college life."
            ),
            (
                5,
                "The Conjuring",
                "Horror|Mystery",
                "Paranormal investigators explore a haunting."
            ),
            (
                6,
                "Harry Potter",
                "Fantasy|Adventure",
                "A young wizard discovers a magical world."
            ),
            (
                7,
                "The Dark Knight",
                "Action|Thriller|Crime",
                "A superhero faces a dangerous criminal."
            ),
            (
                8,
                "Your Name",
                "Animation|Romance|Fantasy",
                "Two teenagers experience a mysterious connection."
            )
        ]

        connection.executemany(
            """
            INSERT OR IGNORE INTO movies
                (movie_id, title, genres, description)
            VALUES (?, ?, ?, ?)
            """,
            sample_movies
        )

    print("Database initialized successfully!")


def add_user(username):
    """Register a username in the database."""

    with connect_db() as connection:
        cursor = connection.execute(
            "INSERT OR IGNORE INTO users (username) VALUES (?)",
            (username,)
        )

        row = connection.execute(
            "SELECT user_id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    return row[0]


def get_movies():
    """Retrieve all movies from the database."""

    with connect_db() as connection:
        rows = connection.execute(
            """
            SELECT movie_id, title, genres, description
            FROM movies
            ORDER BY title
            """
        ).fetchall()

    return rows


def add_to_watchlist(user_id, movie_id):
    """Save a movie to a user's watchlist."""

    with connect_db() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO watchlist
                (user_id, movie_id, watched)
            VALUES (?, ?, 0)
            """,
            (user_id, movie_id)
        )


def rate_movie(user_id, movie_id, rating):
    """Add or update a movie rating."""

    if not 0.5 <= rating <= 5.0:
        raise ValueError("Rating must be between 0.5 and 5.0.")

    with connect_db() as connection:
        connection.execute(
            """
            INSERT INTO ratings (user_id, movie_id, rating)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, movie_id)
            DO UPDATE SET rating = excluded.rating
            """,
            (user_id, movie_id, rating)
        )


if __name__ == "__main__":
    initialize_database()

    user_id = add_user("demo_user")
    print(f"Demo user ID: {user_id}")

    print("\nMovies in CineMatch:\n")

    for movie_id, title, genres, description in get_movies():
        print(f"{movie_id}. {title}")
        print(f"   Genres: {genres}")
        print(f"   Description: {description}\n")
