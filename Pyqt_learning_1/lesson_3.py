from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QFrame, QTextEdit
)
from PyQt6.QtCore import Qt
import sys

class SplitScreenApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lesson 3A - Split Screen")
        self.setGeometry(100, 100, 800, 400)


        # Main horizontal layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)


        # ------- Left Sidebar -------
        self.sidebar = QFrame()
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setStyleSheet("background-color: #2C3E50;") #Dark sidebar
        self.sidebar.setFixedWidth(200) ## 50% of 800px width
        sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(sidebar_layout)


        # Add buttons to sidebar
        self.btn_home = QPushButton("Home")
        self.btn_profile = QPushButton("Profile")
        self.btn_reports = QPushButton("Reports")
        self.btn_settings = QPushButton("Settings")
        self.btn_help = QPushButton("Help")

        style = """
            QPushButton {
                color: white;
                background-color: #34495E;
                border: none;
                padding: 15px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #3E5871;
            }
            """

        for btn in [self.btn_home, self.btn_profile, self.btn_settings, self.btn_reports, self.btn_help]:
            btn.setStyleSheet(style)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch() # Push buttons up


        # Right Main Content
        self.main_content = QFrame()
        self.main_content.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_content.setStyleSheet("background-color: #ECF0F1;")
        content_layout = QVBoxLayout()
        self.main_content.setLayout(content_layout)


        self.label = QLabel("Welcome! Click a button on the left sidebar.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.label)

        self.text_area = QTextEdit()
        self.tmp_text_area = ["Main content here..."]
        self.text_area.setText(self.list_to_str(self.tmp_text_area))
        content_layout.addWidget(self.text_area)


        # Add sidebar and main content to the main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_content)


        # Connect buttons
        self.btn_home.clicked.connect(lambda: self.update_content("Home"))
        self.btn_profile.clicked.connect(lambda: self.update_content("Profile"))
        self.btn_settings.clicked.connect(lambda: self.update_content("Settings"))
        self.btn_reports.clicked.connect(lambda: self.update_content("Reports"))
        self.btn_help.clicked.connect(lambda: self.update_content("Help"))
        

    def update_content(self, page_name):
        self.label.setText(f"You are viewing the {page_name} page.")
        self.tmp_text_area.append(f"This is the content for {page_name}")
        self.text_area.setText(self.list_to_str(self.tmp_text_area))


    def list_to_str(self, list):
        tmp_str = ''
        for item in list:
            tmp_str = tmp_str + item + '\n'
        
        return tmp_str
    
# ------ Run App ------

app = QApplication(sys.argv)
window = SplitScreenApp()
window.show()
app.exec()
