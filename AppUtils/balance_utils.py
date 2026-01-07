from PyQt6.QtWidgets import(
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QLineEdit, QComboBox, QDateEdit)
from Data.db_utils import (
    get_categories, insert_categories, update_categories, delete_categories,
    get_labels, insert_labels, update_labels, delete_labels)
from PyQt6.QtCore import  pyqtSignal, QDate


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
        
        layout.addLayout(top_buttons)
        
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()
        row6 = QHBoxLayout()

        amount_label = QLabel("Amount:")
        self.amount = QLineEdit()
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
        cat_list = get_categories()
        for cat in cat_list:
            self.category.addItem(cat["name"], cat["id"])
        
        labels_label = QLabel("Labels:")
        self.label = QComboBox()
        label_list = get_labels()
        for labItem in label_list:
            self.label.addItem(labItem["name"], labItem["id"])

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
        
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        row4.addWidget(save_btn)
        row4.addWidget(cancel_btn)
        layout.addLayout(row4)

        row5.addWidget(QLabel("Recently Added:"))
        
        expense_history = QTableWidget()
        expense_history.setColumnCount(6)
        row6.addWidget(expense_history)
        layout.addLayout(row5)
        layout.addLayout(row6)

        layout.addStretch()



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
        else:
            print('Adding Label was canceled')


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
                print("cancel editing label")

        else:
            return


    def remove_label(self):
        current_row = self.labels_table.currentRow()
        
        if current_row != -1:
            dialog = QDialog()

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
                print("remove label canceled")
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

