# -*- coding: utf-8 -*-
"""
Created on Sat May 12 13:04:37 2018

@author: fengmaniu
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
import time
import cv2

class Chick_GUI:
    imgDict = {}
    playing = False
    imageVideo = None
    timer = None
    pathVideo = "2.mp4"
    value = 20
    progress = 0
    #text.set('视频')
    now_schedule1 = [80, 90, 70, 80, 90, 90, 90, 70, 90, 90, 70, 80, 90, 90, 100, 90, 70, 90, 70, 80, 90, 90, 90, 70,
                     90, 90, 70, 80, 90, 90, 100, 90, 70]
    now_schedule2 = [2, 3, 4, 5, 3, 2, 6, 1, 2, 3, 4, 5, 3, 2, 5, 6, 1, 3, 4, 5, 3, 2, 6, 1, 2, 3, 4, 5, 3, 2, 5, 6, 1]
    now_schedule3 = [3, 4, 1, 5, 3, 6, 4, 1, 2, 4, 1, 5, 3, 6, 2, 4, 1, 4, 1, 5, 3, 6, 4, 1, 2, 4, 1, 5, 3, 6, 2, 4, 1]
    now_schedule4 = [5, 6, 3, 4, 7, 4, 3, 7, 8, 6, 3, 4, 7, 4, 5, 3, 7, 6, 3, 4, 7, 4, 3, 7, 8, 6, 3, 4, 7, 4, 5, 3, 7]
    now_schedule5 = [10, 7, 12, 6, 7, 8, 7, 11, 8, 7, 12, 6, 7, 8, 8, 7, 11, 7, 12, 6, 7, 8, 7, 11, 8, 7, 12, 6, 7, 8,
                     8, 7, 11]
    def __init__(self,cav):
        # initlize cav(first canvas)
        cav.title("智环AI识别")
        cav.geometry('1200x600')                 
        cav.resizable(width=False, height=False)
        # cav->fm1+fm2
        # fm1->fm11+fm12
        self.fm1 = tk.Frame(cav, width=700, bg="#DBDBDB")

        # 使用OpenCV读取要播放的视频文件
        self.videoCap = cv2.VideoCapture(self.pathVideo)

        # get frame rate of the video
        self.frameRate    = int(self.videoCap.get(cv2.CAP_PROP_FPS))
        self.frameCount   = int(self.videoCap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frameCurrent = 0
        self.scale_focus  = False
        self.root = cav
        
        # fm11 显示视频
        self.fm11 = tk.Frame(self.fm1, width=700, height=450, bg="#DBDBDB")
        tk.Label(self.fm11, text="视频", font=("Arial", 16),bg="#DBDBDB").\
        pack(expand=tk.YES, side=tk.TOP, pady=5, padx=5, anchor=tk.W)
        #image1 = Image.OPEN(r'test.jpg') # C:\\code\\intelligencering\\chicken_video_demo\\chicken_video_demo\\chicken_demo\\
        #image1 = ImageTk.PhotoImage(image1)
        #image1 = tk.PhotoImage(file="C:\\test.jpg") 只支持gif格式
        #image1 = self.getImgWidget("/Users/Jiankors/Documents/test.png")
        self.imageVideo = self.getImageFromVideo()
        self.labelVideo = tk.Label(self.fm11, image=self.imageVideo, width=700,height=400)
        self.labelVideo.pack(side=tk.TOP, padx=5, anchor=tk.W,expand=tk.YES)
        self.fm11.pack(pady=5,fill=tk.BOTH)
        
        # fm12 视频选项 开始 暂停 进度条
        self.fm12 = tk.Frame(self.fm1, width=700,height=150, bg="")
        tk.Button(self.fm12, text="开始", font=("Arial", 13), command = self.playVideo).pack(side=tk.LEFT, padx=5)
        tk.Button(self.fm12, text="暂停", font=("Arial", 13), command = self.pauseVideo).pack(side=tk.LEFT, padx=5)
		
        self.scale = tk.Scale(self.fm12, from_=0, to=100, orient=tk.HORIZONTAL, command=self.scaleValueChanged) # command: define function
        self.scale.set(0)  # 设置初始值
        self.scale.bind('<ButtonPress-1>', lambda x:self.scaleFocus(True))
        self.scale.bind('<ButtonRelease-1>', lambda x:self.scaleFocus(False))
        self.scale.pack(fill=tk.X, expand=2, side=tk.LEFT, padx=5, ipady=5)
        self.fm12.pack(pady=5,fill=tk.BOTH)
        self.fm1.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

        # fm2
        self.fm2 = tk.Frame(cav, width=500, bg="#DBDBDB")

        tk.Label(self.fm2, text="VIDEO LABEL", font=("Arial", 16)).grid(row=0, column=0, sticky=tk.W, rowspan=1, pady=5)

        tk.Label(self.fm2, text="健康鸡", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, rowspan=1, pady=5)

        self.canvas1 = tk.Canvas(self.fm2, width=400, height=30, bg="white")
        self.canvas1.grid(row=3, column=0)
        self.x1 = tk.StringVar()
        # 进度条以及完成程度
        self.out_rec1 = self.canvas1.create_rectangle(5, 5, 400, 25, outline="#CDCD00", width=1)
        self.fill_rec1 = self.canvas1.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="#CDCD00")
        tk.Label(self.fm2, textvariable=self.x1).grid(row=3, column=1)

        tk.Label(self.fm2, text="渴鸡", font=("Arial", 12)).grid(row=4, column=0, sticky=tk.W, rowspan=1, pady=5)

        self.canvas2 = tk.Canvas(self.fm2, width=400, height=30, bg="white")
        self.canvas2.grid(row=5, column=0)
        self.x2 = tk.StringVar()
        # 进度条以及完成程度
        self.out_rec2 = self.canvas2.create_rectangle(5, 5, 400, 25, outline="#912CEE", width=1)
        self.fill_rec2 = self.canvas2.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="#912CEE")
        tk.Label(self.fm2, textvariable=self.x2).grid(row=5, column=1)

        tk.Label(self.fm2, text="病鸡", font=("Arial", 12)).grid(row=6, column=0, sticky=tk.W, rowspan=1, pady=5)

        self.canvas3 = tk.Canvas(self.fm2, width=400, height=30, bg="white")
        self.canvas3.grid(row=7, column=0)
        self.x3 = tk.StringVar()
        # 进度条以及完成程度
        self.out_rec3 = self.canvas3.create_rectangle(5, 5, 400, 25, outline="#8B4789", width=1)
        self.fill_rec3 = self.canvas3.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="#8B4789")
        tk.Label(self.fm2, textvariable=self.x3).grid(row=7, column=1)

        tk.Label(self.fm2, text="冷鸡", font=("Arial", 12)).grid(row=8, column=0, sticky=tk.W, rowspan=1, pady=5)

        self.canvas4 = tk.Canvas(self.fm2, width=400, height=30, bg="white")
        self.canvas4.grid(row=9, column=0)
        self.x4 = tk.StringVar()
        # 进度条以及完成程度
        self.out_rec4 = self.canvas4.create_rectangle(5, 5, 400, 25, outline="#EE799F", width=1)
        self.fill_rec4 = self.canvas4.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="#EE799F")
        tk.Label(self.fm2, textvariable=self.x4).grid(row=9, column=1)

        tk.Label(self.fm2, text="饿鸡", font=("Arial", 12)).grid(row=10, column=0, sticky=tk.W, rowspan=1, pady=5)

        self.canvas5 = tk.Canvas(self.fm2, width=400, height=30, bg="white")
        self.canvas5.grid(row=11, column=0)
        self.x5 = tk.StringVar()
        # 进度条以及完成程度
        self.out_rec5 = self.canvas5.create_rectangle(5, 5, 400, 25, outline="#54FF9F", width=1)
        self.fill_rec5 = self.canvas5.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="#54FF9F")
        tk.Label(self.fm2, textvariable=self.x5).grid(row=11, column=1)

        self.fm2.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)
		
        self.video_loop()

        #self.thread = threading.Thread(target=self.fun_timer)
        #self.thread.setDaemon(True)
        #self.thread.start()

        self.thread2 = threading.Thread(target=self.update_timer)
        self.thread2.setDaemon(True)
        self.thread2.start()


    def shutdown(self):
        self.videoCap.release()

    def getImgWidget(self,filePath): # 图片显示不出来，要保存起来
        
        if os.path.exists(filePath) and os.path.isfile(filePath):
            if filePath in self.imgDict and self.imgDict[filePath]:
                return self.imgDict[filePath]
            img = Image.open(filePath)
            img = self.resize(700, 400, img)
            #print(img.size)
            img = ImageTk.PhotoImage(img)
            self.imgDict[filePath] = img
            return img
        return None

    def getImageFromVideo(self):
        ret, frame = self.videoCap.read()
        if ret:
            # convert colors from BGR to RGBA
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            cv2image = cv2.resize(cv2image, (700, 400) ,interpolation=cv2.INTER_AREA)

            # frame increasement
            self.frameCurrent = self.frameCurrent + 1

            # Convert the Image object into a TkPhoto object
            img = Image.fromarray(cv2image)
            #img = self.resize(700, 400, img)
            #print(img.size)
            self.imageVideo = ImageTk.PhotoImage(img)
        else:
            # reset video when finished or invalid
            self.videoCap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.playing = False
            self.frameCurrent = 0
            self.change_schedule(self.progress, 99)
            self.progress = 0
        return self.imageVideo

    def scaleFocus(self, focus):
        self.scale_focus = focus
    
    def resize(self, w_box, h_box, pil_image): #参数是：要适应的窗口宽、高、Image.open后的图片  
        w, h = pil_image.size #获取图像的原始大小     
        '''
        # 保持图片本身比例
        f1 = 1.0*w_box/w   
        f2 = 1.0*h_box/h      
        factor = min([f1, f2])     
        width = int(w*factor)      
        height = int(h*factor)      
        return pil_image.resize((width, height), Image.ANTIALIAS)
        '''
        return pil_image.resize((w_box,h_box), Image.ANTIALIAS)

    # video progress value changed callback
    def scaleValueChanged(self, value):
        # get current scale value
        valueInt = int(self.scale.get() * 0.01 * self.frameCount)
        # seek frame
        self.videoCap.set(cv2.CAP_PROP_POS_FRAMES, valueInt)

        if(self.playing == False or self.scale_focus == True):
            img = self.getImageFromVideo()
            #cv2.waitKey(30)
            if(img != None):
                self.labelVideo.config(image = img)
                self.frameCurrent = valueInt

    def playVideo(self):
        if (False == self.playing):
            self.playing = True

    def pauseVideo(self):
        if(True == self.playing):
            self.playing = False

    def video_loop(self):
        if(self.playing == True and self.scale_focus == False):
            img = self.getImageFromVideo()
            #cv2.waitKey(30)
            if(img != None):
                self.labelVideo.config(image = img)
            # set current slide value
            self.scale.set(self.frameCurrent  / self.frameCount * 100)
        # call the video_loop function according to video frame rate
        self.root.after(self.frameRate, self.video_loop)

    def fun_timer(self):
        while (True):
            if (True == self.playing):
                img = self.getImgFromVideo(False)
                if (img != None):
                    self.labelVideo.config(image=img)
                    self.labelVideo.update()
            # video frame rate
            time.sleep(0.033)  # 1 / 30

    def change_schedule(self, i, all_schedule):
        self.canvas1.coords(self.fill_rec1, (5, 5, 6 + (self.now_schedule1[i] / all_schedule) * 400, 25))
        self.x1.set(str(round(self.now_schedule1[i] / all_schedule * 100, 2)) + '%')
        self.canvas2.coords(self.fill_rec2, (5, 5, 6 + (self.now_schedule2[i] / all_schedule) * 400, 25))
        self.x2.set(str(round(self.now_schedule2[i] / all_schedule * 100, 2)) + '%')
        self.canvas3.coords(self.fill_rec3, (5, 5, 6 + (self.now_schedule3[i] / all_schedule) * 400, 25))
        self.x3.set(str(round(self.now_schedule3[i] / all_schedule * 100, 2)) + '%')
        self.canvas4.coords(self.fill_rec4, (5, 5, 6 + (self.now_schedule4[i] / all_schedule) * 400, 25))
        self.x4.set(str(round(self.now_schedule4[i] / all_schedule * 100, 2)) + '%')
        self.canvas5.coords(self.fill_rec5, (5, 5, 6 + (self.now_schedule5[i] / all_schedule) * 400, 25))
        self.x5.set(str(round(self.now_schedule5[i] / all_schedule * 100, 2)) + '%')
        self.fm2.update()

    def update_timer(self):
        while (True):
            if (True == self.playing):
                self.progress = self.progress + 1
                time.sleep(0.4)
                self.change_schedule(self.progress, 99)
                if (self.progress == 15):
                    self.playing = False
                    self.progress = 0
    
def main():
    root_cav = tk.Tk() #Toplevel() image "pyimage42" doesn't exist
    chick = Chick_GUI(root_cav)
    root_cav.mainloop()
    chick.shutdown()

if __name__ == "__main__":
    main()
