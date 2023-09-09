from pytube import YouTube
from pytube import *
import sys 
from sys import * 
from tkinter import * 
import tkinter as tk 


class Downloader :
    
    _url = "https://youtu.be/G8ZfiO0hj5A?si=zsuAAG1G65ufwrJ-" 
    _filePath = "E:\\PROJECTS\\Tube Fetch App\\"
    _isTargetVideo = False 
    _isTargetAudio = False 
    _fileFormats = None 
    _selectedFile_itag = None 

    def __init__(self):
        self.createInstance() 
        
        # self.getter() 

        # self.displayAvailFormats()  

        # self.downloadFile() 

        return 

    def createInstance(self):
        try:
            self._fileFormats = YouTube(self._url)
        except Exception as e:
            print(e)
        else:
            # print("-- instance creation successfull !") 
            pass 

    def initComponents(self):
        self._url = ""
        self._filePath = ""
        self._isTargetAudio = False 
        self._isTargetVideo = False 
        self._fileFormats = None  
        self._selectedFile_itag = None 
        return 

    def getter(self):
        # self._url = input("Enter video url: ")
        # self._filePath = input("Enter file saving location: ") 
        
        self._isTargetVideo = True if input("Download Video ? (Y or N): ").lower() == "y" else False 

        self._isTargetAudio = True if input("Download Audio ? (Y or N): ").lower() == "y" else False 

        return 

    def displayAvailFormats(self):
        if self._isTargetVideo:
            self.displayVideoFormats()  
            
        if self._isTargetAudio:
            self.displayAudioFormats() 
             

    def displayVideoFormats(self): 
        print("Fetching all available video formats......",end="")
        videoItagList = self.fetchItagList(video=True) 
        print("Done!") 
        print("Available Video Resolutions".format(50)) 
        print("".format(50, "-"))

        for index, vid_itag in enumerate(videoItagList):
            print(f"{index+1} {self._fileFormats.streams.get_by_itag(vid_itag).resolution}          {int(self._fileFormats.streams.get_by_itag(vid_itag).filesize_mb)}MB")
        
        selectedVideoResolution = int(input("\nEnter your choice: ")) 
        self._selectedFile_itag = videoItagList[selectedVideoResolution-1]  
        print(f"--system_info.selectedFile_itag: {self._selectedFile_itag}\n")  # verified !
        return 


    def displayAudioFormats(self):
        print("Fetching all available audio formats......",end="")
        audioItagList = self.fetchItagList(audio=True) 
        print("Done!") 

        print("Available Audio Resolutions".format(50)) 
        print("".format(50, "-"))

        for index, aud_itag in enumerate(audioItagList):
            print(f"{index+1} {self._fileFormats.streams.get_by_itag(aud_itag).abr}          {int(self._fileFormats.streams.get_by_itag(aud_itag).filesize_mb)}MB")
        
        selectedAudioResolution = int(input("\nEnter your choice: ")) 
        self._selectedFile_itag = audioItagList[selectedAudioResolution-1] 
        print(f"--system_info.selectedFile_itag: {self._selectedFile_itag}\n")  # verified ! 
        return 

    def fetchItagList(self, video: bool = False, audio: bool = False):
        try:
            if video:
                return [vid.itag for vid in self._fileFormats.streams.filter(type="video", file_extension="mp4") if vid.is_progressive]

            if audio:
                return [vid.itag for vid in self._fileFormats.streams.filter(type="audio")] 
        except Exception as e:
            print(e) 


    def downloadFile(self): 
        print("Download started......") 
        self._fileFormats.streams.get_by_itag(self._selectedFile_itag).download(self._filePath) 
        print(f"{'Video downloaded successfully!' if self._isTargetVideo else ''}") 
        print(f"{'Audio downloaded successfully!' if self._isTargetAudio else ''}") 
        print(f"Location: {self._filePath+self._fileFormats.streams.get_by_itag(self._selectedFile_itag).title}") 
        print() 
        print("".format(50, "-"))


         


