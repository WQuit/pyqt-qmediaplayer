import os
import time
import sys

FileName = os.path.basename(sys.argv[0])
FilePath = sys.argv[0].replace(FileName,"")
UiName = FileName.replace(".py",".ui")
UiPath = FilePath +UiName
Ui_pyName = FilePath+"ui_audio.py"
FileFlag = os.path.isfile(Ui_pyName)

if FileFlag == 0:
	sys_cmd	 = os.popen("pyuic5"+" -o "+Ui_pyName+" "+UiPath)
	time.sleep(1)

from ui_audio import Ui_Audio
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class audioWidget(QWidget):
	def __init__(self):
		super(audioWidget,self).__init__()
		global ui
		ui = Ui_Audio()
		ui.setupUi(self)
		self.audio = ui

	def getSlider(self):
		return self.audio.verticalSlider

	def getMuteBtn(self):
		return self.audio.pushButton