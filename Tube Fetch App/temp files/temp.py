import tkinter as tk 
from tkinter import * 
from tkinter import ttk , filedialog, messagebox
from win32api import GetSystemMetrics
import tkinter.scrolledtext as st
from pytube import YouTube
from pytube import *

import os 
from PIL import Image

import time

def displayLoading(self, start: bool = False, stop : bool = False): 
        if start == True :
            self.loading_label.place(x=self.xpad*1.9,y=self.ypad*1.8+5, height=50) 
            update( 0) 
            # return True 
        
        if stop == True :
            self.loading_label.place_forget()  
            # return False 
        # return False 
        return 

def update(ind):
    global self 
    frame = self.loading_label.frames[ind]
    ind += 1
    if ind == self.loading_label.frameCnt:
        ind = 0
    self.loading_label.configure(image=frame)
    self.loading_label.after(100, update, ind)


def permission():
    global self 
    print("Toggle with 0 and 1")
    load = bool(input()) 

    if load :
        displayLoading(self, start=True) 
        
    if load == False:
        displayLoading(self, stop=True) 
    
    permission() 
    

width_max = GetSystemMetrics(0)
height_max = GetSystemMetrics(1)



self = tk.Tk() 
self.window_bg = "white"
self.xpad = width_max/4  # init xpad 
self.ypad = height_max/5



self.geometry("500x500") 
self.loading_label = tk.Label(self, text="loading here", bg=self.window_bg) 
self.loading_label.frameCnt = 6
self.loading_label.frames = [PhotoImage(file='loading_gif.gif',format = 'gif -index %i' %(i)) for i in range(self.loading_label.frameCnt)]
self.loading_label.place(x=self.xpad*1.9,y=self.ypad*1.9) 
# self.loading_label.place_forget() 

displayLoading(self, start=True)  
permission() 
self.mainloop() 

# print("I am out of mainloop()")
# time.sleep(3)
# print("Forget place")
# self.loading_label.place_forget()   
