import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class TransparentHUD(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 500, 140)

        self.mic_on = True
        self.cam_on = True
        self.sys_on = True

        self.label = QtWidgets.QLabel('LTO HUD: All systems active', self)
        self.label.setStyleSheet('color: white; font-size: 18px; background: transparent;')
        self.label.move(20, 10)

        self.mic_btn = QtWidgets.QPushButton('Mic: ON', self)
        self.mic_btn.setCheckable(True)
        self.mic_btn.setChecked(True)
        self.mic_btn.setGeometry(20, 60, 120, 40)
        self.mic_btn.clicked.connect(self.toggle_mic)

        self.cam_btn = QtWidgets.QPushButton('Camera: ON', self)
        self.cam_btn.setCheckable(True)
        self.cam_btn.setChecked(True)
        self.cam_btn.setGeometry(160, 60, 120, 40)
        self.cam_btn.clicked.connect(self.toggle_cam)

        self.sys_btn = QtWidgets.QPushButton('System: ON', self)
        self.sys_btn.setCheckable(True)
        self.sys_btn.setChecked(True)
        self.sys_btn.setGeometry(300, 60, 120, 40)
        self.sys_btn.clicked.connect(self.toggle_sys)

        self.show()

    def toggle_mic(self):
        self.mic_on = not self.mic_on
        self.mic_btn.setText(f"Mic: {'ON' if self.mic_on else 'OFF'}")
        self.label.setText(f"Mic {'enabled' if self.mic_on else 'disabled'} by user.")

    def toggle_cam(self):
        self.cam_on = not self.cam_on
        self.cam_btn.setText(f"Camera: {'ON' if self.cam_on else 'OFF'}")
        self.label.setText(f"Camera {'enabled' if self.cam_on else 'disabled'} by user.")

    def toggle_sys(self):
        self.sys_on = not self.sys_on
        self.sys_btn.setText(f"System: {'ON' if self.sys_on else 'OFF'}")
        self.label.setText(f"System {'enabled' if self.sys_on else 'disabled'} by user.")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QColor(0, 0, 0, 80))  # semi-transparent black
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    hud = TransparentHUD()
    sys.exit(app.exec_())
