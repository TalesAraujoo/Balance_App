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
        name TEXT NOT NULL,
        color TEXT,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
        UNIQUE (name, category_id)  -- Prevents duplicated labels with the same category
    )
    """)

    query.exec("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_type TEXT,
        amount_cents INTEGER NOT NULL,
        date TEXT NOT NULL,
        category_id INTEGER,
        label_id INTEGER,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
        FOREIGN KEY (label_id) REFERENCES labels (id) ON DELETE SET NULL
    )
    """)

    # print("Tables created successfully.")


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


def get_labels():
    query = QSqlQuery("""
                    SELECT * FROM labels
                    """)
    
    labels_list = []
    while query.next():
        labels_list.append({
            "id": query.value(0),
            "name": query.value(1),
            "color": query.value(2),
            "category_id": query.value(3)
        })

    return labels_list


def insert_labels(name, color, cat_id):
    query = QSqlQuery("""
                    INSERT INTO labels (name, color, category_id)
                    VALUES (?,?,?)
                    """)
    
    query.addBindValue(name)
    query.addBindValue(color)
    query.addBindValue(cat_id)

    if not query.exec():
        print(f"Error adding new label to DB: {query.lastError().text()}")
        return False
    return True


def update_labels(name, color, label_id, cat_id):
    query = QSqlQuery("""
                    UPDATE labels
                      SET name = ?, color = ?, category_id = ?
                      WHERE id = ?
                    """)
    
    query.addBindValue(name)
    query.addBindValue(color)
    query.addBindValue(cat_id)
    query.addBindValue(label_id)

    if not query.exec():
        print(f"Error updating Label Item: {query.lastError().text()}")


def delete_labels(label_id):
    query = QSqlQuery("""
                    DELETE FROM labels
                    WHERE id = ?
                    """)

    query.addBindValue(label_id)

    if not query.exec():
        print(f"Error deleting label: {query.lastError().text()}")
        return False
    return True


def insert_transaction(trans_type, amount_cents, date, cat, lab, desc):
    query = QSqlQuery("""
                    INSERT INTO transactions 
                        (transaction_type, amount_cents, date, category_id, label_id, description)
                    VALUES
                        (?,?,?,?,?,?)
                """)
    
    query.addBindValue(trans_type)
    query.addBindValue(amount_cents)
    query.addBindValue(date)
    query.addBindValue(cat)
    query.addBindValue(lab)
    query.addBindValue(desc)

    if not query.exec():
        print(f"Error saving transaction to DB: {query.lastError().text()}")
        return False
    return True


def get_transactions():
    query = QSqlQuery("""
                    SELECT * FROM transactions
                    ORDER BY date DESC
                    """)

    transaction_list = []

    while query.next():
        transaction_list.append({
            'id': query.value(0),
            'transaction_type': query.value(1),
            'amount_cents': query.value(2),
            'date': query.value(3),
            'category_id': query.value(4),
            'label_id': query.value(5),
            'description': query.value(6)
        })
    
    return transaction_list


def delete_transaction(trans_id):
    query = QSqlQuery("""
                    DELETE from transactions
                    WHERE id = ?
                    """)
    
    query.addBindValue(trans_id)


    if not query.exec():
        print(f"Error deleting transaction: {query.lastError().text()}")
        return False
    return True


def tmp():
    query = QSqlQuery("""
                    DROP TABLE transactions
                """)


if __name__ == "__main__":
    app = QApplication([])
    if db_init():
        create_tables()
        # tmp()
       