import sys

import os
import images_rc
import urllib
from PyQt5 import uic
from PyQt5.QtWidgets import *
from model import Parser, Downloader
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5 import QtCore

INCORRECT_SYMBOLS = ['<', '>', ':', '\"', '|', '?', '*', '\\', '/', '\'']


class PhotoLoader(QMainWindow):
    def __init__(self):
        super(PhotoLoader, self).__init__()
        self.ui = uic.loadUi('Design.ui')
        self.catch_btn = self.ui.catchButton
        self.load_button = self.ui.loadButton
        self.link_line = self.ui.lineEdit
        self.menu_bar = self.ui.menuBar
        self.text = self.ui.simpleText
        self.initUI()

    def initUI(self):
        self.ui.setWindowTitle('Photo Loader')
        self.ui.setWindowIcon(QIcon(':/Icons/png/app_icon.png'))
        self.catch_btn.clicked.connect(self.get_load_link)
        self.load_button.clicked.connect(self.file_save)
        self.text.setVisible(False)
        self.load_button.setEnabled(False)
        self.preview = self.ui.preview
        self.ui.statusbar.showMessage(self.link_line.text())
        self.ui.setFixedSize(607, 607)
        self.ui.statusbar.setSizeGripEnabled(False)
        self.ui.actionHelp.triggered.connect(self.about)
        self.ui.actionExit.triggered.connect(self.closeEvent)
        self.ui.show()

    def get_load_link(self):
        """
        Load link.

        Parse an html document and take a link for loading.
        :return: loading link
        """
        if not self.link_line.text():
            self.noEvent()
        else:
            self.ui.statusbar.showMessage('Buffering...')
            try:
                try:
                    os.mkdir('temp')
                except OSError:
                    pass
                link = Parser(self.link_line.text()).parse()
                self.ui.statusbar.showMessage('Caught!')
                cach_image = Downloader(link, os.path.join('temp'))
                cach_image.download()
                self.preview.setPixmap(QPixmap('temp/' +
                                               os.listdir('temp')[0]))
                os.remove('temp/' + os.listdir('temp')[0])

            except ValueError:
                self.ui.statusbar.showMessage('Unknown url type!')
            except urllib.error.URLError:
                self.ui.statusbar.showMessage('Please, check your Internet '
                                              'connection !')
                QMessageBox.warning(None, 'Error!', 'Please, check your Internet connection!')
            else:

                self.load_button.setEnabled(True)
                return link

    def file_save(self):
        directory = QFileDialog.getSaveFileName(self, 'Save image', '/home',
                                                'Images (*jpg)')
        if directory[0]:
            file_name = os.path.split(directory[0])[1]
            for i in INCORRECT_SYMBOLS:
                if i in file_name:
                    self.ui.statusbar.showMessage('Incorrect file name!')
                    break
            if not file_name:
                raise ValueError('Incorrect file name!')
            print(file_name)
            if not file_name.endswith('.jpg'):
                file_name += '.jpg'
            print(file_name)
            self.ui.statusbar.showMessage('Downloading...')
            load = Downloader(self.get_load_link(),
                              os.path.split(directory[0])[0], str(file_name))
            load.download()
            self.link_line.setText('')
            self.ui.statusbar.showMessage('Download finished!')
            self.text.setVisible(True)
            self.load_button.setEnabled(False)

    def about(self):
        QMessageBox.about(self, self.tr('About Application'),
                          self.tr('About Instagram Photo Downloader:\n'
                                  '- this software used for downloading \n '
                                  '  Instagram photos;\n'
                                  '- Catch button - generate downloading link;\n'
                                  '- Download button - for download your photo;\n'
                                  '- !software used for downloading your\n'
                                  '  own photos, but you also can load photos\n'
                                  '  of other users, If you get permission from them!\n'
                                  '- if some errors with downloading photo, please, go \n'
                                  '   to \"Privacy and Security settings\" and uncheck \n'
                                  '  \"Private account\" item, it\'s very important for\n'
                                  '   correct functioning of the program!'))

    def noEvent(self):
        pass

    def restart(self):
        self.initUI()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            qApp.quit()
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PhotoLoader()
    sys.exit(app.exec_())
