#this version was made only with a list of strings and simple functions to do 
# what we have in the simple start menu
import csv


def show_menu():
    print('------ Monthly Balance ------\n')
    print('1. Income')
    print('2. Expense')
    print('3. Report')
    print('4. Exit\n')
    option = input('Choose an option: ')
    get_option(int(option))
    print('\n')


def get_option(chosen_option):

    match chosen_option:
        case 1:
            add_income()
            show_menu()

        case 2:
            add_expense()
            show_menu()

        case 3: 
            show_report()
            show_menu()
            
        case 4:
            print('Exiting program...')
            print('Great job, keep shit updated!\n')


def create_row(trans_type, amount):

    row_data = {
        "transaction_type": trans_type,
        "amount": amount
    }

    return row_data

def add_income():
    with open('september.csv', 'a', newline='') as csvfile: 
        writer = csv.writer(csvfile)
        tmp_value = input('Income value: ')
        write_row = ['Income', tmp_value]
        writer.writerow(write_row)
        csvfile.close()
        print('\n')


def add_expense():
    with open('september.csv', 'a', newline='') as csvfile: 
        writer = csv.writer(csvfile)
        tmp_value = input('Expense value: ')
        write_row = ['Expense', tmp_value]
        writer.writerow(write_row)
        csvfile.close()
        print('\n')


def show_report():
    with open('september.csv', 'r', newline = '') as csvfile:
        csv_reader = csv.reader(csvfile)
        total_income = 0
        total_expenses = 0
        
        for row in csv_reader:
            if row[0] == 'Income':
                total_income += int(row[1])
            else:
                total_expenses += int(row[1])

        print('------ Report ------')
        print(f'Total income: {total_income:.2f}')
        print(f'Total expenses: {total_expenses:.2f}')
        print(f'Profitability: {(total_income - total_expenses):.2f}')    
        print('\n----------------------')
        input('Press any key to procced...')


show_menu()
