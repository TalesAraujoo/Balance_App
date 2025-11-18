from balance_utils import get_option, add_transaction_ui, title_generator, enter_to_continue
from balance_utils import add_transaction_type, show_existing_transaction_type, edit_transaction_type, exclude_transaction_type
from balance_utils import add_category, show_category, edit_category, exclude_category
from balance_utils import add_sub_category, show_sub_category, edit_sub_category, exclude_sub_category


def show_menu():

    print(title_generator('Main Menu'))
    print('1. Add Transaction')
    print('2. Reports')
    print('3. Test')
    print('4. Settings')
    print('5. Exit')
    
    match get_option():
        case '1': 
            add_transaction_ui()
            show_menu()
        case 2:
            pass
        case 3:
            pass
        case '4':
            settings_menu()
            show_menu()
        case '5':
            print('Exiting program...')
        case _:
            print('\nChoose a valid option.')
            enter_to_continue()


def settings_menu():

    print(title_generator('Settings Menu'))
    print('1. Transaction type')
    print('2. Category')
    print('3. Sub category')
    print('0. Main menu')

    match get_option():
        case '1':
            transaction_type_settings()
        case '2':
            categories_settings()
        case '3':
            sub_categories_settings()
        case '0': 
            show_menu()


def transaction_type_settings():
    print(title_generator('Transaction Type Settings'))
    print('1. Add new type')
    print('2. Edit a type')
    print('3. Delete a type')
    print('4. Show existing types')
    print('0. Main menu')

    match get_option():
        case '1':
            add_transaction_type()         
        case '2':
            edit_transaction_type()
        case '3':
            exclude_transaction_type()
        case '4':
            show_existing_transaction_type()
            enter_to_continue()
        case '0':
            show_menu()


def categories_settings():
    print(title_generator('Categories Settings'))
    print('1. Add category')
    print('2. Edit category')
    print('3. Delete category')
    print('4. Show existing categories')
    print('0. Main menu')

    match get_option():
        case '1':
            add_category()
        case '2':
            edit_category()
        case '3':
            exclude_category()
        case '4':
            show_category()
            enter_to_continue()
        case '0':
            show_menu()
        

def sub_categories_settings():
    print(title_generator('Sub-category settings'))
    print('1. Add sub-category')
    print('2. Edit sub-category')
    print('3. Delete sub-category')
    print('4. Show existing sub-category')
    print('0. Main menu')

    match get_option():
        case '1':
            add_sub_category()
        case '2':
            edit_sub_category()
        case '3':
            exclude_sub_category()
        case '4':
            show_sub_category()
            enter_to_continue()
        case '0':
            show_menu() 


show_menu()
