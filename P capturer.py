import sys
import cv2
import easyocr
import time
import pyautogui
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                            QLabel, QPushButton, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont, QColor, QPainter, QPen

class HealthMonitorGUI(QMainWindow):
    def __init__(self):
        super().__init__() #989890898028590385092859o32850925832095832058329058320598320598325932805832058320958320                10
        self.reader = easyocr.Reader(['en'], gpu=True)
        self.health_bar_region = (1993, 414, 200, 220)
        self.previous_health = None
        self.current_health = None
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        # Main window settings
        self.setWindowTitle("Health Monitor")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel("HEALTH MONITOR")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 18, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #6ac4f1;")
        main_layout.addWidget(title)
        
        # Health display area
        health_display = QFrame()
        health_display.setFrameShape(QFrame.StyledPanel)
        health_display.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 8px;
                border: 1px solid #3a3a3a;
            }
        """)
        health_display.setFixedHeight(120)
        health_layout = QHBoxLayout(health_display)
        health_layout.setContentsMargins(20, 10, 20, 10)
        
        # Health value display
        self.health_value_label = QLabel("--")
        self.health_value_label.setAlignment(Qt.AlignCenter)
        health_value_font = QFont("Arial", 32, QFont.Bold)
        self.health_value_label.setFont(health_value_font)
        self.health_value_label.setStyleSheet("color: #ff6b6b;")
        
        # Health status
        self.health_status_label = QLabel("Monitoring...")
        self.health_status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont("Arial", 12)
        self.health_status_label.setFont(status_font)
        
        health_text_layout = QVBoxLayout()
        health_text_layout.addWidget(self.health_value_label)
        health_text_layout.addWidget(self.health_status_label)
        health_layout.addLayout(health_text_layout)
        
        # Preview image
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                border-radius: 8px;
                border: 1px solid #3a3a3a;
            }
        """)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("background-color: #4CAF50;")
        self.start_button.clicked.connect(self.start_monitoring)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("background-color: #f44336;")
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(exit_button)
        
        # Add widgets to main layout
        main_layout.addWidget(health_display)
        main_layout.addWidget(self.preview_label)
        main_layout.addLayout(button_layout)
        
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_health)
        
    def start_monitoring(self):
        self.timer.start(1000)  # Update every second
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.health_status_label.setText("Monitoring active")
        self.health_status_label.setStyleSheet("color: #4CAF50;")
        
    def stop_monitoring(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.health_status_label.setText("Monitoring paused")
        self.health_status_label.setStyleSheet("color: #f44336;")
        
    def update_health(self):
        health_image = self.capture_health_area(self.health_bar_region)
        
        # Display the captured image
        height, width, channel = health_image.shape
        bytes_per_line = 3 * width
        q_img = QImage(health_image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_img)
        self.preview_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        current_health = self.read_health_value(health_image)
        
        if current_health is not None:
            self.current_health = current_health
            self.health_value_label.setText(str(current_health))
            
            if self.previous_health is not None and current_health < self.previous_health:
                self.health_status_label.setText(f"Health loss detected! {self.previous_health} → {current_health}")
                self.health_status_label.setStyleSheet("color: #ff9800;")
                
            self.previous_health = current_health
        else:
            self.health_value_label.setText("--")
            self.health_status_label.setText("No health value detected")
            self.health_status_label.setStyleSheet("color: #9e9e9e;")
    
    def capture_health_area(self, region):
        screenshot = pyautogui.screenshot(region=region)
        screenshot_np = np.array(screenshot)
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        return screenshot_np
    
    def read_health_value(self, image):
        result = self.reader.readtext(image)
        print(f"OCR Result: {result}")
        
        if result:
            try:
                health_value_text = result[0][1]
                print(f"Detected Text: {health_value_text}")
                health_value = int(health_value_text)
                return health_value
            except (ValueError, IndexError):
                pass
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set dark theme palette
    palette = app.palette()
    palette.setColor(palette.Window, QColor(43, 43, 43))
    palette.setColor(palette.WindowText, Qt.white)
    palette.setColor(palette.Base, QColor(30, 30, 30))
    palette.setColor(palette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(palette.ToolTipBase, Qt.white)
    palette.setColor(palette.ToolTipText, Qt.white)
    palette.setColor(palette.Text, Qt.white)
    palette.setColor(palette.Button, QColor(60, 60, 60))
    palette.setColor(palette.ButtonText, Qt.white)
    palette.setColor(palette.BrightText, Qt.red)
    palette.setColor(palette.Highlight, QColor(106, 196, 241))
    palette.setColor(palette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    window = HealthMonitorGUI()
    window.show()
    sys.exit(app.exec_())
