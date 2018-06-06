import time
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cv2 import *
import threading

class VideoBox(QWidget):

    VIDEO_TYPE_OFFLINE = 0
    VIDEO_TYPE_REAL_TIME = 1

    STATUS_INIT = 0
    STATUS_PLAYING = 1
    STATUS_PAUSE = 2

    video_url = ""

    progress = 0
    
    now_schedule1 = [80,90,70,80,90,90,90,70,90,90,70,80,90,90,100,90,70,90,70,80,90,90,90,70,90,90,70,80,90,90,100,90,70]
    now_schedule2 = [2,3,4,5,3,2,6,1,2,3,4,5,3,2,5,6,1,3,4,5,3,2,6,1,2,3,4,5,3,2,5,6,1]
    now_schedule3 = [3,4,1,5,3,6,4,1,2,4,1,5,3,6,2,4,1,4,1,5,3,6,4,1,2,4,1,5,3,6,2,4,1]
    now_schedule4 = [5,6,3,4,7,4,3,7,8,6,3,4,7,4,5,3,7,6,3,4,7,4,3,7,8,6,3,4,7,4,5,3,7]
    now_schedule5 = [10,7,12,6,7,8,7,11,8,7,12,6,7,8,8,7,11,7,12,6,7,8,7,11,8,7,12,6,7,8,8,7,11]
    
    def __init__(self, video_url="", video_type=VIDEO_TYPE_OFFLINE, auto_play=False):
        QWidget.__init__(self)
        self.setWindowTitle('上海奥卫科技')
        self.setWindowIcon(QIcon('test.jpg'))
        self.video_url = video_url
        self.video_type = video_type  # 0: offline  1: realTime
        self.auto_play = auto_play
        self.status = self.STATUS_INIT  # 0: init 1:playing 2: pause

        # 组件展示
        self.pictureLabel = QLabel()
        init_image = QPixmap("test.jpg").scaled(1000, 700)
        self.pictureLabel.setPixmap(init_image)

        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.switch_video)

        control_box = QHBoxLayout()
        control_box.setContentsMargins(0, 0, 0, 0)
        control_box.addWidget(self.playButton)

        llayout = QVBoxLayout()
        llayout.addWidget(self.pictureLabel)
        llayout.addLayout(control_box)
        
        rlayout = QVBoxLayout()
        # rlayout.setStyleSheet('background:white;')
        # pe = QPalette()  
        # pe.setColor(QPalette.WindowText,Qt.red)#设置字体颜色  
        # self.label1.setAutoFillBackground(True)#设置背景充满，为设置背景颜色的必要条件  
        # pe.setColor(QPalette.Window,Qt.white)#设置背景颜色  
        self.label1 = QLabel()
        self.label1.setContentsMargins(20,0,20,0)
        self.label1.setText("VIDEO LABEL                                      ")
        self.label1.setFont(QFont("",14,QFont.Bold))
        self.label1.setStyleSheet('background:white;')
        
        self.label2 = QLabel()
        self.label2.setContentsMargins(20,0,20,0)
        self.label2.setText("病鸡")
        self.label2.setFont(QFont("",12))
        self.label2.setStyleSheet('background:white;')
        
        self.label3 = QLabel()
        self.label3.setContentsMargins(20,0,20,0)
        self.label3.setText("冻鸡")
        self.label3.setFont(QFont("",12))
        self.label3.setStyleSheet('background:white;')
        
        self.label4 = QLabel()
        self.label4.setContentsMargins(20,0,20,0)
        self.label4.setText("冷鸡")
        self.label4.setFont(QFont("",12))
        self.label4.setStyleSheet('background:white;')
        
        self.label5 = QLabel()
        self.label5.setContentsMargins(20,0,20,0)
        self.label5.setText("渴鸡")
        self.label5.setFont(QFont("",12))
        self.label5.setStyleSheet('background:white;')
        
        self.label6 = QLabel()
        self.label6.setContentsMargins(20,0,20,0)
        self.label6.setText("饿鸡")
        self.label6.setFont(QFont("",12))
        self.label6.setStyleSheet('background:white;')
        
        self.pbar1 = QProgressBar(self)
        
        self.pbar1.setValue(88)
        self.pbar2 = QProgressBar(self)
        
        self.pbar2.setValue(2)
        self.pbar3 = QProgressBar(self)
        
        self.pbar3.setValue(5)
        self.pbar4 = QProgressBar(self)
        
        self.pbar4.setValue(3)
        self.pbar5 = QProgressBar(self)
        
        self.pbar5.setValue(2)

        rlayout.addWidget(self.label1)
        rlayout.addStretch(1)
        rlayout.addWidget(self.label2)
        rlayout.addWidget(self.pbar1)
        rlayout.addStretch(1)
        rlayout.addWidget(self.label3)
        rlayout.addWidget(self.pbar2)
        rlayout.addStretch(1)
        rlayout.addWidget(self.label4)
        rlayout.addWidget(self.pbar3)
        rlayout.addStretch(1)
        rlayout.addWidget(self.label5)
        rlayout.addWidget(self.pbar4)
        rlayout.addStretch(1)
        rlayout.addWidget(self.label6)
        rlayout.addWidget(self.pbar5)
        rlayout.addStretch(20)
        
        layout = QHBoxLayout()
        layout.addLayout(llayout)
        layout.addLayout(rlayout)
        self.setLayout(layout)

        # timer 设置
        self.timer = VideoTimer()
        self.timer.timeSignal.signal[str].connect(self.show_video_images)

        # video 初始设置
        self.playCapture = VideoCapture()
        if self.video_url != "":
            self.set_timer_fps()
            if self.auto_play:
                self.switch_video()
            # self.videoWriter = VideoWriter('*.mp4', VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps, size)
        self.thread2 = threading.Thread(target=self.update_timer)
        self.thread2.setDaemon(True)
        self.thread2.start()
        
    def reset(self):
        self.timer.stop()
        self.playCapture.release()
        self.status = VideoBox.STATUS_INIT
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def set_timer_fps(self):
        self.playCapture.open(self.video_url)
        fps = self.playCapture.get(CAP_PROP_FPS)
        self.timer.set_fps(fps)
        self.playCapture.release()

    def set_video(self, url, video_type=VIDEO_TYPE_OFFLINE, auto_play=False):
        self.reset()
        self.video_url = url
        self.video_type = video_type
        self.auto_play = auto_play
        self.set_timer_fps()
        if self.auto_play:
            self.switch_video()

    def play(self):
        if self.video_url == "" or self.video_url is None:
            return
        if not self.playCapture.isOpened():
            self.playCapture.open(self.video_url)
        self.timer.start()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.status = VideoBox.STATUS_PLAYING

    def stop(self):
        if self.video_url == "" or self.video_url is None:
            return
        if self.playCapture.isOpened():
            self.timer.stop()
            if self.video_type is VideoBox.VIDEO_TYPE_REAL_TIME:
                self.playCapture.release()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.status = VideoBox.STATUS_PAUSE

    def re_play(self):
        if self.video_url == "" or self.video_url is None:
            return
        self.playCapture.release()
        self.playCapture.open(self.video_url)
        self.timer.start()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.status = VideoBox.STATUS_PLAYING

    def show_video_images(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                height, width = frame.shape[:2]
                if frame.ndim == 3:
                    rgb = cvtColor(frame, COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cvtColor(frame, COLOR_GRAY2BGR)

                temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image).scaled(1000,700)
                # temp_pixmap = cv2.resize(temp_pixmap,(700,400))
                self.pictureLabel.setPixmap(temp_pixmap)
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success and self.video_type is VideoBox.VIDEO_TYPE_OFFLINE:
                    print("play finished")  # 判断本地文件播放完毕
                    self.reset()
                    self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()

    def change_schedule(self,i):
        self.pbar1.setValue(self.now_schedule1[i])
        self.pbar2.setValue(self.now_schedule2[i])
        self.pbar3.setValue(self.now_schedule3[i])
        self.pbar4.setValue(self.now_schedule4[i])
        self.pbar5.setValue(self.now_schedule5[i])
        
    def update_timer(self):
        while(True):
            if self.status is VideoBox.STATUS_PLAYING:
                    self.progress = self.progress + 1
                    time.sleep(0.4)  
                    self.change_schedule(self.progress)
                    if(self.progress == 15):
                        self.progress = 0    

    def switch_video(self):
        if self.video_url == "" or self.video_url is None:
            return
        if self.status is VideoBox.STATUS_INIT:
            self.playCapture.open(self.video_url)
            self.timer.start()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        elif self.status is VideoBox.STATUS_PLAYING:
            self.timer.stop()
            if self.video_type is VideoBox.VIDEO_TYPE_REAL_TIME:
                self.playCapture.release()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        elif self.status is VideoBox.STATUS_PAUSE:
            if self.video_type is VideoBox.VIDEO_TYPE_REAL_TIME:
                self.playCapture.open(self.video_url)
            self.timer.start()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        self.status = (VideoBox.STATUS_PLAYING,
                       VideoBox.STATUS_PAUSE,
                       VideoBox.STATUS_PLAYING)[self.status]


class Communicate(QObject):

    signal = pyqtSignal(str)


class VideoTimer(QThread):

    def __init__(self, frequent=20):
        QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()
        self.mutex = QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit("1")
            time.sleep(1 / self.frequent)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.frequent = fps


if __name__ == "__main__":
    mapp = QApplication(sys.argv)
    mw = VideoBox()
    mw.set_video("2.mp4", VideoBox.VIDEO_TYPE_OFFLINE, False)
    mw.show()
    sys.exit(mapp.exec_())