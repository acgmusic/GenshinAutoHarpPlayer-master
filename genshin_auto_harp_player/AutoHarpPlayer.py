import configparser
import os
import random
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from GSMidiPlayer import GSMidiPlayer
from PyQt5.QtWidgets import (QWidget, QDesktopWidget,
                             QMessageBox, QHBoxLayout, QVBoxLayout, QListWidget,
                             QPushButton, QLabel, QFileDialog, QComboBox)
from utils import get_border_image_url, KeyBoardManager
# import pyautogui

SPEEDS = [0.5, 0.75, 1, 1.25, 1.5]


class AutoHarpPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.PlayModeBtn = QPushButton(self)
        self.playBtn = QPushButton(self)
        self.prevBtn = QPushButton(self)
        self.nextBtn = QPushButton(self)
        self.openBtn = QPushButton(self)
        self.speedCB = QComboBox(self)
        self.speedCB.addItems([f"×{n}" for n in SPEEDS])
        self.speedCB.setCurrentIndex(2)
        self.speedText = QLabel("倍速演奏")

        self.musicList = QListWidget()
        self.song_formats = ['mid', 'midi']
        self.songs_list = []  # List(List(file_name, file_path))
        self.cur_playing_song = ''
        self.is_pause = True
        self.player = GSMidiPlayer()
        self.is_switching = False
        self.playMode = 0
        self.playback_speed = 1

        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        config_path = config_path.replace("\\", '/')
        self.setFileName = config_path
        # self.textLabel = QLabel('作者：https://github.com/acgmusic')
        self.infoLabel = QLabel('author: acgmusic v0.1.0')

        self.playBtn.setStyleSheet(get_border_image_url('play.png'))
        self.playBtn.setFixedSize(48, 48)
        self.nextBtn.setStyleSheet(get_border_image_url('next.png'))
        self.nextBtn.setFixedSize(48, 48)
        self.prevBtn.setStyleSheet(get_border_image_url('prev.png'))
        self.prevBtn.setFixedSize(48, 48)
        self.openBtn.setStyleSheet(get_border_image_url('open.png'))
        self.openBtn.setFixedSize(24, 24)
        self.PlayModeBtn.setStyleSheet(get_border_image_url('sequential.png'))
        self.PlayModeBtn.setFixedSize(24, 24)

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.playByMode)

        # 全局快捷键
        manager = KeyBoardManager(self)
        manager.nextSignal.connect(self.nextMusic)
        manager.prevSignal.connect(self.prevMusic)
        manager.playSignal.connect(self.playMusic)
        manager.start()

        # self.hBoxSlider = QHBoxLayout()
        self.hBoxButton = QHBoxLayout()
        self.hCBox = QHBoxLayout()

        self.hBoxButton.addWidget(self.PlayModeBtn)
        self.hBoxButton.addStretch(1)
        self.hBoxButton.addWidget(self.prevBtn)
        self.hBoxButton.addWidget(self.playBtn)
        self.hBoxButton.addWidget(self.nextBtn)
        self.hBoxButton.addStretch(1)
        self.hBoxButton.addWidget(self.openBtn)

        self.hCBox.addStretch(16)
        self.hCBox.addWidget(self.speedCB)
        self.hCBox.addWidget(self.speedText)

        self.vBoxControl = QVBoxLayout()
        # self.vBoxControl.addLayout(self.hBoxSlider)
        self.vBoxControl.addLayout(self.hBoxButton)
        self.vBoxControl.addLayout(self.hCBox)

        self.hBoxAbout = QHBoxLayout()
        # self.hBoxAbout.addWidget(self.textLabel)
        self.hBoxAbout.addStretch(1)
        self.hBoxAbout.addWidget(self.infoLabel)

        self.vboxMain = QVBoxLayout()
        self.vboxMain.addWidget(self.musicList)
        self.vboxMain.addLayout(self.vBoxControl)
        self.vboxMain.addLayout(self.hBoxAbout)

        self.setLayout(self.vboxMain)

        self.openBtn.clicked.connect(self.openMusicFolder)
        self.playBtn.clicked.connect(self.playMusic)
        self.prevBtn.clicked.connect(self.prevMusic)
        self.nextBtn.clicked.connect(self.nextMusic)
        self.speedCB.currentIndexChanged.connect(self.resetSpeed)
        self.musicList.itemDoubleClicked.connect(self.doubleClicked)
        self.PlayModeBtn.clicked.connect(self.playModeSet)

        self.loadingSetting()

        self.initUI()

    # 初始化界面
    def initUI(self):
        self.resize(600, 400)
        self.center()
        self.setWindowTitle('自动弹琴工具')
        icon_path = os.path.join(os.path.dirname(__file__), f'resource/image/', 'Hutao.ico')
        icon_path = icon_path.replace("\\", '/')
        self.setWindowIcon(QIcon(icon_path))
        self.show()

    # 窗口显示居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 打开文件夹
    def openMusicFolder(self):
        self.cur_path = QFileDialog.getExistingDirectory(self, "请选择乐谱所在文件夹", './')
        if self.cur_path:
            self.showMusicList()
            self.cur_playing_song = ''
            self.updateSetting()
            self.is_pause = True
            self.playBtn.setStyleSheet(get_border_image_url('play.png'))

    # 显示音乐列表
    def showMusicList(self):
        self.musicList.clear()
        self.songs_list.clear()
        if os.path.exists(self.cur_path):
            for song in os.listdir(self.cur_path):
                if song.split('.')[-1] in self.song_formats:
                    self.songs_list.append([song, os.path.join(self.cur_path, song).replace('\\', '/')])
                    self.musicList.addItem(song)
        self.musicList.setCurrentRow(0)
        if self.songs_list:
            self.cur_playing_song = self.songs_list[self.musicList.currentRow()][-1]

    # 提示
    def Tips(self, message):
        QMessageBox.about(self, "提示", message)

    # 设置当前播放的音乐
    def setCurPlaying(self):
        self.cur_playing_song = self.songs_list[self.musicList.currentRow()][-1]
        # self.player.setMedia(QMediaContent(QUrl(self.cur_playing_song)))
        self.player.setMedia(self.cur_playing_song, speed=self.playback_speed)
        # print("开始播放", self.cur_playing_song)

    # 播放/暂停播放
    def playMusic(self):
        if self.musicList.count() == 0:
            self.Tips('当前路径内无可播放的音乐文件')
            return
        # if not self.player.isAudioAvailable():
        #     self.setCurPlaying()
        if self.is_pause or self.is_switching:
            self.playBtn.setStyleSheet(get_border_image_url('pause.png'))
            self.player.play()
            self.is_pause = False

        elif (not self.is_pause) and (not self.is_switching):
            print("开始3")
            self.playBtn.setStyleSheet(get_border_image_url('play.png'))
            self.player.pause()
            self.is_pause = True


    # 上一曲
    def prevMusic(self):
        if self.musicList.count() == 0:
            self.Tips('当前路径内无可播放的音乐文件')
            return
        # 如果处于随机播放
        if self.playMode == 2:
            pre_row = random.randint(0, self.musicList.count() - 1)
        else:
            pre_row = self.musicList.currentRow() - 1 if self.musicList.currentRow() != 0 else self.musicList.count() - 1
        self.musicList.setCurrentRow(pre_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    # 下一曲
    def nextMusic(self):
        if self.musicList.count() == 0:
            self.Tips('当前路径内无可播放的音乐文件')
            return
        # 如果处于随机播放
        if self.playMode == 2:
            next_row = random.randint(0, self.musicList.count() - 1)
        else:
            next_row = self.musicList.currentRow() + 1 if self.musicList.currentRow() != self.musicList.count() - 1 else 0
        self.musicList.setCurrentRow(next_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    # 双击歌曲名称播放音乐
    def doubleClicked(self):
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    # 根据播放模式进行播放
    def playByMode(self):
        # 顺序播放
        if (self.playMode == 0) and (not self.is_pause) and (not self.is_switching):
            if self.musicList.count() == 0:
                return
            if self.player.position() == self.player.duration():
                # pyautogui.press('esc')
                self.nextMusic()
        # 单曲循环
        elif (self.playMode == 1) and (not self.is_pause) and (not self.is_switching):
            if self.musicList.count() == 0:
                return
            if self.player.position() == self.player.duration():
                # pyautogui.press('esc')
                self.is_switching = True
                self.setCurPlaying()
                self.playMusic()
                self.is_switching = False
        # 随机播放
        elif (self.playMode == 2) and (not self.is_pause) and (not self.is_switching):
            if self.musicList.count() == 0:
                return
            if self.player.position() == self.player.duration():
                # pyautogui.press('esc')
                self.is_switching = True
                self.musicList.setCurrentRow(random.randint(0, self.musicList.count() - 1))
                self.setCurPlaying()
                self.playMusic()
                self.is_switching = False

    def resetSpeed(self, index):
        self.playback_speed = SPEEDS[index]

    # 更新配置文件
    def updateSetting(self):
        config = configparser.ConfigParser()
        config.read(self.setFileName)
        if not os.path.isfile(self.setFileName):
            config.add_section('AutoHarpPlayer')
        config.set('AutoHarpPlayer', 'PATH', self.cur_path)
        config.write(open(self.setFileName, 'w'))

    # 加载配置文件
    def loadingSetting(self):
        config = configparser.ConfigParser()
        config.read(self.setFileName)
        if not os.path.isfile(self.setFileName):
            return
        self.cur_path = config.get('AutoHarpPlayer', 'PATH')
        self.showMusicList()

    # 播放模式设置
    def playModeSet(self):
        # 设置为单曲循环模式
        if self.playMode == 0:
            self.playMode = 1
            self.PlayModeBtn.setStyleSheet(get_border_image_url('circulation.png'))
        # 设置为随机播放模式
        elif self.playMode == 1:
            self.playMode = 2
            self.PlayModeBtn.setStyleSheet(get_border_image_url('random.png'))
        # 设置为顺序播放模式
        elif self.playMode == 2:
            self.playMode = 0
            self.PlayModeBtn.setStyleSheet(get_border_image_url('sequential.png'))

    # 确认用户是否要真正退出
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "确定要退出吗？", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import (QApplication)

    app = QApplication(sys.argv)
    ex = AutoHarpPlayer()
    sys.exit(app.exec_())
