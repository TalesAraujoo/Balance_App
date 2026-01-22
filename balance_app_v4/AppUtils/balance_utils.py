from PyQt6.QtWidgets import(
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QComboBox, QDateEdit, QMessageBox, QMenu, QDoubleSpinBox)
from Data.db_utils import (
    get_categories, insert_categories, update_categories, delete_categories,
    get_labels, insert_labels, update_labels, delete_labels, insert_transaction,
    get_transactions, delete_transaction)
from PyQt6.QtCore import  pyqtSignal, QDate, Qt, QLocale


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

        amount_label = QLabel("Amount:")
        self.amount = QDoubleSpinBox()
        self.amount.setDecimals(2)
        self.amount.setMinimum(0.00)
        self.amount.setMaximum(999999999.99)
        self.amount.setPrefix('$ ')
        self.amount.setSingleStep(1)
        self.amount.setLocale(QLocale('en_US'))
        self.amount.clear()
        date_label = QLabel("Date:")
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())

        row1.addWidget(amount_label)
        row1.addWidget(self.amount)
        row1.addWidget(date_label)
        row1.addWidget(self.date)
        layout.addLayout(row1)

        categories_label = QLabel("Category:")
        self.category = QComboBox()
        self.category.currentIndexChanged.connect(self.load_labels)
               
        labels_label = QLabel("Labels:")
        self.label = QComboBox()
      
        row2.addWidget(categories_label)
        row2.addWidget(self.category)
        row2.addWidget(labels_label)
        row2.addWidget(self.label)
        layout.addLayout(row2)


        description_label = QLabel("Description:")
        self.description = QLineEdit()
        row3.addWidget(description_label)
        row3.addWidget(self.description)
        layout.addLayout(row3)
        
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        row4.addWidget(self.save_btn)
        row4.addWidget(self.cancel_btn)
        layout.addLayout(row4)

        row5.addWidget(QLabel("Recently Added:"))
        
        self.expense_history = QTableWidget()
        self.expense_history.setColumnCount(7)
        self.expense_history.setHorizontalHeaderLabels(['Date', 'amount', 'type', 'label', 'category', 'description', 'ID'])
        self.expense_history.hideColumn(6)
        self.expense_history.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
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


    def show_recently_added(self, amount = 5):
        transactions = get_transactions()
        self.expense_history.setRowCount(0)

        row = 0
        cat_pairs = {cat['id']: cat['name'] for cat in get_categories()}
        lab_pairs = {lab['id']: lab['name'] for lab in get_labels()}
        for item in transactions:
            cat_name = cat_pairs.get(item['category_id'], '')
            lab_name = lab_pairs.get(item['label_id'], '')
            amount_value = f'{item['amount_cents'] / 100:.2f}'

            self.expense_history.insertRow(row)
            self.expense_history.setItem(row, 0, QTableWidgetItem(item["date"]))
            self.expense_history.setItem(row, 1, QTableWidgetItem('$ ' + str(amount_value)))
            self.expense_history.setItem(row, 2, QTableWidgetItem(item["transaction_type"]))
            self.expense_history.setItem(row, 3, QTableWidgetItem(lab_name))
            self.expense_history.setItem(row, 4, QTableWidgetItem(cat_name))
            if item["description"]:
                self.expense_history.setItem(row, 5, QTableWidgetItem(item["description"]))

            self.expense_history.setItem(row, 6, QTableWidgetItem(str(item['id'])))
            

            row += 1
            if row == amount:
                break
            
            print(f'{item["transaction_type"]}, {item["amount_cents"]}, {item["date"]},{item["category_id"]},{item["label_id"]},{item["description"]}')


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


class SettingsPage(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        account = QPushButton("Account")
        theme = QPushButton("Theme")
        backup_sync = QPushButton("Back up / Sync")
        self.cat_labels = QPushButton("Categories and Labels")

        layout.addWidget(account)
        layout.addWidget(theme)
        layout.addWidget(backup_sync)
        layout.addWidget(self.cat_labels)
        layout.addStretch()

        self.cat_labels.clicked.connect(lambda: self.navigate.emit("cat_labels"))


class CategoriesLabelsSettings(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("Categories"))
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
        self.layout.addWidget(QLabel("Labels"))
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

