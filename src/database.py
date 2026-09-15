import sqlite3
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database location
DATABASE = BASE_DIR / "database" / "parksby.db"


def get_db_connection():
    """Create and return a connection to the Parksby database."""
    connection = sqlite3.connect(DATABASE)

    # Return database rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
