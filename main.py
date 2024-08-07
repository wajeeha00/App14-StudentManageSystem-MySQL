from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, 
    QVBoxLayout, QLineEdit, QComboBox, QPushButton, QToolBar, QStatusBar, 
    QMessageBox, QLabel, QGridLayout
)
import sys
import sqlite3

class DatabaseConnection:
    def __init__(self,database_file = 'database.db'):
        self.database_file = database_file
    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        search_action = QAction("Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar_action_add = QAction(QIcon("icons/add.png"), "Add Student", self)
        toolbar_action_add.triggered.connect(self.insert)
        toolbar.addAction(toolbar_action_add)

        toolbar_action_search = QAction(QIcon("icons/search.png"), "Search", self)
        toolbar_action_search.triggered.connect(self.search)
        toolbar.addAction(toolbar_action_search)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)

        children = self.statusbar.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog(self)
        dialog.exec()

    def edit(self):
        dialog = EditDialog(self)
        dialog.exec()

    def load_data(self):
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog(self)
        dialog.exec()

    def search(self):
        dialog = SearchDialog(self)
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('About')
        content = """ 
        This app was created by Wajeeha Aftab by following the tutorial at Udemy.
        """
        self.setText(content)


class DeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Delete Student Data')

        layout = QGridLayout()
        confirmation = QLabel('Are you sure you want to delete this record?')
        yes = QPushButton('YES')
        no = QPushButton('NO')

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.close)

    def delete_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (main_window.table.item(main_window.table.currentRow(), 0).text(),))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()

        confirmation = QMessageBox()
        confirmation.setText('Record deleted successfully')
        confirmation.exec()


class EditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Update Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        course_name = main_window.table.item(index, 2).text()
        mobile = main_window.table.item(index, 3).text()

        self.student_name = QLineEdit(self)
        self.student_name.setText(student_name)
        layout.addWidget(self.student_name)

        self.course = QComboBox()
        courses = ['Math', 'Astronomy', 'Physics', 'Biology']
        self.course.addItems(courses)
        self.course.setCurrentText(course_name)
        layout.addWidget(self.course)

        self.mobile = QLineEdit(self)
        self.mobile.setText(mobile)
        layout.addWidget(self.mobile)

        self.button = QPushButton('Update', self)
        self.button.clicked.connect(self.update_student)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?', 
                       (self.student_name.text(), self.course.currentText(), self.mobile.text(), main_window.table.item(main_window.table.currentRow(), 0).text()))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()


class InsertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(200)

        layout = QVBoxLayout()

        self.student_name = QLineEdit(self)
        self.student_name.setPlaceholderText('Enter student name')
        layout.addWidget(self.student_name)

        self.course = QComboBox()
        courses = ['Math', 'Science', 'History', 'Geography', 'Computer Science']
        self.course.addItems(courses)
        layout.addWidget(self.course)

        self.mobile = QLineEdit(self)
        self.mobile.setPlaceholderText('Enter mobile number')
        layout.addWidget(self.mobile)

        self.button = QPushButton('Register', self)
        self.button.clicked.connect(self.add_student)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course.currentText()
        mobile = self.mobile.text()

        if name and course and mobile:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)', (name, course, mobile))
            connection.commit()
            cursor.close()
            connection.close()

            main_window.load_data()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Search Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit(self)
        self.student_name.setPlaceholderText('Enter student name')
        layout.addWidget(self.student_name)

        self.button = QPushButton('Search', self)
        self.button.clicked.connect(self.search_student)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()

        if name:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()

            if result:
                QMessageBox.information(self, 'Success', f'Name: {result[1]}\nCourse: {result[2]}\nMobile: {result[3]}')
            else:
                QMessageBox.warning(self, 'Error', 'Student not found')
        else:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
