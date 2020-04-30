import os
import time
import sys

FileName = os.path.basename(sys.argv[0])
FilePath = sys.argv[0].replace(FileName,"")
UiName = FileName.replace(".py",".ui")
UiPath = FilePath +UiName
Ui_pyName = FilePath+"ui.py"
FileFlag = os.path.isfile(Ui_pyName)

if FileFlag == 0:
	sys_cmd	 = os.popen("pyuic5"+" -o "+Ui_pyName+" "+UiPath)
	time.sleep(1)

from ui import Ui_Form
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class m_window(QWidget,Ui_Form):
	Index_Signle = pyqtSignal(int)
	def __init__(self):
		super(m_window,self).__init__()
		self.setupUi(self)
		self.playrate = 1.0
		self.listWidget = QListWidget(self)
		self.PushButtonInit()
		self.ProgressBarInit()
		self.mplayer = QMediaPlayer(self)	
		self.ListWidgetInit()
		self.mplayList.setCurrentIndex(0)
		self.mVideoWin = QVideoWidget(self)

		self.LayoutInit()

		self.mplayer.setVideoOutput(self.mVideoWin)
		self.play.clicked.connect(self.PlayVideo)
		self.stop.clicked.connect(self.StopVideo)
		self.fastforwad.clicked.connect(self.FastForword)
		self.jog.clicked.connect(self.Jog)
		self.mplayer.positionChanged.connect(self.PlaySlide)
		self.mplayer.durationChanged.connect(self.MediaTime)
		self.listWidget.itemDoubleClicked.connect(self.GetItem)
		self.Index_Signle.connect(self.SetPlayMedia)

	def LayoutInit(self):
		self.gridLayout.addWidget(self.mVideoWin,0,0,24,16)
		self.gridLayout.addWidget(self.listWidget,0,16,18,2)
		self.gridLayout.addWidget(self.play,24,0,1,1)
		self.gridLayout.addWidget(self.stop,24,1,1,1)
		self.gridLayout.addWidget(self.Slider,24,2,1,5)
		self.gridLayout.addWidget(self.fastforwad,24,7,1,1)
		self.gridLayout.addWidget(self.jog,24,8,1,1)

	def PushButtonInit(self):
		self.play = QPushButton(self)
		self.play.setText("Play")
		self.play.show()
		self.stop = QPushButton(self)
		self.stop.setText("stop")
		self.stop.show()
		self.fastforwad = QPushButton(self)
		self.fastforwad.setText("FastForward")
		self.fastforwad.show()
		self.jog = QPushButton(self)
		self.jog.setText("Jog")
		self.jog.show()

	def ProgressBarInit(self):
		self.Slider = QSlider(Qt.Horizontal,self)
		self.Slider.setRange(0,100)
		self.Slider.show()

	def PlayVideo(self):
		self.mplayer.play()

	def StopVideo(self):
		self.mplayer.pause()

	def FastForword(self):
		self.playrate += 0.2
		self.SetPlaybackRate(self.playrate)

	def Jog(self):
		self.playrate -= 0.2
		self.SetPlaybackRate(self.playrate)

	def MediaTime(self,time):
		self.Slider.setValue(0)
		self.time = self.mplayer.duration() /1000
		self.Slider.setRange(0,int(self.time))

	def PlaySlide(self,val):
		self.Slider.setValue(int(val/1000))

	def ListWidgetInit(self):
		self.mplayList = QMediaPlaylist();
		self.mplayList.addMedia(QMediaContent(QUrl.fromLocalFile("https://vd1.bdstatic.com/mda-hg6uempmez9u6mqi/sc/mda-hg6uempmez9u6mqi.mp4?auth_key=1562172911-0-0-4c22196ad1d0fcc49402d91336c999c5&bcevod_channel=searchbox_feed&pd=bjh&abtest=all")))
		self.mplayList.addMedia(QMediaContent(QUrl.fromLocalFile("https://vd1.bdstatic.com/mda-hgdizw7w7fpc1pcr/sc/mda-hgdizw7w7fpc1pcr.mp4?auth_key=1562254279-0-0-703eb2eca1f7017eaa49b62a7ef56dda&bcevod_channel=searchbox_feed&pd=bjh&abtest=all")))
		self.mplayer.setPlaylist(self.mplayList)
		self.mplayList.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
		self.listWidget.addItem("1")
		self.listWidget.addItem("2")

	def SetPlayMedia(self,Index):
		self.mplayer.stop()
		self.mplayList.setCurrentIndex(Index)
		self.mplayer.play()

	def GetItem(self,Item):
		self.Index = self.listWidget.row(Item)
		self.Index_Signle.emit(self.Index)

	def SetPlaybackRate(self,val):
		self.mplayer.pause()
		self.mplayer.setPlaybackRate(val)
		self.mplayer.play()
		print("playbackRate:",self.mplayer.playbackRate())

app = QApplication(sys.argv)
window = m_window();
window.show()
sys.exit(app.exec_())