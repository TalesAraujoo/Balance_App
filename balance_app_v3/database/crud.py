from mysql.connector import ProgrammingError
from database.db_connect import new_connection

# ------- transaction type -------
#CREATE
def insert_transaction_type(transaction_type):
    sql = """
        INSERT INTO transaction_type
            (type)
        VALUES
            (%s)
    """

    args = transaction_type

    with new_connection() as connection:
        
        try:
            cursor = connection.cursor()
            cursor.execute(sql, args)
            connection.commit()
        
        except ProgrammingError as e:
            return e.msg
        
#READ
def select_transaction_types():
    sql = """
        SELECT * from transaction_type
    """

    with new_connection() as connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)

            rows = cursor.fetchall()

            return rows

        except ProgrammingError as e:
            return e.msg

#UPDATE
def update_transaction_type(tmp_type, tmp_id):

    sql = """
        UPDATE transaction_type
        SET type = %s
        WHERE id = %s
    """

    args = (tmp_type , tmp_id)

    with new_connection() as connection:
        try: 
            cursor = connection.cursor()
            cursor.execute(sql, args)
            connection.commit()
        
        except ProgrammingError as e:
            return e.msg
        
#DELETE
def delete_transaction_type(tmp_type):
    sql = """
        DELETE FROM transaction_type 
        WHERE id = %s
    """

    args = (tmp_type['id'],)

    with new_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(sql, args)
            connection.commit()

        except ProgrammingError as e: 
            return e.msg
        
# ------ category ------    
def insert_category(category):
    sql = """
        INSERT INTO category
            (category)
        VALUES
            (%s)
    """

    args = category

    with new_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(sql, args)
            connection.commit()
        except ProgrammingError as e:
            return e.msg


def select_category():
    sql = """
        SELECT * FROM category
    """

    with new_connection() as connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)

            rows = cursor.fetchall()

            return rows
        except ProgrammingError as e:
            return e.msg


def update_category(tmp_item):
    sql = """
        UPDATE category
        SET category = %s
        WHERE id = %s
    """

    args = (tmp_item['id'],)


    with new_connection() as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(sql, args)
            connection.commit()
        
        except ProgrammingError as e:
            return e.msg


def delete_category(tmp_item):
    sql = """
        DELETE FROM category
        WHERE id = %s
    """

    args = (tmp_item['id'],)


    with new_connection() as connection: 
        try:
            cursor = connection.cursor()
            cursor.execute(sql, args)
            connection.commit()
        except ProgrammingError as e:
            return e.msg
