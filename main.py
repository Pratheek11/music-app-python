from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import os
from mutagen.mp3 import MP3
from pygame import mixer
from tkinter import ttk
from ttkthemes import themed_tk as tk


mixer.init()

root = tk.ThemedTk()
root.get_themes()

root.set_theme("radiance")

#header = Label(root, text='Select songs by your MoOd', relief=SUNKEN)
#header.pack(side=TOP, fill=X)

statusbar = ttk.Label(root, text='Welcome, Let\'s Binge', anchor=W, relief=SUNKEN)
statusbar.pack(side=BOTTOM, fill=X)


playlist = []

# Menu and Sub bar functions
def exit_player():
    mixer.stop()
    exit(0)


def show_details(s):
    global a, total_length, mins, secs, timeformat, fileData

    fileData = os.path.splitext(s)

    if fileData[1] == '.mp3' :
        audio = MP3(s)
        total_length = audio.info.length
    else:
        a = mixer.Sound(s)
        total_length = a.get_length()


    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total length " + '-' + timeformat


def open_files():
    global  filename
    filename = filedialog.askopenfilename()
    addToPl(filename)

def addToPl(f):
    f = os.path.basename(f)
    index = 0
    lb.insert(index, f)
    playlist.insert(index, filename)
    index += 1


def about_us():
    tkinter.messagebox.showinfo('About Developer', 'Naah!! Thank Me Later❤')


def delete_files():
    mixer.music.stop()
    selected_song = lb.curselection()
    selected_song = int(selected_song[0])
    lb.delete(selected_song)
    playlist.pop(selected_song)
    statusbar['text'] = 'Welcome, Let\'s Binge'


# Tool Bar and SubMenu
menubar = Menu(root)
root.config(menu=menubar)

subbar = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=subbar)
subbar.add_command(label='Open', command=open_files)
subbar.add_command(label='Exit', command=exit_player)

subbar = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=subbar)
subbar.add_command(label='About Us', command=about_us)

# Title and Icon
root.title('Let\'s Binge')
root.geometry('650x300')
root.iconbitmap(r'iicon.ico')
root.configure()

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=5)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack(pady=10)

middleframe = Frame(rightframe, border=0)
middleframe.pack(padx=5, pady=10)

bottomframe = Frame(rightframe, border=0)
bottomframe.pack(pady=10)


lengthlabel = ttk.Label(topframe, text='Total time - 00:00')
lengthlabel.pack(pady=5)

#currentlabel = ttk.Label(topframe, text='Current time - 00:00', command=currentTime)
#currentlabel.pack(pady=5)

lb = Listbox(leftframe)
lb.pack(padx=10)

addBtn = ttk.Button(leftframe, text=' + ', command=open_files)
addBtn.pack(side=LEFT, padx=10)

subBtn = ttk.Button(leftframe, text=' - ', command=delete_files)
subBtn.pack(side=LEFT)

global i
i = 0

# Play, Pause, Stop functions
def play_music():

    global play_it
    global paused
    try:
       selected_song = lb.curselection()
       selected_song = int(selected_song[0])
       play_it = playlist[selected_song]
       mixer.music.load(play_it)
       mixer.music.play()
       statusbar['text'] = 'Playing Music - ' + os.path.basename(play_it)
       show_details(play_it)
    #except IndexError:
        #tkinter.messagebox.showerror('File not Selected', 'Please select a file before playing')
    finally:

        while i<=len(playlist):
            mixer.music.load(playlist[i])
            mixer.music.play()
            statusbar['text'] = 'Playing Music - ' + os.path.basename(playlist[i])
            show_details(playlist[i])
            i += 1


paused = False


def pause_music():
    global paused
    if (paused == True):
        paused = False
        mixer.music.unpause()
        statusbar['text'] = 'Playing Music - ' + os.path.basename(play_it)
    elif (paused == False):
        paused = True
        mixer.music.pause()
        statusbar['text'] = 'Paused Music - ' + os.path.basename(play_it)


def stop_music():
    mixer.music.stop()
    statusbar['text'] = 'Music Stopped '


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


muted = False

mutePhoto = PhotoImage(file='mute.png')
speakerPhoto = PhotoImage(file='speaker.png')


def mute_music():
    global muted, unmutePhoto, mutePhoto, muteBtn
    if muted:
        muted = False
        mixer.music.set_volume(0.5)
        scale.set(50)
        muteBtn.configure(image=speakerPhoto)
        statusbar['text'] = 'Playing Music - ' + os.path.basename(play_it)
    else:
        muted = True
        mixer.music.set_volume(0)
        scale.set(0)
        muteBtn.configure(image=mutePhoto)
        statusbar['text'] = 'Muted Music - ' + os.path.basename(play_it)


# Button Functions
playPhoto = PhotoImage(file='play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=5, pady=10)

pausePhoto = PhotoImage(file='pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=1, padx=10, pady=10)

stopPhoto = PhotoImage(file='stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=2, padx=10, pady=10)

backwardBtn = ttk.Button(middleframe,text=' << ')
backwardBtn.grid(row=1, column=0, pady=10)

forwardBtn = ttk.Button(middleframe, text=' >> ')
forwardBtn.grid(row=1, column=2, pady=10)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)
mixer.music.set_volume(0.5)
scale.pack(pady=10, side=LEFT, padx=10)

muteBtn = ttk.Button(middleframe, image=speakerPhoto, command=mute_music)
muteBtn.grid(row=1, column=1, pady=10)


root.protocol('WM_DELETE_WINDOW', exit_player)

# Display constant
root.mainloop()
