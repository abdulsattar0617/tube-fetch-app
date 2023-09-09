import tkinter as tk 
from tkinter import * 
from tkinter import ttk , filedialog, messagebox
from win32api import GetSystemMetrics
import tkinter.scrolledtext as st
from pytube import YouTube
from pytube import *
import validators 
import urllib.request 
import os 
from PIL import Image
import datetime
import threading 

class App(tk.Tk):

    window_font = "Verdana" 
    window_bg = "#000033"
    headingText = "Video Downloader"
    width_max = GetSystemMetrics(0)
    height_max = GetSystemMetrics(1)
    xpad = width_max/4  # init xpad 
    ypad = height_max/5
    appdata_image_path = "E:\\PROJECTS\\Tube Fetch App\\tubefetch.data\\images\\" 
    url_entry_placeholder_text = "Paste your url here"
    browsefolder_image_path = appdata_image_path + "download_folder_image.png"
    appLogo_image_path = appdata_image_path + "Tube-Fetch.png"
    download_location = "" 
    videoApi = None 
    loadingVisualsFlag = False 
    # off-white color hex: #FAF9F6


    def __init__(self):
        super().__init__()

        # load window size  
        self.geometry("1000x500+130+50")  
        self.state("zoomed")
        self.configure(bg=self.window_bg)
        self.title("") 
      
        # setting heading Label 
        self.headingLabel = tk.Label(text=self.headingText,justify="center", font=(self.window_font,"24"), bg=self.window_bg, fg="#FAF9F6")


        # print(self.xpad)  
        self.headingLabel.place(x=self.xpad+60, y=self.ypad, width=self.xpad*1.8)

        # adding entry frame 
        self.urlEntryFrame = tk.Frame(borderwidth=5, highlightbackground="white", highlightthickness=2, bg="#FAF9F6") 
        self.urlEntryFrame.place(x=self.xpad+60, y=self.ypad+60, width=self.xpad*1.8, height=self.ypad/2.5)

        # setting url entry 
        self.urlEntryValue = tk.Entry(justify="left", borderwidth=0, 
                                      highlightbackground="white",
                                      highlightthickness=0, 
                                      font=(self.window_font, "14") 
                                    ) 
        self.urlEntryValue.insert(0, self.url_entry_placeholder_text) 
        self.urlEntryValue.place(x=self.xpad+80, y=self.ypad+70, width=self.xpad*1, height=self.ypad/4) 

        # adding browse folder button
        self.browseFolder_image = tk.PhotoImage(file=self.browsefolder_image_path)

        self.browseFolder_button = tk.Button(image=self.browseFolder_image, command=self.browseFolder, width=50,font=(self.window_font, '16'), background="#FAF9F6")
        self.browseFolder_button["border"] = "0"
        self.browseFolder_button.place(x=self.xpad*2.30, y=self.ypad+70, width=50, height=40) 


        # adding download button to frame
        self.genDownloadLinks_button = tk.Button(text="Download →", fg="white", bg="#DA2C43", command=self.genDownloadLinks, font=(self.window_font,'16'))
        self.genDownloadLinks_button["border"] = "0"
        self.genDownloadLinks_button.place(x=self.xpad*2.5, y=self.ypad+70, width=155, height=40)  

    
        # adding video / audio drop down (ComboBox) 
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('TCombobox',
                                background="red", # pulling button
                                fieldbackground=self.window_bg, # text field bg color
                                
                                foreground="#DA2C43", # selected text color
                                darkcolor="#000066",  # selector color TODO - change color
                                selectbackground="Transparent", 
                                lightcolor="#000066"  # border TODO-change border color
                                )


        self.options = ["Video", "Audio"] 
        
        
        self.ff_dropDown = ttk.Combobox(values=self.options, justify='center',font=(self.window_font, "18"))   
        self.ff_dropDown.bind("<<ComboboxSelected>>", self.updateFields) 
        self.ff_dropDown.set("Video") 
        # self.ff_dropDown.place(x=self.xpad*2, y=self.ypad*2.25, width=self.xpad+self.xpad/2, height=self.ypad/3) 
        


        # adding text box -- link display board 
        self.linkDisplayBoard = st.ScrolledText(self, font = (self.window_font, "14"))  

        self.linkDisplayBoard.insert(tk.INSERT, "") 
        self.linkDisplayBoard.configure(border=0, borderwidth=2, bg=self.window_bg, highlightcolor="#000066", relief="groove", fg="#FAF9F6") 
        # self.linkDisplayBoard.place(x=self.xpad*2, y=self.ypad*2.58, width=self.xpad+self.xpad/2, height=self.ypad*1.5)

        # Making the text read only
        # self.linkDisplayBoard.configure(state ='disabled')   TODO- add security using it
        

    
        self.thumbnailCanva = tk.Canvas(self, width=self.xpad-self.xpad/6, height=self.ypad, bg=self.window_bg, highlightthickness=0)  
        self.bind("<Destroy>", self.on_destroy)
        # self.thumbnailCanva.place(x=self.xpad, y=self.ypad*2.25) 
        
        # adding app logo
        self.appLogoCanva = tk.Canvas(self, width= 332, height= 63, bg=self.window_bg, highlightthickness=0) 

        # placing logo image to canva 
        logo = tk.PhotoImage(file=self.appLogo_image_path) 
        self.appLogo_image = logo # prevent image garbage collected
        self.appLogoCanva.create_image(0,0, anchor=NW, image=self.appLogo_image) 
        self.appLogoCanva.bind("<Button-1>", self.resetComponents) 
        self.appLogoCanva.place(x=10, y=10) 
        

        # adding video title 
        self.videoTitle = tk.Text(font=(self.window_font, "14"),
                                  border=0,
                                  borderwidth=2,
                                  relief="flat",
                                  bg=self.window_bg, fg="#FAF9F6") 
        self.videoTitle.insert(tk.INSERT, "Copy the video's URL and insert it into the input field positioned at the page's upper section. Then, simply hit \"Enter\" or click on the \"Download\" button.")
        # self.videoTitle.place(x=self.xpad+2, y=self.ypad*3.275, width=self.xpad-self.xpad/6, height=self.ypad/1.6) 

        # adding duration label
        self.videoDurationLabel = tk.Label(text="Duration:", justify="center",font=(self.window_font, "12"), highlightcolor="red", borderwidth=2, relief="flat", fg="#FAF9F6", bg=self.window_bg) 
        # self.videoDurationLabel.place(x=self.xpad, y=self.ypad*3.9, width=self.xpad/2.4, height=self.ypad/4)

        # adding duration value entry 
        self.videoDurationValue = tk.Entry(justify="center", font=(self.window_font, "12"), borderwidth=2, relief="flat", bg=self.window_bg, fg="#FAF9F6") 
        # self.videoDurationValue.place(x=self.xpad+self.xpad/2.3, y=self.ypad*3.9, width=self.xpad/2.5, height=self.ypad/4)
        

        # loading label 
        self.loading_label = tk.Label(self, text="loading here", bg=self.window_bg) 
        self.loading_label.frameCnt = 6
        self.loading_label.frames = [PhotoImage(file=self.appdata_image_path+'loading_gif.gif',format = 'gif -index %i' %(i)) for i in range(self.loading_label.frameCnt)]
        self.loading_label.place(x=self.xpad*1.9,y=self.ypad*1.9) 
        self.loading_label.place_forget() 
        # self.displayLoading() 

    # reset left box

    # reset right box
    # reset components -- for reset button
    def resetComponents(self, event):
        # reset url
        self.urlEntryValue.delete(0, END) 
        self.urlEntryValue.insert(0, self.url_entry_placeholder_text)

        # change thumbnail image
        img = tk.PhotoImage(file=self.appdata_image_path+"DefaultThumbnail.png") 

        self.thumbnail_image = img # prevent image garbage collected
        self.thumbnailCanva.create_image(0,0, anchor=NW, image=self.thumbnail_image)

        # change video title to default title
        self.videoTitle.delete("1.0", "end") 
        self.videoTitle.insert("1.0","Download Your Favourite\nYoutube Videos\n\nWith Tube Fetch 🧡") 

        # change video duration to 'Time' 
        self.videoDurationValue.delete(0, END)
        self.videoDurationValue.insert(0, 'Ꝏ')

        # empty the link display board
        self.linkDisplayBoard.delete("1.0","end")
        self.linkDisplayBoard.insert("1.0", "Fed up with the never-ending search for the perfect software enabling effortless downloads of online videos or music? \n\nSearch no more! \n\nOur Tube Fetch video downloader provides a free solution, enabling you to effortlessly fetch videos or music with just one click!")
        return

    def loadRightBox(self):
        # load combo box (menu audio/video) 
        self.ff_dropDown.place(x=self.xpad*2, y=self.ypad*2.25, width=self.xpad+self.xpad/2, height=self.ypad/3)

        # loading link displaying board
        self.linkDisplayBoard.place(x=self.xpad*2, y=self.ypad*2.58, width=self.xpad+self.xpad/2, height=self.ypad*1.5)
        
        return True 

    def loadLeftBox(self):
        # load video thumbnail
        self.thumbnailCanva.place(x=self.xpad, y=self.ypad*2.25) 

        # load video title
        self.videoTitle.place(x=self.xpad+2, y=self.ypad*3.275, width=self.xpad-self.xpad/6, height=self.ypad/1.6)

        # load video duration label
        self.videoDurationLabel.place(x=self.xpad, y=self.ypad*3.9, width=self.xpad/2.4, height=self.ypad/4)

        # load video duration value 
        self.videoDurationValue.place(x=self.xpad+self.xpad/2.3, y=self.ypad*3.9, width=self.xpad/2.5, height=self.ypad/4)
        
        return True 

    def update(self, ind):
        frame = self.loading_label.frames[ind]
        ind += 1
        if ind == self.loading_label.frameCnt:
            ind = 0
        self.loading_label.configure(image=frame)
        self.loading_label.after(100, self.update, ind)

    def displayLoading(self, start: bool = False, stop : bool = False): 
        if start == True :
            self.loading_label.place(x=self.xpad*1.9,y=self.ypad*1.8+5, height=50) 
            self.update(0) 
            # return True 
        
        if stop == True :
            self.loading_label.place_forget()  
            # return False 
        # return False 
        return 

    # TODO - implement method toggleLoadingVisuals() 
    # --Not working, correct it
    def toggleLoadingVisuals(self):
        if self.loadingVisualsFlag :
            self.displayLoading(start=True) 
        
        if self.loadingVisualsFlag == False:
            self.displayLoading(stop=True) 
        
        self.toggleLoadingVisuals() 
        

    def displayLinks(self):
        
        # load ff_dropdown (video/audio) menu & link display board 
        self.loadRightBox() 

        if self.ff_dropDown.get().lower() == self.options[0].lower(): # for video 
            # print(self.ff_dropDown.get()) 
            self.displayVideoLinks() 
            return

        if self.ff_dropDown.get().lower() == self.options[1].lower(): # for audio
            # print(self.ff_dropDown.get()) 
            self.displayAudioLinks() 
            return 
        return 
        
    def on_destroy(self, even):
        # delete video thumbnail from local storage
        if os.path.isfile(self.appdata_image_path+"VideoThumb.png"):
            os.remove(self.appdata_image_path+"VideoThumb.png")


    # text box size: 
    # x=self.xpad*2, y=self.ypad*2.58, width=self.xpad+self.xpad/2, height=self.ypad*1.5

    def validateFields(self):
        if not validators.url(self.urlEntryValue.get()):
            # print("Enter url first") 
            return False 
        
        if self.download_location == "":  # TODO correct file finding location
            self.browseFolder()

        if self.urlEntryValue.get() == self.url_entry_placeholder_text:
            return False 
    
        if self.urlEntryValue.get() == "": 
            return False 


        
        return True 


    def displayVideoLinks(self):
        # self.displayLoading(start=True) 

        video_itag_list = self.fetchItagList(video=True) 
        self.linkDisplayBoard.delete("1.0","end") 
        # self.linkDisplayBoard.bind("<Configure>", App.reset_tabs) 
        # print(video_itag_list) 
        for i in video_itag_list:
            video = self.videoApi.streams.get_by_itag(i) 


            item = "\n   {res}.mp4 \t\t{size}MB".format(res=video.resolution[:-1], size=int(video.filesize_mb)) 
            self.linkDisplayBoard.insert("end", item + "\t        \n") 
            button = tk.Button(self.linkDisplayBoard, text="⭳ Download", padx=2, pady=2,
                            cursor="left_ptr",
                            bd=1, highlightthickness=0,
                            command = lambda tag= i: self.download_file(tag),   
                            borderwidth=2 , 
                            highlightcolor="red" ,
                            font=(self.window_font, "14"),
                            relief="flat",
                            bg="white" ,
                            fg="#DA2C43"

                        )            
                          
            self.linkDisplayBoard.window_create("end-2c", window=button)  
            self.linkDisplayBoard.insert("end","------------------------------------------------------")

    def download_file(self, itag):      
        # print(itag)  

        # self.videoApi.streams.get_by_itag(itag).download(self.download_location)  
        downloadTaskThread = threading.Thread(target=self.startDownload, args=(itag,))
        downloadTaskThread.start() 
        # print("Download started......") 
        messagebox.showinfo("Tube Fetch","Download Started !") 
        
        # downloadTaskThread.join()
        # messagebox.showinfo("Tube Fetch","Download Completed !")
        return True 

    def startDownload(self, itagValue):
        YouTube(self.urlEntryValue.get()).streams.get_by_itag(itagValue).download(self.download_location) 




    def fetchItagList(self, video: bool = False, audio: bool = False):
        try:
            if video:
                return [vid.itag for vid in self.videoApi.streams.filter(type="video", file_extension="mp4") if vid.is_progressive]

            if audio:
                return [vid.itag for vid in self.videoApi.streams.filter(type="audio")] 
        except Exception as e:
            print(e) 

    def displayAudioLinks(self):
        # self.displayLoading(start=True)

        audio_itag_list = self.fetchItagList(audio=True) 
        self.linkDisplayBoard.delete("1.0","end") 

        for i in audio_itag_list:
            audio = self.videoApi.streams.get_by_itag(i) 

            item = "\n   {abr} \t\t{size}MB".format(abr=audio.abr, size=int(audio.filesize_mb)) 

            self.linkDisplayBoard.insert("end", item + "\t        \n")
            button = tk.Button(self.linkDisplayBoard, text="⭳ Download", padx=2, pady=2,
                            cursor="left_ptr",
                            bd=1, highlightthickness=0,
                            command = lambda tag= i: self.download_file(tag), 
                            borderwidth=2 , 
                            highlightcolor="red" ,
                            font=(self.window_font, "14"),
                            relief="flat",
                            bg="white" ,
                            fg="#DA2C43"

                        )                          
            self.linkDisplayBoard.window_create("end-2c", window=button)  
            self.linkDisplayBoard.insert("end","------------------------------------------------------")

    def browseFolder(self):
        self.download_location = filedialog.askdirectory() + "/"
        # print(self.download_location) 

        return 

    
    # initialization for youtube object
    # def initVideoApi(self):
    #     self.videoApi = YouTube(self.urlEntryValue.get()) 
    #     return 
        

    def genDownloadLinks(self):     # button clicks
        # print("video link generation started.....") 


        if self.validateFields() :
            try:
                # TODO - start loading visuals here
                # loadingVisualsThread = threading.Thread(target=self.displayLoading, args=(True, False)) 
                # loadingVisualsThread.start()

                # toggleLoadingVisualsThread = threading.Thread(target=self.toggleLoadingVisuals, args=())
                # toggleLoadingVisualsThread.start()
                
                # self.loadingVisualsFlag = True

                # Thread 'VideoApiThread' initializes the Youtube object
                self.videoApi = YouTube(self.urlEntryValue.get())  
                # VideoApiThread = threading.Thread(target=self.initVideoApi, args=()) 
                # VideoApiThread.start() 
                # VideoApiThread.join() 


                # loading the left box = thumbnail + title + duration (label + value)
                # self.loadLeftBox()  
                # thread for above task
                loadLeftBoxThread = threading.Thread(target=self.loadLeftBox, args=()) 
                loadLeftBoxThread.start() 

                # load data for left box = thumbnail + title + duration (label + value)
                # self.loadVideoBoard() 
                loadVideoBoardThread = threading.Thread(target=self.loadVideoBoard(), args=()) 
                loadVideoBoardThread.start() 

                # load data for link display board (video download links) 
                # self.displayLinks() 
                displayLinksThread = threading.Thread(target=self.displayLinks(), args=())
                displayLinksThread.start() 

                # self.loadingVisualsFlag = False 

            except Exception as e:
                print(e)
            else:
                # print("video link generation ...Done !")  
                
                # TODO - stop the loading visuals here
                # self.displayLoading(True, False) 
                # self.displayLoading(start=False, stop=True)
                # pass 
                pass 

        else:
            print("enter fields properly !") 

    
    def loadVideoBoard(self):
        # load left box -- video thumbnail + video title + video duration with label        
        # self.loadLeftBox() 

        # load video title
        self.videoTitle.delete("1.0", "end") 
        self.videoTitle.insert("1.0", self.videoApi.title) 

        # load video thumbnail
        # self.loadVideoThumbnail() 
        loadVideoThmbThread = threading.Thread(target=self.loadVideoThumbnail, args=())
        loadVideoThmbThread.start() 

        # TODO- load duration of video
        
        # count duration of video
        # video min = (video.length/60)*60  --> gives total video seconds
        video_time = datetime.timedelta(seconds=round(self.videoApi.length/60)*60) 

        # update video duration 
        self.videoDurationValue.delete(0, END)
        self.videoDurationValue.insert(0, video_time) 

        return 
        
      
    def loadVideoThumbnail(self):
        # thumbnail size: width=self.xpad-self.xpad/6, height=self.ypad
        # 1. download thumb
        # 2. resize it 
        # 3. delete old thumb
        # 4. place new resized thumb in self.thumbnailCanva

        # removing last thumbnail  
        if os.path.isfile(self.appdata_image_path+"VideoThumb.png"):
            os.remove(self.appdata_image_path+"VideoThumb.png")

        # print("---controlUnder --> loadVideoThumbnail") # verification only

        # downloading thumbnail image
        urllib.request.urlretrieve(self.videoApi.thumbnail_url, 
                                   self.appdata_image_path+"tempFileVideoThumb.png")
        
        # resizing the thumbnail image 
        basewidth = int(self.xpad-self.xpad/6) 
        img = Image.open(self.appdata_image_path+"tempFileVideoThumb.png")
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
        img.save(self.appdata_image_path+"VideoThumb.png")
        # print("resizing....Done !", basewidth, hsize)

        # deleting old thumbnail image
        os.remove(self.appdata_image_path+"tempFileVideoThumb.png") 
        # print("removing .........Done!")

        # placing thumbnail image to canva 
        img = tk.PhotoImage(file=self.appdata_image_path+"VideoThumb.png") 
        self.thumbnail_image = img # prevent image garbage collected
        self.thumbnailCanva.create_image(0,0, anchor=NW, image=self.thumbnail_image) 

        # print("Done loadVideoThumbnail() --passed")
        return 

    def updateFields(self, event): 
        if self.validateFields():
            self.displayLinks() 
        

