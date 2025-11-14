from mysql.connector import connect, ProgrammingError
from main import show_menu

def new_connection():
    
    parameters = dict(
        host = 'localhost',
        port = '3306',
        user = 'root',
        passwd = '123456',
        database = 'balance_app'
    )

    connection = connect(**parameters)

    try:
        yield connection
    
    except ConnectionError as e:
        print(f'Error: {e}')
    
    finally: 
        if connection and connection.is_connected():
            connection.close()


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
            print(f'Error: {e.msg}')
            input('Press ENTER to continue')
            show_menu()

        else:
            print(f'Registro {args} incluído com sucesso')
