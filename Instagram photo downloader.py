import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b>.')
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(50, 35, 210, 25))
        btn = QPushButton('Download', self)
        btn.resize(btn.sizeHint())
        btn.move(110, 70)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Instagram photo downloader')
        self.setWindowIcon((QIcon('vFzlsp5-1024x576.png')))

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(QMessageBox(), 'Message', 'Are you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())