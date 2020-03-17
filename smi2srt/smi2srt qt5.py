#! python3
# -*- coding: utf-8 -*-

import sys
import re
from PyQt5 import QtCore, QtGui
from datetime import timedelta
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QAction, \
                            QMessageBox, QTextEdit, QProgressBar
from PyQt5.QtWidgets import QPushButton, QGroupBox, QHBoxLayout


class Smi2Srt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle('smi2srt Converter')
        self.setWindowIcon(QtGui.QIcon('images/convert.png'))
        self.setGeometry(100, 50, 500, 650)
        self.setFixedSize(500, 650)
        flag = QtCore.Qt.WindowFlags(QtCore.Qt.WindowMinimized)
        self.setWindowFlags(flag)

        self.MenuBar()
        self.OutputBox()
        self.Button_and_bar()
        self.show()

    def MenuBar(self):
        mainMenu = self.menuBar()
        mainMenu.setStyleSheet('background-color:lightgrey')

        fileMenu = mainMenu.addMenu('File')
        aboutMenu = mainMenu.addMenu('About')
        '''helpMenu = mainMenu.addMenu('Help')'''

        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.Open)
        fileMenu.addAction(openAction)

        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.Save)
        fileMenu.addAction(saveAction)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+E')
        exitAction.triggered.connect(sys.exit)
        fileMenu.addAction(exitAction)

        aboutAction = QAction('About smi2srt', self)
        aboutAction.triggered.connect(self.About)
        aboutMenu.addAction(aboutAction)

    def OutputBox(self):
        self.outspace = QGroupBox('Srt Output', self)
        self.outspace.setGeometry(0, 22, self.width(), self.height()*9/10)

        self.box2 = QHBoxLayout()
        self.outbox = QTextEdit()

        self.box2.addWidget(self.outbox)
        self.outspace.setLayout(self.box2)

    def Button_and_bar(self):
        self.bt = QPushButton('Convert', self)
        self.bt.setIcon(QtGui.QIcon('images/convert.png'))
        self.bt.setIconSize(QtCore.QSize(20, 20))
        self.bt.setGeometry(10, 612.5, 100, 30)
        self.bt.clicked.connect(self.Convert)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(120, 612.5, 370, 30)

    def Open(self):
        self.op = QFileDialog.getOpenFileName(self, 'Open file', '', 'Smi files *.smi')

        if self.op != ('', ''):
            self.outbox.clear()
            self.progress.setValue(0)
            with open(f'{self.op[0]}', 'r') as f:
                self.smiContent = f.read()

    def content(self):
        ent1 = re.sub(r'&#39;', "'", self.smiContent)
        ent2 = re.sub(r'&#40;', '"', ent1)
        # content seeking
        ent3 = re.findall(r'(?<=SYNC\s)Start=.*?<SYNC|(?<=SYNC\s)Start=.*?</body', ent2, re.DOTALL)
        # filter and concatenation of strings
        ent4 = [re.sub(r'\n', ' ', item0) for item0 in ent3]
        ent5 = []
        for item0 in ent4:
            a = re.findall(r'>.*?<', item0)
            b = [c for c in a if c != '><']
            d = []
            for e in b:
                f = re.search(r'[^>].*[^<]', e)
                # filter of None values
                if bool(f) is True:
                    d.append(f.group())
                else:
                    continue
            g = ''.join(d)
            ent5.append(g)
        self.progress.setMaximum(len(ent5))
        for item0 in ent5:
            if bool(re.match(r'.+', item0)) is not True:
                yield '......'
            else:
                yield item0

    def time(self):
        ent1 = re.sub(r'&#39;', "'", self.smiContent)
        ent2 = re.sub(r'&#40;', '"', ent1)
        # define search for times
        a = re.findall(r'Start=[\d]+', ent2)
        # add times to list
        b = [(re.search(r'[\d]+', item0)).group() for item0 in a]
        # convert times to desired format
        d = []
        for item0 in b:
            e = timedelta(milliseconds=int(item0))
            if re.search(r'[.]', str(e)) is None:
                f = str(e) + '.000'
            else:
                f = str(e)
            d.append(f[0:11])
        return list(enumerate(d))

    def Convert(self):
        try:
            x = 1
            for tim, cont in zip(self.time(), self.content()):
                # iteration correction for last
                if tim[0] == len(self.time()) - 1:
                    var1 = re.sub(r"[0-5][0-9]\Z", '58', tim[1])
                    var2 = re.sub(r'[0-5][0-9][^:\d]', '59.', var1)
                    self.outbox.insertPlainText(str(tim[0] + 1) + '\n')
                    self.outbox.insertPlainText(tim[1] + ' --> ' + var2 + '\n')
                    self.outbox.insertPlainText(cont + '\n')
                    self.progress.setValue(x)
                    break
                # writing of srt file
                self.outbox.insertPlainText(str(tim[0] + 1) + '\n')
                self.outbox.insertPlainText(tim[1] + ' --> ' + self.time()[tim[0] + 1][1] + '\n')
                self.outbox.insertPlainText(cont + '\n\n')
                self.progress.setValue(x)
                x += 1

        except AttributeError:
            pass

    def Save(self):
        self.sv = QFileDialog.getSaveFileName(self, 'Save file', '', 'Srt files *.srt')

        if self.sv != ('', ''):
            with open(f'{self.sv[0]}', 'w') as f:
                f.write(self.outbox.toPlainText())

    def About(self):
        note = QMessageBox(self)
        note.about(self, 'About smi2srt',
                   '''<b>Created By:</b> Ndokanga Kudakwashe<br/>
                      <b>Email:</b> ndokaskuda1999@gmail.com
                          <center><b><u>Purpose</u></b></center>
                      This application converts subtitle files<br/>
                      from SMI format to SRT format.
                      ''')


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Smi2Srt()
    sys.exit(App.exec())
