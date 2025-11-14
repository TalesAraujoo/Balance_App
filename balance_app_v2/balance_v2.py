import csv, ast, calendar
from datetime import date, time, datetime, timedelta
from pathlib import Path

#This sets the csv month file to the current month as a standard...globally
today = datetime.today()
month_file = today.strftime("%B").lower() + '.csv'


def show_menu():
    print('\n------ Monthly Balance ------\n')
    print('1. Add Transaction')
    print('2. Change month')
    print('3. Reports')
    print('4. Test')
    print('5. Exit\n')
    option = input('Choose an option: ')
    get_option(int(option))


def show_main_menu():

    with open('main_menu.csv', 'r', newline='', encoding='utf-8') as csvfile:
        tmp_reader = csv.reader(csvfile)
        print('\n------ Monthly Balance ------\n')
        i = 1
        for item in tmp_reader:
            print(f'{i}. {item[0]}')
            i += 1
        print('9. Go back')
        print('0. Go Foward')
        print('')
        option = input('Choose an option: ')
        get_option(int(option))


def get_option(chosen_option):

    match chosen_option:
        case 1:
            add_transaction()
            show_menu()

        case 2:
            change_month()
            show_menu()

        case 3: 
            show_report()
            show_menu()

        case 4:
            run_test()
            show_menu()

        case 5:
            print('Exiting program...')
            print('Great job, keep shit updated!\n')


def create_month_file(month_name):
    with open(month_name, 'w', newline='', encoding='utf-8') as csvfile:
        fnames = ['transaction_id', 'transaction_type', 'amount', 'date', 'category', 'sub_category']
        writer = csv.writer(csvfile)
        writer.writerow(fnames)
        print(f'\nYou sucessfully CREATED month file to "{month_file}"')


def change_month():
    
    global month_file
    month = 1
    print('\n------ Change Month ------\n')
    for x in range(1, 13):
        fake_date = datetime(2025, x, 1)
        print(f'{x}. {fake_date.strftime("%B")}')
    
    print('')
    option = input('Choose an option: ')

    fake_date = datetime(2025, int(option), 1)
    tmp_month_file = fake_date.strftime("%B").strip().lower() + '.csv'
    month_file = tmp_month_file

    file_path = Path(month_file)

    if file_path.exists():
        print(f'\nYou sucessfully changed month file to "{month_file}"')
    else:
        create_month_file(month_file)


def get_transaction_type():
    print('\n------ Transaction type ------\n')
    print('1. Income')
    print('2. Expense')
    print('')
    print('0. Main menu\n')
    chosen_option = input('Choose your option: ')
    
    if chosen_option == '1':
        return 'Income'
    elif chosen_option == '2':
        return 'Expense'
    elif chosen_option == '0':
        show_menu()
    

def get_amount():

    print('\n------ Amount ------\n')
    tmp_amount = input('Amount: ')
    print('\n')
    return float(tmp_amount)


def get_date():
    
    print('\n------ Choose a date ------\n')
    print('1. Today')
    print('2. Different date')
    print('')
    print('0. Main Menu')
    print('')
    chosen_option = input('Choose your option: ')

    if chosen_option == '1':
        tmp_date = date.today().strftime("%d/%m/%Y")
        return tmp_date
    elif chosen_option == '2':
        print('\n------ Different day ------\n')
        date_string = input('When was it (dd-mm-yyyy)? ')
        date_format = "%d-%m-%Y"
        parsed_date = datetime.strptime(date_string, date_format).date()
        tmp_date = parsed_date.strftime("%d/%m/%Y")
        return tmp_date
    elif chosen_option == '0':
        show_menu()


def get_category(transaction_type):
    if transaction_type == 'Expense':
        file = 'expense'
    else:
        file = 'income'

    with open(f'.//{file}_database_v2.csv') as csvfile:
        fnames = ['category', 'sub_category']
        reader = csv.DictReader(csvfile, fieldnames=fnames)

        tmp_list = []
        print('\n------ Choose a category ------\n')
        count = 1
        for item in reader:
            print(f'{count}. {item["category"]}')
            tmp_list.append(item['category'])
            count += 1
        
        print('')
        print('0. Main menu')
        print('')
        
        count = 1
        option = input('Choose an option: ')
        if option == '0':
            show_menu()

        for item in tmp_list:
            if int(option) == count:
                return item
            else:
                count += 1


def get_sub_category(transaction_type, category):

    if transaction_type == 'Expense':
        file = 'expense'
    else:
        file = 'income'

    with open(f'.//{file}_database_v2.csv') as csvfile:
        fnames = ['category', 'sub_category']
        reader = csv.DictReader(csvfile, fieldnames=fnames)

        print('\n------ Choose a sub-category ------\n')
        count = 1
        for item in reader:
            if category == item['category']:

                tmp_menu_list = ast.literal_eval(item['sub_category'])
            
                for item in tmp_menu_list:
                    print(f'{count}. {item}')
                    count += 1
                
                print('')
                print('0. Main menu')

                print('')
                count = 1
                option = input('Choose an option: ')
                if option == '0':
                    show_menu()

                for item in tmp_menu_list:

                    if int(option) == count:
                        return item
                    else:
                        count += 1 
                    

def get_transaction_id():
    with open(f'.\{month_file}') as csvfile:
        fnames = ['transaction_id','transaction_type','amount','date','category','sub_category']
        reader = csv.DictReader(csvfile, fieldnames=fnames)
        
        last = 0
        for item in reader:
            if item != None:
                last = item['transaction_id']
            
        return int(last)+1 


def create_dict():
    
    trans_id = get_transaction_id()
    trans_type = get_transaction_type()
    amount = get_amount()
    date = get_date()
    category = get_category(trans_type)
    sub_category = get_sub_category(trans_type, category)

    dict_data = {
        "transaction_id": trans_id,
        "transaction_type": trans_type,
        "amount": amount,
        "date": date,
        "category": category,
        "sub_category": sub_category
    }

    return dict_data


def dict_validation(tmp_dict):

    while True:
        print('\n------ Validate the info below ------\n')
    
        print(f'Amount: R$ {(tmp_dict['amount']):.2f}')
        print(f'Transaction Type: {tmp_dict['transaction_type']}')
        print(f'Date: {tmp_dict['date']}')
        print(f'Category: {tmp_dict['category']}')
        print(f'Sub-category: {tmp_dict['sub_category']}')

        print('\nShould we save it?\n')
        print('1. Yes')
        print('2. No')
        print('')
        validator = input('Choose your option: ')
        
        if validator == '1':
            print('\n****** SUCCESSFULLY SAVED! ******')
            return tmp_dict
            break
        else:
            print('\n****** Type it again ******')
            tmp_dict = create_dict()


def add_transaction():
    with open(f'.//{month_file}', 'a', newline='') as csvfile: 
               
        tmp_dict = create_dict()
        final_dict = dict_validation(tmp_dict)
        tmp_fieldnames = ['transaction_id', 'transaction_type', 'amount', 'date', 'category', 'sub_category']
        writer = csv.DictWriter(csvfile, fieldnames= tmp_fieldnames)
        writer.writerow(final_dict)


def show_report():

    print('\n------ Report ------\n')
    print('1. Simple report')
    print('2. Detailed report')
    print('3. Report per specific periods\n')

    option = input('Choose your option: ')

    if option == '1':
        show_simple_report()
    elif option == '2':
        show_detailed_report()
    elif option == '3':
        show_per_period_report()


def show_simple_report():
    with open(f'.\{month_file}', 'r', newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        
        total_income = 0
        total_expenses = 0
        
        for row in reader:
            if row['transaction_type'] == 'Income':
                total_income += float(row['amount'])
            elif row['transaction_type'] == 'Expense':
                total_expenses += float(row['amount'])

        print('\n------ Report ------\n')
        print(f'Total income: {total_income:.2f}')
        print(f'Total expenses: {total_expenses:.2f}')
        print('--------------------')
        print(f'Profitability: {(total_income - total_expenses):.2f}')
        print('')  
        input('Press ENTER to procced...')


def show_detailed_report():
    with open(f'.\{month_file}') as csvfile:
        reader = csv.DictReader(csvfile)

        total_apps = 0
        total_uber = 0
        total_99 = 0
        total_indrive = 0
        total_concerts = 0
        total_market = 0
        total_gas = 0
        total_utilities = 0
        total_fixed_expenses = 0
        total_food_groceries = 0
        total_entertainment = 0
       
        for item in reader:
            if item['transaction_type'] == 'Income':
                
                if item['sub_category'] == 'Uber':
                    total_uber += float(item['amount'])
                elif item['sub_category'] == '99':
                    total_99 += float(item['amount'])
                elif item['sub_category'] == 'inDrive':
                    total_indrive += float(item['amount'])

                if item['category'] == 'Shows':
                    total_concerts += float(item['amount']) 

            else:
                if item['category'] == 'Food and Groceries':
                    total_food_groceries += float(item['amount'])
                    if item['sub_category'] == 'Supermarket':
                        total_market += float(item['amount'])
                elif item['category'] == 'Fixed Expenses':
                    total_fixed_expenses += float(item['amount'])
                    if item['sub_category'] == 'Gas':
                        total_gas += float(item['amount'])
                elif item['category'] == 'Utility':
                    total_utilities += float(item['amount'])
                elif item['category'] == 'Entertainment':
                    total_entertainment += float(item['amount'])

        total_apps = total_uber + total_99 + total_indrive

        print('\n------ INCOME ------\n')
        print(f'          TOTAL APPs: R$ {total_apps:.2f}')
        print(f'                Uber: R$ {total_uber:.2f}')
        print(f'                  99: R$ {total_99:.2f}')
        print(f'             inDrive: R$ {total_indrive:.2f}')
        print('')
        print(f'               Shows: R$ {total_concerts:.2f}')
        print('')
        print(f'        TOTAL INCOME: R$ {(total_apps + total_concerts):.2f}')
        print('\n------ EXPENSES ------\n')
        print(f'           Utilities: R$ {total_utilities:.2f}')
        print(f'- Food and Groceries: R$ {total_food_groceries:.2f}')
        print(f'         Supermarket: R$ {total_market:.2f}')
        print(f'      Fixed Expenses: R$ {total_fixed_expenses:.2f}')
        print(f'                 Gas: R$ {total_gas:.2f}')
        print(f'       Entertainment: R$ {total_entertainment:.2f}')
        print('')
        print(f'      TOTAL EXPENSES: R$ {(total_utilities + total_fixed_expenses + total_entertainment + total_food_groceries):.2f}')
        print('-------------------')
        print(f'     CURRENT BALANCE: R$ {((total_apps + total_concerts) - (total_utilities + total_food_groceries + total_entertainment + total_fixed_expenses)):.2f}')
        print('')
        input('Press ENTER to procced...')


def show_per_period_report():
    print('\n------ Choose a period ------\n')
    print('1. Weekly report')
    print('2. This month')
    print('3. This year')
    print('4. Specific date')
    print('')

    option = input('Choose an option: ')

    if option == '1':
        get_weekly_report()
    elif option == '2':
        get_monthly_report()
    elif option == '3':
        get_year_report()
    elif option == '4':
        get_specific_date_report()


def get_weekly_report():
    
    with open(f'.\{month_file}') as csvfile:
        reader = csv.DictReader(csvfile)


        #this section gets an ordered list
        tmp_ordered_dictlist = []
        date_format = '%d/%m/%Y'
        last_highest = 0

        for item in reader:
            parsed_item = datetime.strptime(item['date'], date_format).date()
            
            if not tmp_ordered_dictlist:
                tmp_ordered_dictlist.append(item)
            
            else:
                for item_list in tmp_ordered_dictlist:
                    parsed_item_list = datetime.strptime(item_list['date'], date_format ).date()

                    if parsed_item == parsed_item_list:
                        last_highest = tmp_ordered_dictlist.index(item_list)
                    elif parsed_item > parsed_item_list:
                        last_highest = tmp_ordered_dictlist.index(item_list) + 1
                    
                
                if last_highest > len(tmp_ordered_dictlist) - 1:
                    tmp_ordered_dictlist.append(item)
                else:
                    tmp_ordered_dictlist.insert(last_highest, item)
                
                last_highest = 0
            
        
        #this section gets info based on the week from monday to sunday
        month = datetime.strptime('01' +  '/' + month_file.strip('.csv') + '/' + '2025', '%d/%B/%Y').date() 
        print(month)
        print(type(month))
        week_count = 1
        first_monthday = datetime.strptime(('01/' + str(month.month) + '/' + str(month.year)), date_format).date()
        _, last_monthday = calendar.monthrange(month.year, month.month)
        tmp_weekday = first_monthday.weekday()
        print(f'\n----------- {month.strftime("%B")} ------------\n')
        
        total_income = 0
        total_expenses = 0 
        total_gas = 0
        total_market = 0
        final_income = 0
        final_expense = 0 
        final_gas = 0
        final_market = 0

        for day in range(1, last_monthday+1):
            
            if day > last_monthday:
                break
            else:
                current_day = datetime.strptime((str(day) + '/' + str(month.month) + '/' + str(month.year)), date_format).date()
                tomorrow = current_day + timedelta(days=1)


            for item_list in tmp_ordered_dictlist:
                
                parsed_item_list = datetime.strptime(item_list['date'], date_format).date()
                if parsed_item_list == current_day:

                    if item_list['transaction_type'] == 'Income':
                        total_income += float(item_list['amount'])
                        final_income += float(item_list['amount'])
                   
                    elif item_list['transaction_type'] == 'Expense':
                        total_expenses += float(item_list['amount'])
                        final_expense += float(item_list['amount'])

                        if item_list['sub_category'] == 'Gas':
                            total_gas += float(item_list['amount'])
                            final_gas += float(item_list['amount'])
                        elif item_list['sub_category'] == 'Supermarket':
                            total_market += float(item_list['amount'])
                            final_market += float(item_list['amount'])
                
                elif parsed_item_list > current_day:
                    break

            if current_day.weekday() == 6:
                end_week = current_day.strftime(date_format)
                start_week = (current_day - timedelta(days=6))
                
                
                if start_week < first_monthday:
                    start_week = first_monthday
                
                print(f'------------ Week {week_count} ------------')
                print(f'--- {start_week.strftime(date_format)} to {end_week} ---\n')
                print(f'Total income:      R$ {total_income:.2f}')
                print(f'Total expenses:    R$ {total_expenses:.2f}')
                print(f'Total gas:         R$ {total_gas:.2f}')
                print(f'Total Supermarket: R$ {total_market:.2f}')
                print(f'--------------------------------')
                print(f'Profitability:     R$ {(total_income - total_expenses):.2f}')
                print('')
                
                week_count += 1
                total_income = 0
                total_expenses = 0 
                total_gas = 0
                total_market = 0

            elif tomorrow.day == 1:    
                start_week = current_day - timedelta(days=current_day.weekday())
                print(f'------------ Week {week_count} ------------')
                print(f'--- {start_week.strftime(date_format)} to {current_day.strftime(date_format)} ---\n')
                print(f'Total income:      R$ {total_income:.2f}')
                print(f'Total expenses:    R$ {total_expenses:.2f}')
                print(f'Total gas:         R$ {total_gas:.2f}')
                print(f'Total Supermarket: R$ {total_market:.2f}')
                print(f'--------------------------------')
                print(f'Profitability:     R$ {(total_income - total_expenses):.2f}')
                print('\n')
                

        print(f"{month.strftime("%B")}'s income:        R$ {final_income:.2f}")
        print(f"{month.strftime("%B")}'s expenses:      R$ {final_expense:.2f} ")
        print(f"{month.strftime("%B")}'s Gas:           R$ {final_gas:.2f}")
        print(f"{month.strftime("%B")}'s Supermarket:   R$ {final_market:.2f}")
        print(f"{month.strftime("%B")}'s Profitability: R$ {(final_income - final_expense):.2f}")
        print('')

        input('Press ENTER to continue...')


def get_monthly_report():
    today = date.today()
    start_of_month = today - timedelta(days = today.day - 1)
    
    with open(f'.\{month_file}') as csvfile:
        reader = csv.DictReader(csvfile)

        total_income = 0
        total_expenses = 0
        total_gas = 0
        total_market = 0 
        
        for row in reader:
            date_format = '%d/%m/%Y'
            parsed_row_date = datetime.strptime(row['date'], date_format).date()

            if parsed_row_date >= start_of_month:

                if row['transaction_type'] == 'Income':
                    total_income += float(row['amount'])
                else:
                    total_expenses += float(row['amount'])
                    if row['sub_category'] == 'Gas':
                        total_gas += float(row['amount'])
                    elif row['sub_category'] == 'Supermarket':
                        total_market += float(row['amount'])

        print('\n------ Monthly Report ------\n')
        print(f'{start_of_month.strftime('%d/%m/%y')} - {today.strftime('%d/%m/%y')}')
        print('')
        print(f'  Total income: R$ {total_income:.2f}')
        print(f'Total Expenses: R$ {total_expenses:.2f}')
        print(f'           Gas: R$ {total_gas:.2f}')
        print(f'   Supermarket: R$ {total_market:.2f}')
        print('------------------------')
        print(f'Current Balance: R$ {(total_income - total_expenses):.2f}')
        print('')
        input('Press ENTER to procced...')


def get_year_report():
    today = date.today()

    total_income = 0
    total_expenses = 0
    total_gas = 0
    total_market = 0
    
    for x in range(1, 13):
        fake_date = datetime(2025, x, 1)
        tmp_month_file = fake_date.strftime("%B").lower() + '.csv'
        file_path = Path(f'{tmp_month_file}')
    
        if file_path.exists():
            with open(f'./{tmp_month_file}') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    if row['transaction_type'] == 'Income':
                        total_income += float(row['amount'])
                    
                    elif row['transaction_type'] == 'Expense':
                        total_expenses += float(row['amount'])
                    
                        if row['sub_category'] == 'Gas':
                            total_gas += float(row['amount'])
                        elif row['sub_category'] == 'Supermarket':
                            total_market += float(row['amount'])

    print(f'\n------ Report of YEAR {today.strftime("%Y")} ------\n')
    print(f'  Total income: R$ {total_income:.2f}')
    print(f'Total expenses: R$ {total_expenses:.2f}')
    print(f'     total gas: R$ {total_gas:.2f}')
    print(f'  total market: R$ {total_market:.2f}')
    print('------------------------')
    print(f'Profitability:  R$ {(total_income - total_expenses):.2f}')
    input('Press ENTER to procced...')


def get_specific_date_report():

    print('\n------ Specific date Reports ------\n')
    print('Tip: Type the date you want or leave it blank to get the most recent or latest date.\n')
    start_date = input('Start date (dd-mm-yyyy): ')
    end_date = input('End date (dd-mm-yyyy): ')

    if start_date == '' and end_date == '':
        start_date = datetime(2025, 1, 1)
        end_date = datetime.today()

        specific_date_calc(start_date, end_date)
    
    elif end_date == '':
        tmp_start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.today()

        specific_date_calc(tmp_start_date, end_date)
    
    elif start_date == '':
        start_date = datetime(2025, 1, 1)
        end_date = datetime.strptime(end_date, "%d-%m-%Y")

        specific_date_calc(start_date, end_date)
    
    else:
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")

        specific_date_calc(start_date, end_date)


def specific_date_calc(start_date, end_date):

    total_income = 0
    total_expenses = 0
    total_gas = 0
    total_market = 0
    
    for x in range(start_date.month, end_date.month + 1):

        fake_date = datetime(2025, x, 1)
        tmp_month_file = fake_date.strftime("%B").lower() + '.csv'
        file_path = Path(f'{tmp_month_file}')

        if file_path.exists():

            with open(f'./{tmp_month_file}') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    tmp_parsed_date = datetime.strptime(row['date'], "%d/%m/%Y")
                    if tmp_parsed_date >= start_date and tmp_parsed_date <= end_date:
                    
                        if row['transaction_type'] == 'Income':
                            total_income += float(row['amount'])
                        elif row['transaction_type'] == 'Expense':
                            total_expenses += float(row['amount'])
                            if row['sub_category'] == 'Gas':
                                total_gas += float(row['amount'])
                            elif row['sub_category'] == 'Supermarket':
                                total_market += float(row['amount'])
    
    print(f'\n------ {start_date.strftime("%d-%m-%y")} - {end_date.strftime("%d-%m-%y")} ------\n')
    print(f'  Total income: R$ {total_income:.2f}')
    print(f'Total expenses: R$ {total_expenses:.2f}')
    print(f'     total gas: R$ {total_gas:.2f}')
    print(f'  total market: R$ {total_market:.2f}')
    print('------------------------')
    print(f'Profitability:  R$ {(total_income - total_expenses):.2f}') 
    input('Press ENTER to procced...') 


def run_test():
    show_main_menu()


show_menu()