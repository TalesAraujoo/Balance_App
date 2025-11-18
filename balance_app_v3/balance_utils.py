def title_generator(title):
    return f'\n------ {title} ------\n'


def enter_to_continue():
    input('\nPress ENTER to continue...')


def get_option():
    option = input('\nChoose an option: ')
    return option


def add_transaction_type():
    from database.crud import insert_transaction_type
    print(title_generator('Add Transacion Type'))
    tmp_type = input('New transaction name: ')

    print('')
    print(f'Item to create: {tmp_type}')
    confirm = input('Is this correct (y/n)? ')

    if confirm == 'y':
        tmp_args = (tmp_type,)
        insert_transaction_type(tmp_args)
    elif confirm == '':
        return
    else:
        add_transaction_type()


def show_existing_transaction_type():
    from database.crud import select_transaction_types
    tmp_types_list = select_transaction_types()
    
    print(title_generator('Existing types'))
    for i, tmp in enumerate(tmp_types_list, start = 1):
        print(f'{i}. {tmp['type']}')
    
#sends 'strings' of parameters to CRUD
def edit_transaction_type():
    from database.crud import select_transaction_types, update_transaction_type
    tmp_types_list = select_transaction_types()

    print(title_generator('Existing Types'))
    for i, tmp in enumerate(tmp_types_list, start = 1):
        print(f'{i}. {tmp['type']}')

    print('')
    option = input('Type which one you want to edit: ')
    tmp_new_type = input("Type the new type's name: ")

    print('')
    print(f'You have selected: {option}. {tmp_new_type}')
    choice_option = input('Is this correct(y/n)? ')
    tmp_id = tmp_types_list[int(option) - 1]['id']

    if choice_option == 'y':
        update_transaction_type(tmp_new_type, tmp_id)
    else: 
        edit_transaction_type()

# sends the 'dictionary' [id, type] to CRUD
def exclude_transaction_type():
    from database.crud import delete_transaction_type, select_transaction_types
    tmp_type_list = select_transaction_types()

    print(title_generator('Delete type'))
    for i, tmp in enumerate(tmp_type_list, start = 1):
        print(f'{i}. {tmp['type']}')
    
    print('')
    option = input('Which one do you want to DELETE? ')

    print('')
    print(f'You have selected: {tmp_type_list[int(option)-1]['type']}')
    decision = input('Are you sure(y/n)? ')

    if decision == 'y':
        delete_transaction_type(tmp_type_list[int(option)-1])
    else:
        exclude_transaction_type()


def add_category():
    from database.crud import insert_category
    print(title_generator('Add new category'))
    tmp_category = input("Category: ")
    
    print('')
    print(f'Item to create: {tmp_category}')
    confirm = input('Is this correct (y/n)? ')

    if confirm == 'y':
        tmp_args = (tmp_category,)
        insert_category(tmp_args)
    elif confirm == '':
        return
    else:
        add_category()


def show_category():
    from database.crud import select_category
    print(title_generator('Show categories'))

    tmp_list = select_category()

    if tmp_list:
        for i, tmp in enumerate(tmp_list, start = 1):
            print(f'{i}. {tmp['category']}')
    else:
        print('No data available') 


def edit_category():
    from database.crud import update_category, select_category

    print(title_generator('Edit category'))
    tmp_list = select_category()

    if tmp_list:
        for i, tmp in enumerate(tmp_list, start = 1):
            print(f'{i}. {tmp['category']}')
        
        option = input('\nWhat category: ')
        int(option)
        tmp_category = input('New category: ')

        print('')
        confirm = input(f'Item to edit: {tmp_category}')
        print('Is this correct (y/n)? ')

        if confirm == 'y':
            update_category(tmp_list[option-1], tmp_category)
        elif confirm == '':
            return
        else:
            edit_category()
 
    else:
        print('No data available')


def exclude_category():
    from database.crud import delete_category, select_category
    
    print(title_generator('Delete category'))

    tmp_list = select_category()

    if tmp_list:
        for i, tmp in enumerate(tmp_list, start = 1):
            print(f'{i}. {tmp['category']}')

        print('')    
        option = input('Which one do you want to delete? ')
        tmp_index = int(option) - 1
        print(f'You have selected: {option}. {tmp_list[tmp_index]['category']}')
        confirm = input('Is this correct (y/n)? ')

        if confirm == 'y':
            print('test')
            delete_category(tmp_list[tmp_index])
        elif confirm == '':
            return
        else:
            exclude_category()


def add_sub_category():
    from database.crud import insert_sub_category
    print(title_generator('Add Sub-category'))
    tmp_sub_category = input('Sub-category: ')

    print('')
    print(f'Item to create: {tmp_sub_category}')
    confirm = input('Is this correct (y/n)? ')

    if confirm == 'y':
        tmp_args = (tmp_sub_category,)
        insert_sub_category(tmp_args)
    elif confirm == '':
        return
    else:
        add_sub_category()


def show_sub_category():
    from database.crud import select_sub_category
    print(title_generator('Show sub-categories'))

    tmp_list = select_sub_category()

    if tmp_list:
        for i, tmp in enumerate(tmp_list, start = 1):
            print(f'{i}. {tmp['sub_category']}')

    else:
        print('No data available')


def edit_sub_category():
    from database.crud import update_sub_category, select_sub_category
    print(title_generator('Edit sub-category'))

    tmp_list = select_sub_category()

    if tmp_list:
        for i, tmp in enumerate(tmp_list, start = 1):
            print(f'{i}. {tmp['sub_category']}')

        print('')
        option = input('Which one do you want to edit: ')
        tmp_sub_category = input('New sub-category: ')
        tmp_index = int(option) - 1

        print('')
        print(f'Item to edit: {option}. {tmp_list[tmp_index]['sub_category']}')
        print(f'New item: {tmp_sub_category}')
        confirm = input('Is this correct (y/n)? ')

        if confirm == 'y':
            update_sub_category(tmp_list[tmp_index], tmp_sub_category)
        elif confirm == '':
            return
        else:
            edit_sub_category()

    else:
        print('No data available')


def exclude_sub_category():
    from database.crud import delete_sub_category, select_sub_category
    print(title_generator('Delete Sub-category'))

    tmp_dict = select_sub_category()

    if tmp_dict:
        for i,tmp in enumerate(tmp_dict, start = 1):
            print(f'{i}. {tmp['sub_category']}')

        print('')
        option = input('Which one do you want to delete? ')
        tmp_index = int(option) - 1
        
        print('')
        print(f'You have selected: {option}. {tmp_dict[tmp_index]['sub_category']} ')
        confirm = input('Is this correct (y/n)? ')

        if confirm == 'y':
            delete_sub_category(tmp_dict[tmp_index])
        elif confirm == '':
            return
        else:
            exclude_sub_category()
    
    else:
        print('No data available')


def add_transaction_ui():
    from transaction import Transaction
    transaction_type = ''
    amount = ''
    date = ''
    category = ''
    sub_category = ''

    tmp_transaction = Transaction(transaction_type, amount, date, category, sub_category)
    print(tmp_transaction)
