from tkinter import *
from tkinter import filedialog
import os
from pygame import mixer
from tkinter import ttk
from ttkthemes import themed_tk as tk


mixer.init()
root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
root.title('Let\'s Binge')
root.iconbitmap(r'iicon.ico')
root.configure()

lists = []

index = 0


def init_i_to_zero():
    global i
    i = 0


i = 0


def index_to_zero():
    global index
    index = 0


def increment_i():
    global i
    i += 1


def decrement_i():
    global i
    i -= 1


paused = False

playPhoto = PhotoImage(file='play.png')
pausePhoto = PhotoImage(file='pause.png')


def play_pause():
    global paused, inpause
    inpause = False
    if (paused == False):
        if (inpause == True):
            mixer.music.unpause()
            playPauseBtn.configure(image=playPhoto)
            paused = True
            inpause = False
        elif (inpause == False):
            mixer.music.load(filename)
            mixer.music.play()
            playPauseBtn.configure(image=playPhoto)
            paused = True
            inpause = True
    elif (paused == True):
        mixer.music.pause()
        playPauseBtn.configure(image=pausePhoto)
        paused = False
        inpause = True


def play_only():
    mixer.music.load(lists[i])
    mixer.music.play()


def forward():
    increment_i()
    play_only()


def backward():
    decrement_i()
    play_only()


def empty_playlist():
    global lists, playlist
    lists = []
    playlist = []


def new_refresh():
    global i
    mixer.music.stop()
    decrement_i()
    init_i_to_zero()
    while (i <= len(lists)):
        lists.pop(i)
        playlist.delete(i)
        i += 1
    init_i_to_zero()
    index_to_zero()



muted = False

mutePhoto = PhotoImage(file='mute.png')
speakerPhoto = PhotoImage(file='speaker.png')


def mute_music():
    global muted, mutePhoto, muteBtn
    if muted:
        muted = False
        mixer.music.set_volume(0.5)
        voicescale.set(50)
        muteBtn.configure(image=speakerPhoto)
    else:
        muted = True
        mixer.music.set_volume(0)
        voicescale.set(0)
        muteBtn.configure(image=mutePhoto)


def voice_scale(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


def playlist_songs(f):
    global index
    f = os.path.basename(f)
    playlist.insert(index, f)
    lists.insert(index, filename)
    increment_i()


def add_to_playlist():
    global filename
    filename = filedialog.askopenfilename()
    playlist_songs(filename)


def sub_from_playlist():
    mixer.music.stop()
    decrement_i()
    lists.pop(i)
    playlist.delete(i)


leftframe = Frame(root)
leftframe.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack(pady=50)

middleframe = Frame(rightframe)
middleframe.pack(pady=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

backPhoto = PhotoImage(file='back-back.png')
backwardBtn = ttk.Button(middleframe, image=backPhoto, command=backward)
backwardBtn.grid(row=5, column=0)

playPauseBtn = ttk.Button(middleframe, image=playPhoto, command=play_pause)
playPauseBtn.grid(row=5, column=1)

forwPhoto = PhotoImage(file='fast-forward.png')
forwardBtn = ttk.Button(middleframe, image=forwPhoto, command=forward)
forwardBtn.grid(row=5, column=2)

muteBtn = ttk.Button(bottomframe, image=speakerPhoto, command=mute_music)
muteBtn.pack(side=LEFT, pady=10)

voicescale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=voice_scale)
voicescale.set(50)
mixer.music.set_volume(0.5)
voicescale.pack(pady=10, side=LEFT, padx=10)

newPhoto = PhotoImage(file='refresh.png')
newplaylist = ttk.Button(bottomframe, image=newPhoto, command=new_refresh)
newplaylist.pack(side=LEFT, pady=10)

playlist = Listbox(leftframe)
playlist.pack(padx=10)

addPhoto = PhotoImage(file='plus.png')
addBtn = ttk.Button(leftframe, image=addPhoto, command=add_to_playlist)
addBtn.pack(side=LEFT, padx=5)

subPhoto = PhotoImage(file='minus.png')
subBtn = ttk.Button(leftframe, image=subPhoto, command=sub_from_playlist)
subBtn.pack(side=LEFT)

root.mainloop()
