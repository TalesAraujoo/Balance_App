import balance_utils

def show_menu():

    print('\n------ Balance App ------\n')
    print('1. Add Transaction')
    print('2. Reports')
    print('3. Test')
    print('4. Settings')
    print('5. Exit')

    option = input('\nChoose an option: ')
    
    match option:
        case '1': 
            balance_utils.add_transaction_ui()
            show_menu()
        case 2:
            pass
        case 3:
            pass
        case '4':
            balance_utils.settings_menu()
        case 5:
            pass


show_menu()
