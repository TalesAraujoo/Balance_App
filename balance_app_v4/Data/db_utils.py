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
        color TEXT,
        icon TEXT
    )
    """)

    query.exec("""
    CREATE TABLE IF NOT EXISTS labels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        color TEXT,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
        UNIQUE (name, category_id)  -- Prevents duplicated labels with the same category
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


def get_categories():
    query = QSqlQuery("""
                    SELECT id, name, color, icon
                    FROM categories
                    """)

    categories = []

    while query.next():
        categories.append({
            "id": query.value(0),
            "name": query.value(1),
            "color": query.value(2),
            "icon": query.value(3)
        })
    
    return categories


def insert_categories(name, color):
    query = QSqlQuery("""
                    INSERT INTO categories
                        (name, color)
                    VALUES
                        (?, ?)
                    """)
    
    query.addBindValue(name)
    query.addBindValue(color)

    if not query.exec():
        print(f"Database Error: {query.lastError().text()}")
        return False
    
    return True


def update_categories(name, color, id):
    query = QSqlQuery("""
                    UPDATE categories
                    SET name = ?, color = ?
                    WHERE id = ?
                    """)
    
    query.addBindValue(name)
    query.addBindValue(color)
    query.addBindValue(id)

    if not query.exec():
        print(f'Error editing database: {query.lastError().text()}')
        return False
    
    return True


def delete_categories(cat_id):
    query = QSqlQuery("""
                    DELETE FROM categories
                    WHERE id = ?
                    """)

    query.addBindValue(cat_id)

    if not query.exec():
        print(f"Error deleting category in database: {query.lastError().text()}")
        return False
    
    return True


if __name__ == "__main__":
    app = QApplication([])
    if db_init():
        create_tables()