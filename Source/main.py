from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from youtube import Ui_MainWindowYouTube
from homePage import Ui_MainWindow
import requests
from pytube import YouTube
from pytube.cli import on_progress
import datetime
import _thread


class MainPageYouTube(QMainWindow):
    yt = ""
    final_yt = None
    handle_url = 0
    address_file = ""
    video_1080 = ""
    video_720 = ""
    video_480 = ""
    video_360 = ""
    video_144 = ""
    video_streams = ""
    list_res = list()
    filesize2 = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindowYouTube()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(r"photo\youtube.png"))
        self.setWindowTitle("YouTube Downloader")
        # destroy topWindow =========================
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # ===========================================
        self.ui.mainpage.setCurrentWidget(self.ui.youtube_url)
        self.ui.url_frame_option.hide()
        self.ui.url_frame_youtube.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #283c86, stop:1 #45a247);")
        self.ui.download_progressBar.setValue(0)
        self.ui.url_btn_submit.clicked.connect(self.submit_func)
        self.ui.url_btn_next.clicked.connect(self.next_url_func)
        self.ui.setting_frame_warning.hide()
        self.ui.url_label_waiting.hide()
        self.ui.setting_btn_browse.clicked.connect(self.get_directory)
        self.ui.setting_btn_download.clicked.connect(self.download_setting)

    def submit_func(self):
        if len(self.ui.url_lineEdit_link.text()) != 0:
            try:
                self.yt = YouTube(self.ui.url_lineEdit_link.text(), on_progress_callback=on_progress)
                self.ui.url_label_title_Ent.setText(self.yt.title)
                time = datetime.timedelta(seconds=self.yt.length)
                self.ui.url_label_time_Ent.setText(str(time))
                self.ui.url_label_view_Ent.setText(str(self.yt.views))
                rating = round(self.yt.rating, 2)
                self.ui.url_label_rating_Ent.setText(str(rating))
                self.ui.url_frame_option.show()
                self.handle_url = 1
            except:
                self.showError("Link", "Something went wrong.")
        else:
            self.showError("Link", "You should fill link.")

    def next_url_func(self):
        self.ui.url_label_waiting.show()
        _thread.start_new_thread(self.next_url, (2,))

    def next_url(self, num):
        if self.handle_url == 1:
            self.get_resolution()
            self.ui.mainpage.setCurrentWidget(self.ui.setting)
            self.ui.url_frame_setting.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #283c86, stop:1 #45a247);")

            self.ui.url_frame_youtube.setStyleSheet(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #232526, stop:1 #414345);")
            self.ui.url_label_waiting.hide()
            self.ui.setting_comboBox_res.currentTextChanged.connect(self.set_size_video)

    def set_size_video(self, text):
        if str(text) == "1080p":
            self.final_yt = self.video_streams.filter(resolution="1080p").first()
            self.ui.setting_label_size.setText(str(int(self.final_yt.filesize / 1000000)) + " Mb")
        elif str(text) == "720p":
            self.final_yt = self.video_streams.filter(resolution="720p").first()
            self.ui.setting_label_size.setText(str(int(self.final_yt.filesize / 1000000)) + " Mb")
        elif str(text) == "480p":
            self.final_yt = self.video_streams.filter(resolution="480p").first()
            self.ui.setting_label_size.setText(str(int(self.final_yt.filesize / 1000000)) + " Mb")
        elif str(text) == "360p":
            self.final_yt = self.video_streams.filter(resolution="360p").first()
            self.ui.setting_label_size.setText(str(int(self.final_yt.filesize / 1000000)) + " Mb")
        elif str(text) == "144p":
            self.final_yt = self.video_streams.filter(resolution="144p").first()
            self.ui.setting_label_size.setText(str(int(self.final_yt.filesize / 1000000)) + " Mb")
        self.filesize2 = int(self.final_yt.filesize / 1000000)

    def get_resolution(self):
        self.list_res.append("")
        self.video_streams = self.yt.streams.filter(progressive=True, file_extension="mp4")
        self.video_1080 = self.video_streams.filter(resolution="1080p")
        self.video_720 = self.video_streams.filter(resolution="720p")
        self.video_480 = self.video_streams.filter(resolution="480p")
        self.video_360 = self.video_streams.filter(resolution="360p")
        self.video_144 = self.video_streams.filter(resolution="144p")
        if len(self.video_1080) != 0:
            self.list_res.append("1080p")
        if len(self.video_720) != 0:
            self.list_res.append("720p")
        if len(self.video_480) != 0:
            self.list_res.append("480p")
        if len(self.video_360) != 0:
            self.list_res.append("360p")
        if len(self.video_144) != 0:
            self.list_res.append("144p")
        for item in self.list_res:
            self.ui.setting_comboBox_res.addItem(item)

    def get_directory(self):
        self.address_file = QFileDialog.getExistingDirectory(self, "Select Directory", "./")
        self.ui.setting_lineEdit_browse.setText(self.address_file)

    # problem
    def progress_Check(self, stream=None, chunk=None, file_handle=None, remaining=None):
        percent = (100 * (self.filesize2 - remaining)) / self.filesize2
        print("{:00.0f}% downloaded".format(percent))

    # problem
    def download_process_func(self, num):
        self.final_yt.download(self.address_file)
        print("finished")

    def download_setting(self):
        if len(self.ui.setting_comboBox_res.currentText()) != 0:
            if len(self.address_file) != 0:
                ques = QMessageBox.question(self, "Download", "Are you sure ? ", QMessageBox.Yes | QMessageBox.No)
                if ques == QMessageBox.Yes:
                    self.ui.url_frame_download.setStyleSheet(
                        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #283c86, "
                        "stop:1 #45a247);")
                    self.ui.url_frame_setting.setStyleSheet(
                        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #232526, "
                        "stop:1 #414345);")
                    self.ui.mainpage.setCurrentWidget(self.ui.download)
                    _thread.start_new_thread(self.download_process_func, (2,))
            else:
                self.showError("file address", "You should fill file address.")
        else:
            self.showError("Resolution", "You should select a resolution.")

    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    def showInfo(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Information)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()

    def showError(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Critical)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()


class MainPageHomePage(QMainWindow):
    author_state = False

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui_home = Ui_MainWindow()
        self.ui_home.setupUi(self)
        self.setWindowIcon(QIcon(r"photo\youtube.png"))
        self.setWindowTitle("YouTube Downloader")
        # destroy topWindow =========================
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # ===========================================
        self.ui_home.label_3.hide()
        self.ui_home.home_btn_author.clicked.connect(self.author_info)
        self.ui_home.home_btn_start.clicked.connect(self.start_func)

    def show_info(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Information)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()

    def show_error(self, title, msg):
        info = QMessageBox(self)
        info.setIcon(QMessageBox.Critical)
        info.setText(msg)
        info.setWindowTitle(title)
        info.show()

    def author_info(self):
        if not self.author_state:
            self.ui_home.label_3.show()
            self.author_state = True
        else:
            self.author_state = False
            self.ui_home.label_3.hide()

    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    def start_func(self):
        if self.check_connection():
            self.ui_start = MainPageYouTube()
            self.hide()
            self.ui_start.show()
        else:
            self.show_error("Connection", "Please check your connection.")

    @staticmethod
    def check_connection():
        url = r"https://www.google.com"
        timeout = 5
        try:
            requests.get(url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    def animation_frame(self, frame, x, y, width, height, state):
        if state:
            self.anim = QPropertyAnimation(frame, b"geometry")
            self.anim.setDuration(500)
            self.anim.setStartValue(QRect(x, y, width, 0))
            self.anim.setEndValue(QRect(x, y, width, height))
            self.anim.start()
        else:
            self.anim = QPropertyAnimation(frame, b"geometry")
            self.anim.setDuration(500)
            self.anim.setStartValue(QRect(x, y, width, height))
            self.anim.setEndValue(QRect(x, y, 0, height))
            self.anim.start()


def setup():
    app = QApplication([])
    ui = MainPageHomePage()
    ui.show()
    app.exec_()


setup()
