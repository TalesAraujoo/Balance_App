from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt, QEvent


class BalanceApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Balance App v4")
        self.resize(400,600)
        self.setMinimumSize(200, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)

        # Resize variables
        self.resizing_left = False
        self.resizing_right = False
        self.resizing_top = False
        self.resizing_bottom = False

        self.drag_pos = None
        self.edge_margin = 8 # Pixels from edge where resize cursor appears
        self.setMouseTracking(True)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        # Title layout
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(32)
        self.title_bar.setMouseTracking(True)
        self.title_bar.installEventFilter(self) # for double-click detection

        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_layout.setContentsMargins(8,0,8,0)

        self.title_label = QLabel("Balance App")
        self.title_label.setMouseTracking(True)
        self.btn_min = QPushButton("_")
        self.btn_max = QPushButton("□")  #🗗 🗖
        self.btn_close = QPushButton("×")

        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.btn_min)
        self.title_layout.addWidget(self.btn_max)
        self.title_layout.addWidget(self.btn_close)

        # Add title_bar to the main layout

        # Content 
        self.content = QHBoxLayout()
        self.tmp_label = QLabel(
            "Testing - Drag title bar to move, edges to resize")
        self.tmp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tmp_label.setWordWrap(True)
        # Extremely necessary so the app knows when mouse reaches the border
        self.tmp_label.setMouseTracking(True) 
        self.content.addWidget(self.tmp_label)

        # Main Layout settings       
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addLayout(self.content)
        self.setLayout(self.main_layout)

        # title bar buttons
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.toggle_max_restore)
        self.btn_close.clicked.connect(self.close)

    
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()

        # Alt + F4
        if key == Qt.Key.Key_F4 and modifiers == Qt.KeyboardModifier.AltModifier:
            self.close()
            return
    
        # windows + arrows
        if modifiers == Qt.KeyboardModifier.MetaModifier:
            if key == Qt.Key.Key_Up:
                if self.isMinimized():
                    self.showNormal()
                else:
                    self.showMaximized()
            elif key == Qt.Key.Key_Down:
                if self.isMaximized():
                    self.showNormal()
                else:
                    self.showMinimized()
            elif key == Qt.Key.Key_Left:
                self.snap_to_left()
            elif key == Qt.Key.Key_Right:
                self.snap_to_right()
        
        # let others keys get through
        super().keyPressEvent(event)


    def snap_to_left(self):
        if self.isMaximized():
            self.showNormal()
        
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen.left(), screen.top(), screen.width() // 2, screen.height())

    
    def snap_to_right(self):
        if self.isMaximized():
            self.showNormal()

        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen.left() + screen.width() // 2, screen.top(), screen.width() // 2, screen.height())


    def eventFilter(self, obj, event):
        if obj == self.title_bar and event.type() == QEvent.Type.MouseButtonDblClick:
            if event.button() == Qt.MouseButton.LeftButton:
                self.toggle_max_restore()
                return True
        return super().eventFilter(obj, event)

  
    def toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


    def get_resize_cursor_shape(self, pos):
        rect = self.rect()
        left = pos.x() < self.edge_margin
        right = pos.x() > rect.width() - self.edge_margin
        top = pos.y() < self.edge_margin
        bottom = pos.y() > rect.height() - self.edge_margin

        if top and left:
            return Qt.CursorShape.SizeFDiagCursor
        elif top and right:
            return Qt.CursorShape.SizeBDiagCursor
        elif bottom and left:
            return Qt.CursorShape.SizeBDiagCursor
        elif bottom and right:
            return Qt.CursorShape.SizeFDiagCursor
        elif left or right:
            return Qt.CursorShape.SizeHorCursor
        elif top or bottom:
            return Qt.CursorShape.SizeVerCursor
        else:
            return Qt.CursorShape.ArrowCursor
        

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            rect = self.rect()

            self.resizing_left = pos.x() < self.edge_margin
            self.resizing_right = pos.x() > rect.width() - self.edge_margin
            self.resizing_top = pos.y() < self.edge_margin
            self.resizing_bottom = pos.y() > rect.height() - self.edge_margin


            # resize if we're on any edge or corner
            if any([self.resizing_left, self.resizing_right, self.resizing_top, self.resizing_bottom]):
                self.drag_pos = event.globalPosition().toPoint()
                event.accept()
                return

            # Check if we're on the title_bar drag area 
            if pos.y() <= self.title_bar.height():
                self.drag_pos = event.globalPosition().toPoint()
                event.accept()
            
        super().mousePressEvent(event)
            

    def mouseMoveEvent(self, event):
        pos = event.pos()

        cursor_shape = self.get_resize_cursor_shape(pos)
        self.setCursor(cursor_shape)
        # print(cursor_shape) testing to see if it was working

        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_pos:
            delta = event.globalPosition().toPoint() - self.drag_pos


            # Resizing
            if any([self.resizing_top, self.resizing_bottom, self.resizing_left, self.resizing_right]):
                new_size = self.size()
                new_pos = self.pos()

                if self.resizing_left:
                    new_pos.setX(new_pos.x() + delta.x())
                    new_size.setWidth(new_size.width() - delta.x())
                if self.resizing_right:
                    new_size.setWidth(new_size.width() + delta.x())
                if self.resizing_top:
                    new_pos.setY(new_pos.y() + delta.y())
                    new_size.setHeight(new_size.height() - delta.y())
                if self.resizing_bottom:
                    new_size.setHeight(new_size.height() + delta.y())

                new_size = new_size.expandedTo(self.minimumSize())

                # if resizing top left corner, update new position
                if self.resizing_top or self.resizing_left:
                    self.move(new_pos)
                
                self.resize(new_size)

            # Dragging title_bar only
            else: 
                self.move(self.pos() + delta)

            # update reference point        
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()

        super().mouseMoveEvent(event)
            

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.resizing_left = self.resizing_right = self.resizing_top = self.resizing_bottom = False
            self.drag_pos = None
        super().mouseReleaseEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    main_window = BalanceApp()
    main_window.show()
    app.exec()