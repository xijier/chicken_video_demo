# -*- coding: utf-8 -*-
"""
Created on Sat May 12 13:04:37 2018

@author: fengmaniu
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class Chick_GUI:
    imgDict = {}
    def __init__(self,cav):
        # initlize cav(first canvas)
        cav.title("智环AI识别")
        cav.geometry('1200x600')                 
        cav.resizable(width=False, height=False)
        # cav->fm1+fm2
        # fm1->fm11+fm12
        self.fm1 = tk.Frame(cav, width=700, bg="green")
        
        # fm11 显示视频
        self.fm11 = tk.Frame(self.fm1, width=700, height=450, bg="blue")
        tk.Label(self.fm11,text="视频",font=("Arial", 16)).\
        pack(expand=tk.YES,side=tk.TOP, pady=5, padx=5, anchor=tk.W)
        #image1 = Image.OPEN(r'test.jpg') # C:\\code\\intelligencering\\chicken_video_demo\\chicken_video_demo\\chicken_demo\\
        #image1 = ImageTk.PhotoImage(image1)
        #image1 = tk.PhotoImage(file="C:\\test.jpg") 只支持gif格式
        image1 = self.getImgWidget("C:\\test.jpg")
        tk.Label(self.fm11, image=image1, width=700,height=400).\
        pack(side=tk.TOP, padx=5, anchor=tk.W,expand=tk.YES)
        self.fm11.pack(pady=5,fill=tk.BOTH)
        
        # fm12 视频选项 开始 暂停 进度条
        self.fm12 = tk.Frame(self.fm1, width=700,height=150, bg="blue")
        tk.Button(self.fm12, text="开始", font=("Arial", 20)).pack(side=tk.LEFT, padx=5)
        tk.Button(self.fm12, text="暂停", font=("Arial", 20)).pack(side=tk.LEFT, padx=5)
        scale = tk.Scale(self.fm12, from_=0, to=100, orient=tk.HORIZONTAL, command=None) # command: define function
        scale.set(25)  # 设置初始值
        scale.pack(fill=tk.X, expand=1, side=tk.LEFT, padx=5, ipady=10)
        self.fm12.pack(pady=5,fill=tk.BOTH)
        self.fm1.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)
        
        # fm2
        self.fm2 = tk.Frame(cav,width=500,bg="red")
        # fm21 显示全部异常鸡
        self.fm21 = tk.Frame(self.fm2, width=500, height=400, bg="blue")
        tk.Label(self.fm21,text="全部异常鸡",font=("Arial", 16)).\
        pack(expand=tk.YES,side=tk.TOP, pady=5, padx=5, anchor=tk.W)
        number = tk.StringVar()
        numberChosen = ttk.Combobox(self.fm21, width=500, textvariable=number)
        numberChosen['values'] = ('热鸡', '饿鸡','渴鸡', '病鸡', '冷鸡')     # 设置下拉列表的值
        numberChosen.pack(expand=tk.YES,side=tk.TOP, pady=5, padx=5, anchor=tk.W)
        numberChosen.current(0)
        listbox_fm21=tk.Listbox(self.fm21, width=500)
        list_item = ["热鸡1 第一列 第一笼", 
                     "热鸡2 第二列 第二笼", 
                     "热鸡3 第三列 第三笼",
                     "热鸡4 第四列 第四笼",
                     "热鸡5 第五列 第五笼",
                     "热鸡6 第六列 第六笼",
                     "热鸡7 第七列 第七笼",
                     "热鸡1 第一列 第一笼", 
                     "热鸡2 第二列 第二笼", 
                     "热鸡3 第三列 第三笼",
                     "热鸡4 第四列 第四笼",
                     "热鸡5 第五列 第五笼"]
        for item in list_item:
            listbox_fm21.insert(tk.END, item)
        listbox_fm21.pack(expand=tk.YES,side=tk.TOP, pady=5, padx=5, anchor=tk.W)
        self.fm21.pack(pady=5,fill=tk.BOTH)
        self.fm21.pack(pady=5,fill=tk.BOTH)
        
        # fm22 视频某帧的当前异常鸡列表
        self.fm22 = tk.Frame(self.fm2, width=500,height=250, bg="blue")
        tk.Label(self.fm22,text="当前病鸡",font=("Arial", 16)).\
        pack(expand=tk.YES,side=tk.TOP, pady=5, padx=5, anchor=tk.W)
        listbox_fm22=tk.Listbox(self.fm22, width=500)
        list_item = ["热鸡1", "饿鸡1", "热鸡2", "病鸡1","病鸡2","病鸡3","饿鸡2"]         #控件的内容为1 2 3 4
        for item in list_item:
            listbox_fm22.insert(tk.END, item)
        listbox_fm22.pack(expand=tk.YES,side=tk.TOP, pady=5, padx=5, anchor=tk.W)
        self.fm22.pack(pady=5,fill=tk.BOTH)
        self.fm2.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH)

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
    
def main():
    root_cav = tk.Tk() #Toplevel() image "pyimage42" doesn't exist
    Chick_GUI(root_cav)
    root_cav.mainloop()

if __name__ == "__main__":
    main()
