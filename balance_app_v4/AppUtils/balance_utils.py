from PyQt6.QtWidgets import(
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QComboBox, QDateEdit, QMessageBox, QMenu, QDoubleSpinBox)
from Data.db_utils import (
    get_categories, insert_categories, update_categories, delete_categories,
    get_labels, insert_labels, update_labels, delete_labels, insert_transaction,
    get_transactions, delete_transaction)
from PyQt6.QtCore import  pyqtSignal, QDate, Qt, QLocale


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        row1 = QHBoxLayout()
        

        self.btn_this_month = QPushButton('This month')
        self.btn_last_month = QPushButton('Last month')
        self.btn_last_three_months = QPushButton('Last 3 months')
        self.btn_this_month.setCheckable(True)
        self.btn_this_month.setChecked(True)
        self.btn_last_month.setCheckable(True)
        self.btn_last_three_months.setCheckable(True)
        self.btn_choice = self.btn_this_month.text()

        row1.addWidget(self.btn_this_month)
        row1.addWidget(self.btn_last_month)
        row1.addWidget(self.btn_last_three_months)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels(['Date', 'Amount', 'Type', 'Label', 'Category', 'Description', 'ID'])
        self.history_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self.show_transaction_menu)
        self.history_table.hideColumn(6)
        layout.addLayout(row1)
        layout.addWidget(self.history_table)

        self.mouse_tracked_widgets()
        self.show_transaction_history()
        self.btn_this_month.clicked.connect(self.this_month_clicked)
        self.btn_last_month.clicked.connect(self.last_month_clicked)
        self.btn_last_three_months.clicked.connect(self.last_three_months_clicked)


    def this_month_clicked(self):
        self.btn_choice = self.btn_this_month.text()
        self.show_transaction_history()
        
        self.btn_this_month.setChecked(True)
        self.btn_last_month.setChecked(False)
        self.btn_last_three_months.setChecked(False)


    def last_month_clicked(self):
        self.btn_choice = self.btn_last_month.text()
        self.show_transaction_history()
        
        self.btn_last_month.setChecked(True)
        self.btn_this_month.setChecked(False)
        self.btn_last_three_months.setChecked(False)


    def last_three_months_clicked(self):
        self.btn_choice = self.btn_last_three_months.text()
        self.show_transaction_history()
        
        self.btn_last_three_months.setChecked(True)
        self.btn_this_month.setChecked(False)
        self.btn_last_month.setChecked(False)


    def get_desc_transaction_list(self):
        transactions = get_transactions()
        tmp_trans = []
        desc_trans = []

        tmp_date = ''
        for i, item in enumerate(transactions):
            # print(item)
            if transactions:
                if not tmp_date:
                    tmp_date = QDate.fromString(item['date'], 'MM-dd-yyyy')
                    tmp_trans.append(item)
                else:
                    if tmp_date == QDate.fromString(item['date'], 'MM-dd-yyyy'):
                        tmp_trans.append(item)
                    
                    else:
                        
                        while len(tmp_trans) != 0:
                            highest_id_index = None 
                            highest = None
                            for i in range(len(tmp_trans)):
                                if not highest_id_index:
                                    highest = tmp_trans[i]['id']
                                    highest_id_index = i
                                else:
                                    if highest < tmp_trans[i]['id']:
                                        highest = tmp_trans[i]['id']
                                        highest_id_index = i
                            if tmp_trans:
                                desc_trans.append(tmp_trans.pop(highest_id_index))
                        tmp_trans = []
                        tmp_date = QDate.fromString(item['date'], 'MM-dd-yyyy')
                        tmp_trans.append(item)
        
            
        while len(tmp_trans) != 0:
            highest_id_index = 0
            highest = tmp_trans[0]['id']

            for j in range(len(tmp_trans)):
                if tmp_trans[j]['id'] > highest:
                    highest = tmp_trans[j]['id']
                    highest_id_index = j

            desc_trans.append(tmp_trans.pop(highest_id_index))

        return desc_trans
    

    def show_transaction_history(self):
        desc_trans = self.get_desc_transaction_list()
        today = QDate.currentDate()
        start_date = None
        end_date = None

        if self.btn_choice.lower() == 'this month':
            start_date = QDate(today.year(), today.month(), 1)
            end_date = start_date.addMonths(1).addDays(-1)

        elif self.btn_choice.lower() == 'last month':
            last_month = today.addMonths(-1)
            start_date = QDate(last_month.year(), last_month.month(), 1)
            end_date = start_date.addMonths(1).addDays(-1)

        elif self.btn_choice.lower() == self.btn_last_three_months.text().lower():
            month = today.addMonths(-2)
            start_date = QDate(month.year(), month.month(), 1)
            current_month = QDate(today.year(), today.month(), 1)
            end_date = current_month.addMonths(1).addDays(-1)
        

        self.history_table.setRowCount(0)    
        row = 0
        cat_pairs = {cat['id']: cat['name'] for cat in get_categories()}
        lab_pairs = {lab['id']: lab['name'] for lab in get_labels()}

        tmp_income = 0
        tmp_expense = 0
       
        for item in desc_trans:
            item_date = QDate.fromString(item['date'], 'MM-dd-yyyy')

            if start_date <= item_date and item_date <= end_date: 

                cat_name = cat_pairs.get(item['category_id'], '')
                lab_name = lab_pairs.get(item['label_id'], '')
                amount = str(f'{(item["amount_cents"] / 100):.2f}')

                self.history_table.insertRow(row)
                self.history_table.setItem(row, 0, QTableWidgetItem(item['date']))
                self.history_table.setItem(row, 1, QTableWidgetItem(amount))
                self.history_table.setItem(row, 2, QTableWidgetItem(item['transaction_type']))
                self.history_table.setItem(row, 3, QTableWidgetItem(lab_name))
                self.history_table.setItem(row, 4, QTableWidgetItem(cat_name))
                self.history_table.setItem(row, 5, QTableWidgetItem(item['description']))
                self.history_table.setItem(row, 6, QTableWidgetItem(str(item['id'])))
                row += 1

                if item['transaction_type'].lower() == 'income':
                    tmp_income += item['amount_cents']
                else:
                    tmp_expense += item['amount_cents']


        tmp_income = f'{tmp_income / 100 :.2f}'
        tmp_expense = f'{tmp_expense / 100 :.2f}'

        print(f'Inc: {tmp_income} - Exp: {tmp_expense}')


    def show_transaction_menu(self, pos):
        item = self.history_table.itemAt(pos)

        if not item:
            return
        
        row = item.row()
        trans_id = int(self.history_table.item(row,6).text())
        trans_id = int(self.history_table.item(row, 6).text())

        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        remove_action = menu.addAction("Remove")

        action = menu.exec(self.history_table.viewport().mapToGlobal(pos))


        if action == edit_action:
            pass
        elif action == remove_action:
            self.remove_transaction(trans_id)


    def mouse_tracked_widgets(self):
        self.setMouseTracking(True)
        self.btn_this_month.setMouseTracking(True)
        self.btn_last_month.setMouseTracking(True)
        self.btn_last_three_months.setMouseTracking(True)
        self.history_table.setMouseTracking(True)


class OverviewPage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        row0 = QHBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        self.btn_choice = 'this month'
        self.btn_this_month  = QPushButton("This month")
        self.btn_last_month = QPushButton("Last month")
        self.btn_last_three_months = QPushButton("Last 3 months")
        self.btn_this_month.setCheckable(True)
        self.btn_this_month.setChecked(True)
        self.btn_last_month.setCheckable(True)
        self.btn_last_three_months.setCheckable(True)

        row0.addWidget(self.btn_this_month)
        row0.addWidget(self.btn_last_month)
        row0.addWidget(self.btn_last_three_months)

        self.income_label = QLabel("Income:")
        self.expense_label = QLabel("Expense:")
        self.income = QLineEdit()
        self.expense = QLineEdit()
        self.income.setReadOnly(True)
        self.expense.setReadOnly(True)


        row1.addWidget(self.income_label)
        row1.addWidget(self.income)
        row1.addWidget(self.expense_label)
        row1.addWidget(self.expense)

        self.fuel_label = QLabel("Fuel:")
        self.fuel = QLineEdit()
        self.fuel.setReadOnly(True)
        self.supermarket_label = QLabel("Supermarket:")
        self.supermarket = QLineEdit()
        self.supermarket.setReadOnly(True)

        row2.addWidget(self.fuel_label)
        row2.addWidget(self.fuel)
        row2.addWidget(self.supermarket_label)
        row2.addWidget(self.supermarket)

        self.profit_label = QLabel("Profit:")
        self.profit = QLineEdit()
        self.profit.setReadOnly(True)

        row3.addWidget(self.profit_label)
        row3.addWidget(self.profit)

        layout.addLayout(row0)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addStretch()

        self.mouse_tracked_widgets()
        self.get_statement_data(self.btn_this_month.text())
        self.btn_this_month.clicked.connect(self.this_month_btn)
        self.btn_last_month.clicked.connect(self.last_month_btn)    
        self.btn_last_three_months.clicked.connect(self.last_three_btn)

   
    def this_month_btn(self):
        self.btn_choice = self.btn_this_month.text()
        self.get_statement_data(self.btn_choice)

        self.btn_this_month.setChecked(True)
        self.btn_last_month.setChecked(False)
        self.btn_last_three_months.setChecked(False)

    
    def last_month_btn(self):
        self.btn_choice = self.btn_last_month.text()
        self.get_statement_data(self.btn_choice)
        
        self.btn_last_month.setChecked(True)
        self.btn_this_month.setChecked(False)
        self.btn_last_three_months.setChecked(False)

    
    def last_three_btn(self):
        self.btn_choice = self.btn_last_three_months.text()
        self.get_statement_data(self.btn_choice)
        
        self.btn_last_three_months.setChecked(True)
        self.btn_this_month.setChecked(False)
        self.btn_last_month.setChecked(False)
        

    def get_statement_data(self, period):
        today = QDate.currentDate()
        transactions = get_transactions()
        
        if period.lower() == 'this month':
            first_day = QDate(today.year(), today.month(), 1)
            last_day = first_day.addMonths(1).addDays(-1)

        elif period.lower() == 'last month':
            last_month = today.addMonths(-1)
            first_day = QDate(last_month.year(), last_month.month(), 1)
            last_day = first_day.addMonths(1).addDays(-1)
                  
        elif period.lower() == 'last 3 months':
            month = today.addMonths(-2)
            first_day = QDate(month.year(), month.month(), 1)
            last_day = first_day.addMonths(3).addDays(-1)

        income = 0
        expense = 0
        fuel = 0
        supermarket = 0
        profit = 0

        labels = get_labels()
        fuel_id = None
        supermarket_id = None
        for item in labels:
            if item['name'].lower() == 'fuel':
                fuel_id = item['id']
            elif item['name'].lower() == 'supermarket':
                supermarket_id = item['id']

        
        for item in transactions:
            item_date = QDate.fromString(item['date'], 'MM-dd-yyyy')
                 
            if first_day <= item_date and item_date <= last_day:
                if item['transaction_type'].lower() == 'income':
                    income += item['amount_cents']
                elif item['transaction_type'].lower() == 'expense':
                    expense += item['amount_cents']

                    if item['label_id'] == fuel_id:
                        fuel += item['amount_cents']
                    elif item['label_id'] == supermarket_id:
                        supermarket += item['amount_cents']

        profit = income - expense
        
        amount_list = [
            self.formatted_value(income),
            self.formatted_value(expense),
            self.formatted_value(fuel),
            self.formatted_value(supermarket),
            self.formatted_value(profit)
        ]
        self.income.setText(str(amount_list[0]))
        self.expense.setText(str(amount_list[1]))
        self.fuel.setText(str(amount_list[2]))
        self.supermarket.setText(str(amount_list[3]))
        self.profit.setText(str(amount_list[4]))

      
    def formatted_value(self, value):
        return f'{(value/100):.2f}'
        

    def mouse_tracked_widgets(self):
        self.setMouseTracking(True)
        self.income_label.setMouseTracking(True)
        self.income.setMouseTracking(True)
        self.expense_label.setMouseTracking(True)
        self.expense.setMouseTracking(True)
        self.fuel_label.setMouseTracking(True)
        self.fuel.setMouseTracking(True)
        self.supermarket_label.setMouseTracking(True)
        self.supermarket.setMouseTracking(True)
        self.profit_label.setMouseTracking(True)
        self.profit.setMouseTracking(True)
        self.btn_this_month.setMouseTracking(True)
        self.btn_last_month.setMouseTracking(True)
        self.btn_last_three_months.setMouseTracking(True)


class AddTransactionPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        top_buttons = QHBoxLayout()
        self.income_btn = QPushButton("Income")
        self.expense_btn = QPushButton("Expense")
        self.income_btn.setCheckable(True)
        self.expense_btn.setCheckable(True)
        self.income_btn.setChecked(True)
        top_buttons.addWidget(self.income_btn)
        top_buttons.addWidget(self.expense_btn)
        self.transaction_type = self.get_transaction_type()

        layout.addLayout(top_buttons)
        
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()
        row6 = QHBoxLayout()

        self.amount_label = QLabel("Amount:")
        self.amount = QDoubleSpinBox()
        self.amount.setDecimals(2)
        self.amount.setMinimum(0.00)
        self.amount.setMaximum(999999999.99)
        self.amount.setPrefix('$ ')
        self.amount.setSingleStep(1)
        self.amount.setLocale(QLocale('en_US'))
        self.amount.clear()
        self.date_label = QLabel("Date:")
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())

        row1.addWidget(self.amount_label)
        row1.addWidget(self.amount)
        row1.addWidget(self.date_label)
        row1.addWidget(self.date)
        layout.addLayout(row1)

        self.category_label = QLabel("Category:")
        self.category = QComboBox()
        self.category.currentIndexChanged.connect(self.load_labels)
               
        self.labels_label = QLabel("Labels:")
        self.label = QComboBox()
      
        row2.addWidget(self.category_label)
        row2.addWidget(self.category)
        row2.addWidget(self.labels_label)
        row2.addWidget(self.label)
        layout.addLayout(row2)


        self.description_label = QLabel("Description:")
        self.description = QLineEdit()
        row3.addWidget(self.description_label)
        row3.addWidget(self.description)
        layout.addLayout(row3)
        
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        row4.addWidget(self.save_btn)
        row4.addWidget(self.cancel_btn)
        layout.addLayout(row4)

        self.recently_added_label = QLabel("Recently Added:")
        self.show_label = QLabel("Show:")
        self.show_combo_box = QComboBox()
        self.show_combo_box.addItems(['5','10','20','30'])
        self.show_combo_box.currentTextChanged.connect(self.show_recently_added)
        row5.addWidget(self.recently_added_label)
        row5.addStretch()
        row5.addWidget(self.show_label)
        row5.addWidget(self.show_combo_box)
        
        self.expense_history = QTableWidget()
        self.expense_history.setColumnCount(7)
        self.expense_history.setHorizontalHeaderLabels(['Date', 'amount', 'type', 'label', 'category', 'description', 'ID'])
        self.expense_history.hideColumn(6)
        self.expense_history.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu) # ALlows right click
        self.expense_history.customContextMenuRequested.connect(self.show_transaction_menu)
        row6.addWidget(self.expense_history)
        layout.addLayout(row5)
        layout.addLayout(row6)

        layout.addStretch()
        
        self.income_btn.clicked.connect(self.set_income_check)
        self.expense_btn.clicked.connect(self.set_expense_check)
        self.save_btn.clicked.connect(self.add_transaction)
        self.cancel_btn.clicked.connect(self.cancel_transaction)

        self.show_recently_added()
        self.mouse_tracked_widgets()


    def load_categories(self):
        cat_list = get_categories()
        for cat in cat_list:
            self.category.addItem(cat["name"], cat["id"])


    def load_labels(self):
        label_list = get_labels()
        self.label.clear()
        for labItem in label_list:
            if labItem['category_id'] == self.category.currentData():
                self.label.addItem(labItem["name"], labItem["id"])


    def set_expense_check(self):
        self.expense_btn.setChecked(True)
        self.income_btn.setChecked(False)
        self.get_transaction_type()


    def set_income_check(self):
        self.income_btn.setChecked(True)
        self.expense_btn.setChecked(False)
        self.get_transaction_type()


    def get_transaction_type(self):
        if self.income_btn.isChecked():
            self.transaction_type = 'Income'
        elif self.expense_btn.isChecked():
            self.transaction_type = 'Expense'


    def validate_transaction(self, trans_type, amnt, date, cat, lab, desc):
        if not self.amount.value():
            QMessageBox.warning(None, 'Invalid amount', 'Amount cannot be zero')
            return
        
        print(self.amount.value())
        dialog = QDialog()
        dialog.setWindowTitle("Confirm Transaction")

        layout = QVBoxLayout(dialog)
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()
        row6 = QHBoxLayout()
        row7 = QHBoxLayout()

        row1.addWidget(QLabel("Transaction Type:"))
        row1.addWidget(QLabel(trans_type))
        row2.addWidget(QLabel("Amount:"))
        row2.addWidget(QLabel(str(amnt)))
        row3.addWidget(QLabel("Date:"))
        row3.addWidget(QLabel(date))
        row4.addWidget(QLabel("Category:"))
        row4.addWidget(QLabel(cat))
        row5.addWidget(QLabel("Label:"))
        row5.addWidget(QLabel(lab))
        
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row4)
        layout.addLayout(row5)
        
        if desc:
            row6.addWidget(QLabel("Description:"))
            row6.addWidget(QLabel(desc))
            layout.addLayout(row6)
        
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        row7.addWidget(ok_btn)
        row7.addWidget(cancel_btn)
        layout.addLayout(row7)
        
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            return True
        else:
            return False


    def add_transaction(self):
        self.get_transaction_type()
        expense_type = self.transaction_type
        date = self.date.date().toString('MM-dd-yyyy')
        category = self.category.currentText()
        label = self.label.currentText()
        description = self.description.text()
        
        if not self.amount.value():
            QMessageBox.warning(None, 'Invalid amount', 'Amount cannot be zero!')
            return
        else:
            amount = self.amount.value()
            amount_cents = amount * 100


        if self.validate_transaction(expense_type, amount, date, category, label, description):
            if self.category.currentData():
                category = self.category.currentData()
            else:
                category = ""
            if self.label.currentData():
                label = self.label.currentData()
            else:
                category = ""
            
            if insert_transaction(expense_type, amount_cents, date, category, label, description):
                # self.income_btn.setChecked(True)
                # self.expense_btn.setChecked(False)
                self.amount.setValue(0.00)
                self.amount.clear()            
                # self.date.setDate(QDate.currentDate())
                # self.category.setCurrentIndex(0)
                # self.label.setCurrentIndex(0)
                self.description.clear()

                self.show_recently_added()
                
    
    def cancel_transaction(self):
        self.income_btn.setChecked(True)
        self.expense_btn.setChecked(False)
        self.amount.clear()            
        self.date.setDate(QDate.currentDate())
        self.category.setCurrentIndex(0)
        self.label.setCurrentIndex(0)
        self.description.clear()


    def get_desc_transaction_list(self):
        transactions = get_transactions()
        tmp_trans = []
        desc_trans = []

        tmp_date = ''
        for i, item in enumerate(transactions):
            
            if transactions:
                if not tmp_date:
                    tmp_date = QDate.fromString(item['date'], 'MM-dd-yyyy')
                    tmp_trans.append(item)
                else:
                    if tmp_date == QDate.fromString(item['date'], 'MM-dd-yyyy'):
                        tmp_trans.append(item)
                    
                    else:
                        
                        while len(tmp_trans) != 0:
                            highest_id_index = None 
                            highest = None
                            for i in range(len(tmp_trans)):
                                if not highest_id_index:
                                    highest = tmp_trans[i]['id']
                                    highest_id_index = i
                                else:
                                    if highest < tmp_trans[i]['id']:
                                        highest = tmp_trans[i]['id']
                                        highest_id_index = i
                            if tmp_trans:
                                desc_trans.append(tmp_trans.pop(highest_id_index))
                        tmp_trans = []
                        tmp_date = QDate.fromString(item['date'], 'MM-dd-yyyy')
                        tmp_trans.append(item)
        
            
        while len(tmp_trans) != 0:
            highest_id_index = 0
            highest = tmp_trans[0]['id']

            for j in range(len(tmp_trans)):
                if tmp_trans[j]['id'] > highest:
                    highest = tmp_trans[j]['id']
                    highest_id_index = j

            desc_trans.append(tmp_trans.pop(highest_id_index))

        return desc_trans
    

    def show_recently_added(self):
        desc_trans = self.get_desc_transaction_list()
        self.expense_history.setRowCount(0)
        show_amount = int(self.show_combo_box.currentText())

        row = 0
        cat_pairs = {cat['id']: cat['name'] for cat in get_categories()}
        lab_pairs = {lab['id']: lab['name'] for lab in get_labels()}
        
        
        for item in desc_trans:
            cat_name = cat_pairs.get(item['category_id'], '')
            lab_name = lab_pairs.get(item['label_id'], '')
            amount_value = str(f'{(item["amount_cents"] / 100) :.2f}')
            
            self.expense_history.insertRow(row)
            self.expense_history.setItem(row, 0, QTableWidgetItem(item["date"]))
            self.expense_history.setItem(row, 1, QTableWidgetItem('$ ' + amount_value))
            self.expense_history.setItem(row, 2, QTableWidgetItem(item["transaction_type"]))
            self.expense_history.setItem(row, 3, QTableWidgetItem(lab_name))
            self.expense_history.setItem(row, 4, QTableWidgetItem(cat_name))
            if item["description"]:
                self.expense_history.setItem(row, 5, QTableWidgetItem(item["description"]))

            self.expense_history.setItem(row, 6, QTableWidgetItem(str(item['id'])))
            
            row += 1
            if row == show_amount:
                break
            
        
    def show_transaction_menu(self, pos):
        item = self.expense_history.itemAt(pos)

        if not item:
            return
        
        row = item.row()
        trans_id = int(self.expense_history.item(row,6).text())
        trans_id = int(self.expense_history.item(row, 6).text())

        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        remove_action = menu.addAction("Remove")

        action = menu.exec(self.expense_history.viewport().mapToGlobal(pos))


        if action == edit_action:
            pass
        elif action == remove_action:
            self.remove_transaction(trans_id)


    def remove_transaction(self, trans_id):
        if delete_transaction(trans_id):
            self.show_recently_added()


    def mouse_tracked_widgets(self):
        self.setMouseTracking(True)
        self.income_btn.setMouseTracking(True)
        self.expense_btn.setMouseTracking(True)    
        self.amount_label.setMouseTracking(True)
        self.amount.setMouseTracking(True)
        self.date_label.setMouseTracking(True)
        self.date.setMouseTracking(True)
        self.category_label.setMouseTracking(True)
        self.category.setMouseTracking(True)
        self.labels_label.setMouseTracking(True)
        self.label.setMouseTracking(True)
        self.description.setMouseTracking(True)
        self.description_label.setMouseTracking(True)
        self.save_btn.setMouseTracking(True)
        self.cancel_btn.setMouseTracking(True)
        self.recently_added_label.setMouseTracking(True)
        self.expense_history.setMouseTracking(True) 
        self.show_label.setMouseTracking(True)
        self.show_combo_box.setMouseTracking(True)


class SettingsPage(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.account = QPushButton("Account")
        self.theme = QPushButton("Theme")
        self.backup_sync = QPushButton("Back up / Sync")
        self.cat_labels = QPushButton("Categories and Labels")

        layout.addWidget(self.account)
        layout.addWidget(self.theme)
        layout.addWidget(self.backup_sync)
        layout.addWidget(self.cat_labels)
        layout.addStretch()

        self.cat_labels.clicked.connect(lambda: self.navigate.emit("cat_labels"))

        self.mouse_tracked_widgets()
    

    def mouse_tracked_widgets(self):
        self.setMouseTracking(True)
        self.account.setMouseTracking(True)
        self.theme.setMouseTracking(True)
        self.backup_sync.setMouseTracking(True)
        self.cat_labels.setMouseTracking(True)


class CategoriesLabelsSettings(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.category_label = QLabel("Categories:")
        self.layout.addWidget(self.category_label)
        self.categories_table = QTableWidget()
        self.categories_table.setColumnCount(4)
        self.categories_table.setHorizontalHeaderLabels(['Name', 'Color', 'Icon', 'ID'])
        self.categories_table.hideColumn(3)

        self.layout.addWidget(self.categories_table)

        self.cat_btns_row = QHBoxLayout()
        self.add_category_btn = QPushButton("Add")
        self.edit_category_btn = QPushButton("Edit")
        self.remove_category_btn = QPushButton("Remove")
        self.cat_btns_row.addWidget(self.add_category_btn)
        self.cat_btns_row.addWidget(self.edit_category_btn)
        self.cat_btns_row.addWidget(self.remove_category_btn)

        self.layout.addLayout(self.cat_btns_row)
        self.show_categories()


        self.cat_pairs = [] #used to manipulate category_name in edit or remove buttons
        self.labels_label = QLabel('Labels:')
        self.layout.addWidget(self.labels_label)
        self.labels_table = QTableWidget()
        self.labels_table.setColumnCount(5)
        self.labels_table.setHorizontalHeaderLabels(["Name", "Color", "Category", "ID", "category_id"])
        self.labels_table.hideColumn(3)
        self.labels_table.hideColumn(4)

        self.layout.addWidget(self.labels_table)

        self.labels_btns_row = QHBoxLayout()
        self.add_label_btn = QPushButton("Add")
        self.edit_label_btn = QPushButton("Edit")
        self.remove_label_btn = QPushButton("Remove")
        self.labels_btns_row.addWidget(self.add_label_btn)
        self.labels_btns_row.addWidget(self.edit_label_btn)
        self.labels_btns_row.addWidget(self.remove_label_btn)

        self.layout.addLayout(self.labels_btns_row)
        self.show_labels()
        self.layout.addStretch()

        self.add_category_btn.clicked.connect(self.add_category)
        self.edit_category_btn.clicked.connect(self.edit_category)
        self.remove_category_btn.clicked.connect(self.remove_category)

        self.add_label_btn.clicked.connect(self.add_label)
        self.edit_label_btn.clicked.connect(self.edit_label)
        self.remove_label_btn.clicked.connect(self.remove_label)

        self.mouse_tracked_widgets()


    def show_categories(self):
        categories_list = get_categories()
        self.categories_table.setRowCount(0)

        row = 0

        for cat in categories_list:
            self.categories_table.insertRow(row)
            self.categories_table.setItem(row, 0, QTableWidgetItem(cat["name"]))
            self.categories_table.setItem(row, 1, QTableWidgetItem(cat["color"]))
            self.categories_table.setItem(row, 2, QTableWidgetItem(cat["icon"]))
            self.categories_table.setItem(row, 3, QTableWidgetItem(str(cat["id"])))
            row += 1
            # print(f'Category: id: {cat["id"]}, name: {cat["name"]}, color: {cat["color"]}')

    
    def add_category(self):
        dialog = QDialog()
        dialog.setWindowTitle("Add Category")
        tmp_wind = QVBoxLayout(dialog)
        
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        
        row1.addWidget(QLabel("Name:"))
        name_input = QLineEdit()
        row1.addWidget(name_input)
        tmp_wind.addLayout(row1)

        row2.addWidget(QLabel("Color:"))
        color_input = QLineEdit()
        row2.addWidget(color_input)
        tmp_wind.addLayout(row2)

        btn_ok = QPushButton("Ok")
        btn_cancel = QPushButton("Cancel")
        row3.addWidget(btn_ok)
        row3.addWidget(btn_cancel)
        tmp_wind.addLayout(row3)

        # signals 
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)

        result = dialog.exec()

        # Read values after dialog closes

        if result == QDialog.DialogCode.Accepted:
            name = name_input.text()
            color = color_input.text()
            print(f'Add Category: {name}, {color}')

            insert_categories(name, color)
            self.show_categories()
            self.show_labels()

        else:
            print("canceled")


    def edit_category(self):
        dialog = QDialog()
        dialog.setWindowTitle("Edit Category")
        tmp_wind = QVBoxLayout(dialog)

        current_row = self.categories_table.currentRow()
        
        if current_row >= 0:
            row1 = QHBoxLayout()
            row2 = QHBoxLayout()
            row3 = QHBoxLayout()
            
            row1.addWidget(QLabel("Name:"))
            name_input = QLineEdit()
            name_input.setText(self.categories_table.item(current_row, 0).text())
            row1.addWidget(name_input)
            tmp_wind.addLayout(row1)

            row2.addWidget(QLabel("Color:"))
            color_input = QLineEdit()
            color_input.setText(self.categories_table.item(current_row, 1).text())
            row2.addWidget(color_input)
            tmp_wind.addLayout(row2)

            btn_ok = QPushButton("Ok")
            btn_cancel = QPushButton("Cancel")
            row3.addWidget(btn_ok)
            row3.addWidget(btn_cancel)
            tmp_wind.addLayout(row3)

            id_item = self.categories_table.item(current_row, 3)
            cat_id = int(id_item.text())

            # signals 
            btn_ok.clicked.connect(dialog.accept)
            btn_cancel.clicked.connect(dialog.reject)

            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                name = name_input.text()
                color = color_input.text()
                
                print(f'Edit categories: {name}, {color}, {cat_id}')

                update_categories(name, color, cat_id)
                self.show_categories()
                self.show_labels()

        else:
            return
        
    
    def remove_category(self):
        dialog = QDialog()
        dialog.setWindowTitle("Delete Category")

        current_row = self.categories_table.currentRow()

        if current_row >= 0:
            layout = QVBoxLayout(dialog)

            row1 = QHBoxLayout()
            row1.addWidget(QLabel("Name:"))
            name = self.categories_table.item(current_row, 0).text()
            row1.addWidget(QLabel(name))

            row2 = QHBoxLayout()
            row2.addWidget(QLabel("Color:"))
            color = self.categories_table.item(current_row, 1).text()
            row2.addWidget(QLabel(color))

            row3 = QHBoxLayout()
            ok_btn = QPushButton("OK")
            cancel_btn = QPushButton("Cancel")
            row3.addWidget(ok_btn)
            row3.addWidget(cancel_btn)

            layout.addLayout(row1)
            layout.addLayout(row2)
            layout.addLayout(row3)

            ok_btn.clicked.connect(dialog.accept)
            cancel_btn.clicked.connect(dialog.reject)

            item_id = self.categories_table.item(current_row, 3)
            cat_id = int(item_id.text())

            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                delete_categories(cat_id)
                self.show_categories()


    def show_labels(self):
        labels_list = get_labels()
        self.labels_table.setRowCount(0)

        row = 0

        self.cat_pairs = {cat['id']: cat['name'] for cat in get_categories()}

        for item in labels_list:
            cat_name = self.cat_pairs.get(item["category_id"], '') #give cat_id otherwise gimme ''
            self.labels_table.insertRow(row)
            self.labels_table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.labels_table.setItem(row, 1, QTableWidgetItem(item["color"]))
            self.labels_table.setItem(row, 2, QTableWidgetItem(cat_name))
            self.labels_table.setItem(row, 3, QTableWidgetItem(str(item["id"])))
            self.labels_table.setItem(row, 4, QTableWidgetItem(str(item["category_id"])))
            row += 1
            # print(f"Labels: Name: {item['name']} color: {item['color']}")


    def add_label(self):
        dialog = AddEditLabels("Add Label")
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            name = dialog.name_input.text()
            color = dialog.color_input.text()
            cat_id = dialog.category_input.currentData()

            insert_labels(name, color, cat_id)
            self.show_labels()
        

    def edit_label(self):
        current_row = self.labels_table.currentRow()

        if current_row >= 0:
            name = self.labels_table.item(current_row, 0).text()
            color = self.labels_table.item(current_row, 1).text()
            cat_id = self.labels_table.item(current_row, 4).text()
            
            dialog = AddEditLabels("Edit Label", name, color, cat_id)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                name = dialog.name_input.text()
                color = dialog.color_input.text()
                label_id = self.labels_table.item(current_row, 3).text()
                cat_id = dialog.category_input.currentData()

                print(f'Ok: {name}, {color}, {label_id}, {cat_id}')
                update_labels(name, color, label_id, cat_id)
                self.show_labels()
        else:
            return


    def remove_label(self):
        current_row = self.labels_table.currentRow()
        
        if current_row != -1:
            dialog = QDialog()
            dialog.setWindowTitle("Remove Label")

            layout = QVBoxLayout(dialog)
            row1 = QHBoxLayout()
            row2 = QHBoxLayout()
            row3 = QHBoxLayout()
            row4 = QHBoxLayout()

            row1.addWidget(QLabel("Name:"))
            name_input = self.labels_table.item(current_row, 0).text()
            row1.addWidget(QLabel(name_input))    
            layout.addLayout(row1)

            row2.addWidget(QLabel("Color:"))
            color_input = self.labels_table.item(current_row, 1).text()
            row2.addWidget(QLabel(color_input))
            layout.addLayout(row2)

            row3.addWidget(QLabel("Category:"))
            cat_input = self.labels_table.item(current_row, 2).text()
            row3.addWidget(QLabel(cat_input))
            layout.addLayout(row3)

            ok_btn = QPushButton("OK")
            cancel_btn = QPushButton("Cancel")
            row4.addWidget(ok_btn)
            row4.addWidget(cancel_btn)
            layout.addLayout(row4)

            ok_btn.clicked.connect(dialog.accept)
            cancel_btn.clicked.connect(dialog.reject)
            
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                label_id = int(self.labels_table.item(current_row, 3).text())
                delete_labels(label_id)
                self.show_labels()
            else:
                return


    def mouse_tracked_widgets(self):
        self.setMouseTracking(True)
        self.category_label.setMouseTracking(True)
        self.categories_table.setMouseTracking(True)
        self.add_category_btn.setMouseTracking(True)
        self.edit_category_btn.setMouseTracking(True)
        self.remove_category_btn.setMouseTracking(True)
        self.labels_label.setMouseTracking(True)
        self.labels_table.setMouseTracking(True)
        self.add_label_btn.setMouseTracking(True)
        self.edit_label_btn.setMouseTracking(True)
        self.remove_label_btn.setMouseTracking(True)
 

# Later I must refactor add/edit categories and transform them into a class
class AddEditLabels(QDialog):
    def __init__(self, win_title, name = '', color = '', cat_id = ''):
        super().__init__()

        self.setWindowTitle(win_title)

        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()

        row1.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        self.name_input.setText(name)
        row1.addWidget(self.name_input)
        layout.addLayout(row1)

        row2.addWidget(QLabel("Color:"))
        self.color_input = QLineEdit()
        self.color_input.setText(color)
        row2.addWidget(self.color_input)
        layout.addLayout(row2)

        
        row3.addWidget(QLabel("Category: "))
        self.category_input = QComboBox()
        
        cat_list = get_categories()
        for item in cat_list:
            self.category_input.addItem(item["name"], item["id"])

        if cat_id:
            index = self.category_input.findData(int(cat_id))
            if index != -1:
                self.category_input.setCurrentIndex(index)
            
        row3.addWidget(self.category_input)
        layout.addLayout(row3)

        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        row4.addWidget(ok_btn)
        row4.addWidget(cancel_btn)
        layout.addLayout(row4)

        self.setLayout(layout)

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
