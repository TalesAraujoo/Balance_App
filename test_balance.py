from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt, QPoint, QEvent
from PyQt6.QtGui import QKeySequence, QShortcut


class BalanceApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Balance App v4")
        self.resize(400, 400)
        self.setMinimumSize(200, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Resize state
        self.resizing_left = False
        self.resizing_right = False
        self.resizing_top = False
        self.resizing_bottom = False

        self.drag_pos = None
        self.edge_margin = 8
        self.setMouseTracking(True)

        # --- UI Setup ---
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Title bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(32)
        self.title_bar.setMouseTracking(True)
        self.title_bar.installEventFilter(self)  # For double-click detection

        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_layout.setContentsMargins(8, 0, 8, 0)

        self.title_label = QLabel("Balance App")
        self.btn_min = QPushButton("_")
        self.btn_max = QPushButton("□")
        self.btn_close = QPushButton("×")

        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.btn_min)
        self.title_layout.addWidget(self.btn_max)
        self.title_layout.addWidget(self.btn_close)

        # Content
        self.content = QHBoxLayout()
        self.tmp_label = QLabel(
            "Keyboard shortcuts:\n"
            "• Alt+F4 → Close\n"
            "• Win+↑ → Maximize\n"
            "• Win+↓ → Restore/Minimize\n"
            "• Win+←/→ → Snap left/right\n"
            "• Double-click title bar → Maximize/Restore"
        )
        self.tmp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tmp_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tmp_label.setMouseTracking(True)
        self.content.addWidget(self.tmp_label)

        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addLayout(self.content)
        self.setLayout(self.main_layout)

        # Button connections
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.toggle_max_restore)
        self.btn_close.clicked.connect(self.close)

        # --- Keyboard Shortcuts (Alternative Method) ---
        # You can use QShortcut for some, but keyPressEvent is more reliable for Win key combos
        QShortcut(QKeySequence("Alt+F4"), self, self.close)


    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()


    def toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # --- Double-click on title bar to maximize ---
    def eventFilter(self, obj, event):
        if obj == self.title_bar and event.type() == QEvent.Type.MouseButtonDblClick:
            if event.button() == Qt.MouseButton.LeftButton:
                self.toggle_max_restore()
                return True
        return super().eventFilter(obj, event)

    # --- Main Keyboard Handler ---
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()

        # Alt + F4 → Close
        if key == Qt.Key.Key_F4 and modifiers & Qt.KeyboardModifier.AltModifier:
            self.close()
            return

        # Only process Windows key combinations
        if modifiers == Qt.KeyboardModifier.MetaModifier:  # Meta = Windows key
            if key == Qt.Key.Key_Up:
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

        # Let other keys pass through
        super().keyPressEvent(event)

    # --- Window Snapping Helpers ---
    def snap_to_left(self):
        if self.isMaximized():
            self.showNormal()
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen.left(), screen.top(), screen.width() // 2, screen.height())

    def snap_to_right(self):
        if self.isMaximized():
            self.showNormal()
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(
            screen.left() + screen.width() // 2,
            screen.top(),
            screen.width() // 2,
            screen.height()
        )

    # --- Cursor and Resize Logic (unchanged from your working version) ---
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

            self.resizing_left   = pos.x() < self.edge_margin
            self.resizing_right  = pos.x() > rect.width() - self.edge_margin
            self.resizing_top    = pos.y() < self.edge_margin
            self.resizing_bottom = pos.y() > rect.height() - self.edge_margin

            # Optional: disable top resize in title bar
            if self.resizing_top and pos.y() <= self.title_bar.height():
                self.resizing_top = False

            if any([self.resizing_left, self.resizing_right, self.resizing_top, self.resizing_bottom]):
                self.drag_pos = event.globalPosition().toPoint()
                event.accept()
                return

            if pos.y() <= self.title_bar.height():
                self.drag_pos = event.globalPosition().toPoint()
                event.accept()
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        self.setCursor(self.get_resize_cursor_shape(pos))

        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_pos:
            delta = event.globalPosition().toPoint() - self.drag_pos

            is_resizing = any([self.resizing_left, self.resizing_right,
                               self.resizing_top, self.resizing_bottom])

            if is_resizing:
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

                if self.resizing_top or self.resizing_left:
                    self.move(new_pos)

                self.resize(new_size)
            else:
                self.move(self.pos() + delta)

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
    window = BalanceApp()
    window.show()
    app.exec()