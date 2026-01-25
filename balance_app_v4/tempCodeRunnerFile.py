:
        if self.isMaximized():
            self.showNormal()
        
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen.left(), screen.top(), screen.width() // 2, screen.height())
