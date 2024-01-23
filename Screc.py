import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QColor
from enum import Enum
from subprocess import Popen, PIPE, CREATE_NO_WINDOW

from AreaGrabber import AreaGrabber
from FileUtil import *


class CaptureMode(Enum):
    FULL_SCREEN = 0
    AREA = 1


class MyApplication(QWidget):

    def __init__(self):
        super().__init__()

        self.areaGrabber = None
        self.ffmpeg_status_label = None
        self.status_label = None
        self.start_stop_button = None
        self.select_area_button = None
        self.full_screen_button = None

        self.captureMode = CaptureMode.FULL_SCREEN
        self.process = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Screen Recorder')
        self.setGeometry(300, 300, 480, 300)

        self.full_screen_button = QPushButton('Full Screen', self)
        self.select_area_button = QPushButton('Select Area', self)
        self.start_stop_button = QPushButton('Start', self)

        self.full_screen_button.clicked.connect(self.on_full_screen_clicked)
        self.select_area_button.clicked.connect(self.on_select_area_clicked)
        self.start_stop_button.clicked.connect(self.on_start_stop_clicked)

        self.status_label = QLabel('Status: Stopped', self)

        self.ffmpeg_status_label = QLabel('FFMPEG Output: ', self)
        self.update_button_colors()
        layout = QVBoxLayout(self)
        layout.addWidget(self.full_screen_button)
        layout.addWidget(self.select_area_button)
        layout.addWidget(self.start_stop_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.ffmpeg_status_label)
        layout.addStretch()

        self.areaGrabber = AreaGrabber()

    def update_button_colors(self):
        color = QColor(100, 255, 100) if self.captureMode == CaptureMode.FULL_SCREEN else QColor(255, 255, 255)
        self.full_screen_button.setStyleSheet(f"background-color: {color.name()}")

        color = QColor(100, 255, 100) if self.captureMode == CaptureMode.AREA else QColor(255, 255, 255)
        self.select_area_button.setStyleSheet(f"background-color: {color.name()}")

    def on_full_screen_clicked(self):

        self.areaGrabber.hide()
        self.captureMode = CaptureMode.FULL_SCREEN
        self.update_button_colors()
        print('Full Screen button clicked')

    def on_select_area_clicked(self):
        self.captureMode = CaptureMode.AREA
        print('Select Area button clicked')
        self.update_button_colors()
        self.areaGrabber.show()
        self.select_area_button.setText(f'Area Selected')

    def on_start_stop_clicked(self):
        current_text = self.start_stop_button.text()
        if self.captureMode == CaptureMode.AREA:
            self.select_area_button.setText(f'Area Selected {self.areaGrabber.payload}')

        if current_text == 'Start':
            filename = getFileNameWithPath()
            self.areaGrabber.hide()
            if self.captureMode == CaptureMode.FULL_SCREEN:
                self.capture_full_screen(filename)
            else:
                x, y, w, h = self.areaGrabber.payload
                self.capture_area(x, y, w, h, filename)

            print(self.areaGrabber.payload)
            self.start_stop_button.setText('Stop')
            self.status_label.setText(f'Status: Recording {filename}')
        else:
            if self.process is not None:
                # Stop the process if it's running
                self.process.communicate(input=str.encode("q"))
                self.process.terminate()
                self.process.wait()
                print("Process stopped.")
            else:
                print("No process running.")

            self.start_stop_button.setText('Start')
            self.status_label.setText('Status: Stopped')

    def run_ffmpeg(self, cmd):
        self.process = Popen(cmd.split(' '), stdout=PIPE, stdin=PIPE, stderr=PIPE, creationflags=CREATE_NO_WINDOW)

    def capture_area(self, x, y, w, h, filename):
        cmd = f"./ffmpeg/ffmpeg -f gdigrab -offset_x {x} -offset_y {y} -video_size {w}x{h} -i desktop {filename}"
        self.run_ffmpeg(cmd)

    def capture_full_screen(self, filename):
        cmd = f"./ffmpeg/ffmpeg -f gdigrab -i desktop {filename}"
        self.run_ffmpeg(cmd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
