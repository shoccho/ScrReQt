import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QColor
from enum import Enum
from subprocess import Popen, PIPE, CREATE_NO_WINDOW

from AreaGrabber import AreaGrabber
from FileUtil import *

class CaptureMode(Enum):
    FULLSCREEN = 0
    AREA = 1

class MyApplication(QWidget):
    
    def __init__(self):
        super().__init__()

        self.captureMode = CaptureMode.FULLSCREEN
        self.process = None
        self.initUI()


    def initUI(self):
        # Set window properties
        self.setWindowTitle('Screen Recorder')
        self.setGeometry(300, 300, 480, 300)

        # Create buttons
        self.fullscreen_button = QPushButton('Full Screen', self)
        self.select_area_button = QPushButton('Select Area', self)
        self.start_stop_button = QPushButton('Start', self)

        # Connect button signals to slots
        self.fullscreen_button.clicked.connect(self.onFullScreenClicked)
        self.select_area_button.clicked.connect(self.onSelectAreaClicked)
        self.start_stop_button.clicked.connect(self.onStartStopClicked)

        # Create a QLabel to display the status
        self.status_label = QLabel('Status: Stopped', self)
        
        self.ffmepg_status_label = QLabel('FFMPEG Output: ', self)
        self.updateButtonColors()
        layout = QVBoxLayout(self)
        layout.addWidget(self.fullscreen_button)
        layout.addWidget(self.select_area_button)
        layout.addWidget(self.start_stop_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.ffmepg_status_label)
        layout.addStretch()

        self.areaGrabber = AreaGrabber()

    def updateButtonColors(self):
        color = QColor(100, 255, 100) if self.captureMode == CaptureMode.FULLSCREEN else QColor(255, 255, 255)
        self.fullscreen_button.setStyleSheet(f"background-color: {color.name()}")
        
        color = QColor(100, 255, 100) if self.captureMode == CaptureMode.AREA else QColor(255, 255, 255)
        self.select_area_button.setStyleSheet(f"background-color: {color.name()}")
    def onFullScreenClicked(self):
        
        self.areaGrabber.hide()
        self.captureMode = CaptureMode.FULLSCREEN
        self.updateButtonColors()
        print('Full Screen button clicked')

    def onSelectAreaClicked(self):
        self.captureMode = CaptureMode.AREA
        print('Select Area button clicked')
        self.updateButtonColors()
        self.areaGrabber.show()
        self.select_area_button.setText(f'Area Selected')
    
    def onStartStopClicked(self):
        global process
        current_text = self.start_stop_button.text()
        if(self.captureMode == CaptureMode.AREA):
            self.select_area_button.setText(f'Area Selected {self.areaGrabber.payload}')

        if current_text == 'Start':
            filename = getFileNameWithPath()            
            self.areaGrabber.hide()
            if(self.captureMode == CaptureMode.FULLSCREEN):
                self.captureFullScreen(filename)
            else:
                x,y,w,h = self.areaGrabber.payload
                self.captureArea(x,y,w,h,filename)

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
    


    def runFFMEPG(self, cmd):
        self.process = Popen(cmd.split(' '), stdout=PIPE, stdin=PIPE, stderr=PIPE, creationflags = CREATE_NO_WINDOW)

    def captureArea(self, x, y, w, h, filename):
        cmd = f"./ffmpeg/ffmpeg -f gdigrab -framerate 30 -offset_x {x} -offset_y {y} -video_size {w}x{h} -show_region 1 -i desktop {filename}"
        self.runFFMEPG(cmd)
        
    def captureFullScreen(self, filename):
        cmd = f"./ffmpeg/ffmpeg -f gdigrab -framerate 30 -i desktop {filename}"
        self.runFFMEPG(cmd)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
