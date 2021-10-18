import os
import time
import sys

FileName = os.path.basename(sys.argv[0])
FilePath = sys.argv[0].replace(FileName,"")
UiName = FileName.replace(".py",".ui")
UiPath = FilePath +UiName
Ui_pyName = FilePath+"ui_url.py"
FileFlag = os.path.isfile(Ui_pyName)

if FileFlag == 0:
	sys_cmd	 = os.popen("pyuic5"+" -o "+Ui_pyName+" "+UiPath)
	time.sleep(1)

from ui_url import Ui_urlWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class urlWidget(QWidget):
	fileInfo_Signle = pyqtSignal(list)
	def __init__(self):
		super(urlWidget,self).__init__()
		global ui
		ui = Ui_urlWidget()
		ui.setupUi(self)
		self.url = ui
		ui.pushButton_2.clicked.connect(self.sltConfirm)

	def getFileInfo(self):
		return [self.url.lineEdit_url.text(),self.url.lineEdit.text()]

	def sltConfirm(self):
		self.fileInfo_Signle.emit([self.url.lineEdit_url.text(),self.url.lineEdit.text()])
		self.hide()

	def sltCancel(self):
		self.hide()
