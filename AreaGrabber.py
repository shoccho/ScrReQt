import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizeGrip
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

class AreaGrabber(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Draggable Window')
        self.setGeometry(100, 100, 400, 300)

        # Create a QLabel to act as the draggable area
        self.draggable_label = QLabel("Drag Me", self)
        self.draggable_label.setAlignment(Qt.AlignCenter)
        self.draggable_label.setStyleSheet(
            "background-color: rgba(100, 100, 255, 255); border: 1px solid black;"
        )
        
        # Set layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.draggable_label)
 
        self.grip = QSizeGrip(self)
        self.grip.setGeometry(self.width() - self.grip.width(), self.height() - self.grip.height(), self.grip.width(), self.grip.height())


        # Make the window frameless
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Initialize variables for dragging
        self.dragging = False
        self.offset = None

        # Set semi-translucent background
        self.setWindowOpacity(0.3)
        self.updatePayload()

    def updatePayload(self):
        self.payload = [self.pos().x(), self.pos().y(), self.size().width(), self.size().height()]

    def paintEvent(self, event):
        # Override paintEvent to achieve semi-translucent background
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.updatePayload()
            self.dragging = False
            self.offset = None
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Enter:
            self.updatePayload()
            print(self.payload)
            self.close()

            
    def resizeEvent(self, event):
        self.updatePayload()
        self.grip.setGeometry(self.width() - self.grip.width(), self.height() - self.grip.height(), self.grip.width(), self.grip.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AreaGrabber()
    sys.exit(app.exec_())
