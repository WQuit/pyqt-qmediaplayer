import os
import time
import sys
import json
import platform

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
from urlWidget import urlWidget
from audio import audioWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

config = {'playlist':[],'playCurrent':{'index':0,'audio':30,'postion':0}}		

class m_window(QWidget,Ui_Form):
	def __init__(self):
		super(m_window,self).__init__()
		self.setupUi(self)
		self.videoframe = QVideoWidget(self)
		self.layout_videoframe.addWidget(self.videoframe)
		self.player = QMediaPlayer(self)
		self.player.setVideoOutput(self.videoframe)
		self.playListInit()
		self.connectBind()
		self.bindPlaylistAnddListWidget()
		self.initAudioAndFile()
		self.fileBtnMenuInit()
		self.readConfig()
	
	#音频设置初始化，文件添加初始化
	def initAudioAndFile(self):
		self.urlWidget = urlWidget()
		self.urlWidget.fileInfo_Signle.connect(self.sltUrlWidget)
		self.audio = audioWidget()
		self.audio.hide()
		self.audio.setParent(self)
		self.audio.getSlider().valueChanged.connect(self.sltSetAudioValue)
		self.audio.getMuteBtn().clicked.connect(self.sltSetAudioMute)

	#播放列表初始化 - 声明/定义/播放模式设置
	def playListInit(self):
		self.playList = QMediaPlaylist()
		self.player.setPlaylist(self.playList)
		self.playList.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
		self.player.positionChanged.connect(self.sltShowPlayTime)

	#信号槽绑定函数 -- 主要功能按键 播放/上一个/下一个/音频/文件/设置
	def connectBind(self):
		self.pushButton_play.clicked.connect(self.sltPlayState)
		self.pushButton_befor.clicked.connect(self.sltPlayBefore)
		self.pushButton_next.clicked.connect(self.sltPlayNext)
		self.pushButton_audio.clicked.connect(self.sltAudio)
		self.pushButton_setup.clicked.connect(self.sltSetup)
		self.listWidget_playlist.setContextMenuPolicy(Qt.CustomContextMenu)
		self.listWidget_playlist.customContextMenuRequested.connect(self.listWidgetRightMenu)

	def sltPlayState(self):
		if self.player.state() == QMediaPlayer.StoppedState or self.player.state() == QMediaPlayer.PausedState:
			self.player.play()
			self.pushButton_play.setText("暂停")
		else:
			self.player.pause()
			self.pushButton_play.setText("播放")

	def sltPlayBefore(self):
		self.player.stop()
		self.playList.setCurrentIndex((self.playList.currentIndex()-1 < 0) and 0 or self.playList.currentIndex()-1 )
		self.player.play()

	def sltPlayNext(self):
		self.player.stop()
		self.playList.setCurrentIndex((self.playList.currentIndex() + 1 == self.playList.mediaCount()) and 0 or (self.playList.currentIndex() + 1))
		self.player.play()

	#文件按钮绑定菜单/本地文件/网络资源
	def fileBtnMenuInit(self):
		btnMenu=QMenu(self)
		btnMenu.addAction("本地文件")
		btnMenu.addAction("网络资源")
		self.pushButton_file.setMenu(btnMenu)
		btnMenu.triggered.connect(self.sltFile)

	#添加本地文件
	def addLoadFile(self):
		str = QFileDialog.getOpenFileName(self,"选择媒体文件","D:/","video files(*.avi *.mp4 *.wmv)")
		filePath = str[0]
		fileName = (filePath.split('/')[-1]).split('.')[0]
		return [filePath,fileName]
	
	#添加网络文件
	def addNetFile(self):
		self.urlWidget.show()

	def sltUrlWidget(self,list):
		config['playlist'].append({'filepath':list[0],'filename':list[1]})
		self.addFile(list[0],list[1])

	#槽函数-添加文件
	def sltFile(self,action):
		if action.text() == "本地文件":
			fileInfo = self.addLoadFile()
			config['playlist'].append({'filepath':fileInfo[0],'filename':fileInfo[1]})
			self.addFile(fileInfo[0],fileInfo[1])
		elif action.text() == "网络资源":
			self.addNetFile()

	def addFile(self,filePath,fileName):
		url = QUrl()
		media_file = path(filePath)
		if platform.system() == 'Linux' and os.path.isfile(filePath) == False:
			url.setUrl(filePath, QUrl.StrictMode)
		else:
			url = QUrl.fromLocalFile(filePath)
		self.playList.addMedia(QMediaContent(url))
		self.createItem(fileName)
	
	#音频设置
	def sltAudio(self):
		pos = self.pushButton_audio.mapTo(self,QPoint(0,0))
		x = pos.x() + self.pushButton_audio.width()/2 - self.audio.width() / 2
		y = pos.y() - self.audio.height() - 6
		self.audio.move(x,y)
		if self.audio.isHidden() == True:
			self.audio.show()
		else:
			self.audio.hide()

	def sltSetAudioValue(self,value):
		self.player.setVolume(value)

	def sltSetAudioMute(self):
		self.player.setMuted(bool(1 - self.player.isMuted()))

	#其他设置
	def sltSetup(self):
		print("++++++++++")

	def listWidgetRightMenu(self,point):
		self.menu = QMenu(self.listWidget_playlist)
		self.currentItem = self.listWidget_playlist.itemAt(point)
		play_action = QAction('播放')
		del_action = QAction('删除')
		self.menu.addAction(play_action)
		self.menu.addAction(del_action)
		play_action.triggered.connect(self.actionPlay)
		del_action.triggered.connect(self.actionDel)
		self.menu.exec(QCursor.pos())

	#右键播放槽函数
	def actionPlay(self):
		self.player.stop()
		self.playList.setCurrentIndex(self.listWidget_playlist.row(self.currentItem))
		self.player.play()
		self.pushButton_play.setText("暂停")

    #右键删除槽函数
	def actionDel(self):
		index = self.listWidget_playlist.row(self.currentItem)
		if index == self.playList.currentIndex():
			self.player.stop()
		self.delCurrentIndex(index)

	def delCurrentIndex(self,index):
		current = self.playList.currentIndex()
		if current == index:
			self.playList.setCurrentIndex(0)
			self.player.stop()
		self.playList.removeMedia(index)
		self.listWidget_playlist.takeItem(index)


	#创建QListWidgetItem
	def createItem(self,str):
		self.item = QListWidgetItem(str)
		self.listWidget_playlist.addItem(self.item)

	#绑定QPlayList与QListWidget
	def bindPlaylistAnddListWidget(self):
		self.listWidget_playlist.itemDoubleClicked.connect(self.doublePressPlayMedia)

	def doublePressPlayMedia(self,item):
		self.player.stop()
		self.playList.setCurrentIndex(self.listWidget_playlist.row(item))
		self.player.play()
		self.pushButton_play.setText("暂停")
	
	#显示播放时长
	def sltShowPlayTime(self,postion):
		self.lcdNumber_progress.display(round(postion/1000))

	#配置文件初始化
	def readConfig(self):
		file = open("./config.json","r+",encoding='UTF-8')
		json_str_str = json.load(file)
		for fileInfo in json_str_str['playlist']:
			self.addFile(fileInfo["filepath"],fileInfo["filename"])
			config['playlist'].append({'filepath':fileInfo["filepath"],'filename':fileInfo["filename"]})
		self.playList.setCurrentIndex(json_str_str["playCurrent"]["index"])
		self.audio.getSlider().setValue(json_str_str["playCurrent"]["audio"])
		self.player.setVolume(json_str_str["playCurrent"]["audio"])
		self.player.setPosition(json_str_str["playCurrent"]["postion"] * 1000)

	#写入配置文件
	def writeConfig(self):
		print("Write ConfigFile!")
		for i in range(0,self.playList.mediaCount()):
			path = ""
			if self.playList.media(i).canonicalUrl().isLocalFile():
				path = self.playList.media(i).canonicalUrl().toLocalFile()
			else:
				path = self.playList.media(i).canonicalUrl().toString()
			config['playlist'][i]["filepath"] = path
			config['playlist'][i]["filename"] = self.listWidget_playlist.item(i).text()
		config['playCurrent']['index'] = self.playList.currentIndex()
		config['playCurrent']['audio'] = self.player.volume()
		config['playCurrent']['postion'] = self.player.position() / 1000
		with open("./config.json",'w') as f:
			json.dump(config,f)

	#关闭事件，再退出前重写config配置文件
	def closeEvent(self,event):
		self.writeConfig()

app = QApplication(sys.argv)
window = m_window()
window.show()
sys.exit(app.exec_())