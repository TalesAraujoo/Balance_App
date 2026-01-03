from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication
from pathlib import Path
import os


def db_init():
    db = QSqlDatabase.addDatabase("QSQLITE")

    script_dir = Path(__file__).parent.resolve()
    db_path = os.path.join(script_dir, "balance.db")
    db.setDatabaseName(db_path)

    if not db.open():
        print("Error: Could not open the database")
        print(db.lastError().text())
        return False

    print("Database connected:", db_path)

    # Enable foreign keys (IMPORTANT for SQLite)
    query = QSqlQuery()
    query.exec("PRAGMA foreign_keys = ON;")

    return True


def create_tables():
    query = QSqlQuery()

    query.exec("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        color TEXT DEFAULT '#888888',
        icon TEXT
    )
    """)

    query.exec("""
    CREATE TABLE IF NOT EXISTS labels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        color TEXT DEFAULT '#888888'
    )
    """)

    query.exec("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount INTEGER NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        category_id INTEGER,
        label_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
        FOREIGN KEY (label_id) REFERENCES labels (id) ON DELETE SET NULL
    )
    """)

    print("Tables created successfully.")


if __name__ == "__main__":
    app = QApplication([])
    if db_init():
        create_tables()