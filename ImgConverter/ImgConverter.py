# -*- coding: utf-8 -*-

import PIL
import tempfile
import sys
import os
import re
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel,\
                            QComboBox, QMessageBox
from PyQt5.QtWidgets import QPushButton, QGroupBox, QHBoxLayout, QVBoxLayout


class ImgConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle('PyImgConverter')
        self.setWindowIcon(QtGui.QIcon('images/ico.jpg'))
        self.setGeometry(100, 50, 1000, 650)
        self.setFixedSize(1000, 650)
        self.setStyleSheet('''
        QMainWindow {
                background-image: url("images/bkg.png");
                background-repeat: no-repeat;
        }
        ''')
        flag = QtCore.Qt.WindowFlags(QtCore.Qt.WindowMinimized)
        self.setWindowFlags(flag)

        self.Buttons()
        self.StatsBox()
        self.PreviewBox()

        self.show()

    def Buttons(self):
        self.groupBox = QGroupBox('', self)
        self.groupBox.setGeometry(0, 0, self.width(), 60)
        self.container = QHBoxLayout()

        self.bt1 = QPushButton('Open', self)
        self.bt1.setMinimumHeight(40)
        self.bt1.clicked.connect(self.Open)
        self.container.addWidget(self.bt1)

        self.conv_text = QLabel('<h3><b>Convert to:</b></h3>')
        self.conv_text.setMinimumHeight(40)
        self.conv_text.setMaximumWidth(125)
        self.conv_text.setStyleSheet('''
        QLabel {
                color: white;
                padding-left: 20px;
        }
        ''')
        self.container.addWidget(self.conv_text)

        self.option = QComboBox()
        self.option.setMinimumHeight(40)
        self.option.setMaximumWidth(125)
        self.option.addItem('')

        a = PIL.Image.registered_extensions()
        b = a.keys()
        c = list(b)
        for ext in c:
            self.option.addItem(ext[1:])

        self.container.addWidget(self.option)

        self.bt2 = QPushButton('Save As', self)
        self.bt2.setMinimumHeight(40)
        self.bt2.clicked.connect(self.Save)
        self.container.addWidget(self.bt2)

        self.bt3 = QPushButton('Exit', self)
        self.bt3.setMinimumHeight(40)
        self.bt3.clicked.connect(sys.exit)
        self.container.addWidget(self.bt3)

        self.groupBox.setStyleSheet('''
        QPushButton {
            color:white;
            background-color:grey;
        }
        QLabel {
            background-color:grey;
        }
        ''')
        self.groupBox.setLayout(self.container)

    def StatsBox(self):
        self.txtbox = QGroupBox('Picture Statistics', self)
        self.txtbox.setGeometry(0, 60, 250, 590)
        self.txtbox.setStyleSheet('QLabel{color: darkred}')
        self.container1 = QVBoxLayout()

        self.label1 = QLabel("Name: <b>----</b>")
        self.container1.addWidget(self.label1)

        self.label2 = QLabel("Path: <b>----</b>")
        self.container1.addWidget(self.label2)

        self.label3 = QLabel("Resolution: <b>--- x ---</b>")
        self.container1.addWidget(self.label3)

        self.label4 = QLabel("Size: <b>---</b>")
        self.container1.addWidget(self.label4)

        self.txtbox.setLayout(self.container1)

    def PreviewBox(self):
        self.picbox1 = QGroupBox('Picture Preview', self)
        self.picbox1.setGeometry(250, 60, 750, 590)

        self.container2 = QVBoxLayout()
        self.labelimg1 = QLabel()
        self.labelimg1.setStyleSheet('background:white')

        self.container2.addWidget(self.labelimg1)

        self.picbox1.setLayout(self.container2)

    def Open(self):
        a = PIL.Image.registered_extensions()
        b = a.keys()
        c = list(b)
        d = ['*{}'.format(x) for x in c]
        ext = ' '.join(d)

        self.og_img = QFileDialog.getOpenFileName(self, 'Open Image', '', f'Image files {ext}')
        if self.og_img != ('', ''):
            extension = re.search(r'[a-zA-Z]{3,4}$', self.og_img[0]).group()
        else:
            return None

        self.img1 = PIL.Image.open(self.og_img[0])
        width, height = self.img1.size

        file = tempfile.gettempdir()
        img = f'{file}\\tmpQbfhp98.{extension}'.replace('\\', '/')

        if width > 725 and height > 560:
            PIL.Image.open(self.og_img[0]).resize((725, 560)).save(img)
            self.labelimg1.setStyleSheet(f"background: url({img}) no-repeat")
        elif width > 725:
            PIL.Image.open(self.og_img[0]).resize((725, height)).save(f'{img}')
            self.labelimg1.setStyleSheet(f'''background: url({img}) no-repeat;
                                             background-position: center;''')
        elif height > 560:
            PIL.Image.open(self.og_img[0]).resize((width, 560)).save(f'{img}')
            self.labelimg1.setStyleSheet(f'''background: url({img}) no-repeat;
                                             background-position: center;''')
        else:
            self.labelimg1.setStyleSheet(f'''background: url({self.og_img[0]}) no-repeat;
                                             background-position: center;''')

        name = re.search(r'[^/\\]+[.][A-Za-z]{3,4}', self.og_img[0]).group()
        self.label1.setText(f'Name: <b>{name}</b>')

        self.label2.setText('Path: <b>{}</b>'.format(self.og_img[0]))
        self.label2.setToolTip('{}'.format(self.og_img[0]))

        self.label3.setText(f'Resolution: <b>{width} x {height}</b>')

        size = os.stat(self.og_img[0])
        size = size[6]
        if size < 1024:
            res = f'{size} bytes'
        elif size < 1048576:
            res = f'{size/1024} kb'
        elif size < 1073741824:
            res = f'{size/1048576} mb'
        self.label4.setText('Size: <b>{}</b>'.format(res))

    def Save(self):
        try:
            if self.og_img:
                if bool(self.option.currentText()):
                    self.sv_img = QFileDialog.getSaveFileName(self, 'Save Image', '', self.option.currentText())
                    if self.sv_img == ('', ''):
                        return None
                    else:
                        save_loc = f'{self.sv_img[0]}.{self.sv_img[1]}'
                        PIL.Image.open(self.og_img[0]).save(save_loc)
                else:
                    note = QMessageBox(self)
                    note.about(self, 'Notification', '<b>Select extension for image to be converted to.</b>')
        except AttributeError:
            note = QMessageBox(self)
            note.about(self, 'Notification', '<b>You have not selected any image to convert.</b>')


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = ImgConverter()
    window.show()
    sys.exit(App.exec())
