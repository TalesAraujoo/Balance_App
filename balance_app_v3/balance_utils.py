from transaction import Transaction
from database.crud import insert_transaction_type


def settings_menu():

    print('\n------ Settings ------\n')
    print('1. Transaction type')
    print('2. Category')
    print('3. Sub category')

    option = input('\nChoose an option: ')
    
    match option:
        case '1':
            transaction_type_settings()


def transaction_type_settings():
    print('\n------ Transaction type Settings ------\n')
    print('1. Add new type')
    print('2. Edit a type')
    print('3. Delete a type')
    print('4. Show existing types')
    print('5. Main menu')

    option = input('\nChoose an option: ')

    match option:
        case '1':
            add_transaction_type()         
        case '2':
            pass


def add_transaction_type():
    print('\n------ Add transaction type ------\n')
    tmp_type = input('New transaction name: ')
    tmp_args = (tmp_type,)
    insert_transaction_type(tmp_args)


def add_transaction_ui():
    transaction_type = ''
    amount = ''
    date = ''
    category = ''
    sub_category = ''

    tmp_transaction = Transaction(transaction_type, amount, date, category, sub_category)
    print(tmp_transaction)
