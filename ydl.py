import youtube_dl
import os

file = './song.mp3'

def ydl(url):
    if os.path.isfile(file):
        os.remove(file)

    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192'
        }],
        'outtmpl':'song.mp3',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])