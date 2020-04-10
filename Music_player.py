from tkinter import *
from tkinter import ttk
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
import os
import threading
import time
from mutagen.mp3 import MP3
from ttkthemes import themed_tk as tk



#this is a newly added line
root = tk.ThemedTk()
root.get_themes()                 # Returns a list of all themes that can be set
root.set_theme("radiance")
menubar =Menu(root)
root.config(menu=menubar)

playlist =[]
LARGE_FONT = ("Verdana",12)

def openfile():
    global filename
    filename= filedialog.askopenfilename()
    add_to_playlist(filename)

def add_to_playlist(filename):
    index = 0
    playlist.insert(index,filename)
    f =os.path.basename(filename)
    Lb.insert(index,f)
    index +=1

def about_us():
    tkinter.messagebox.showinfo('Music','Music is my world')
#sub menu
statusbar =Label(root,text = "Welcome to Music",relief = SUNKEN,anchor ="w",font =LARGE_FONT)
statusbar.pack(side =BOTTOM,fill =X)

leftframe = Frame(root)
rightframe = Frame(root)
leftframe.pack(side =LEFT)
rightframe.pack()

Lb= Listbox(leftframe)
Lb.pack()

def deletefun():
    selected_song = Lb.curselection()
    selected_song = int(selected_song[0])
    Lb.delete(selected_song)
    playlist.pop(selected_song)



add = ttk.Button(leftframe,text =" +ADD",command =openfile)
delete =ttk.Button(leftframe,text ="-DELETE",command=deletefun)
add.pack(side =LEFT,padx=10,pady=10)
delete.pack(pady=10)

topframe =Frame(rightframe)
middleframe =Frame(rightframe)
bottomframe =Frame(rightframe)

submenu = Menu(menubar,tearoff =0)
menubar.add_cascade(label="File",menu=submenu)
submenu.add_command(label ="Open",command =openfile)
submenu.add_command(label ="Exit",command =root.destroy)
submenu = Menu(menubar,tearoff =0)
menubar.add_cascade(label ="Help",menu=submenu)
submenu.add_command(label ="About us",command = about_us)

mixer.init()
root.title("Music")
root.iconbitmap("music_player_t2K_icon.ico")
root.geometry('650x550')
text = Label(topframe,text="Let's make some noise")
text.pack(pady=10)

lengthlabel =Label(topframe,text ="Total length -00:00",font=LARGE_FONT)
lengthlabel.pack(pady=10)

currentlabel =Label(topframe,text ="Current length -00:00",relief =GROOVE)
currentlabel.pack(pady=10)

photo = PhotoImage(file="play.png")
photo1 = PhotoImage(file="pause-button.png")
photo2 = PhotoImage(file ="rounded-pause-button.png")
photo3 = PhotoImage(file ="rewind-button.png")
photovol =PhotoImage(file ="icon.png")
photomut =PhotoImage(file ="mute-button.png")



def show_details(play_song):
    text['text'] = "playing "+os.path.basename(play_song)
    filedata =os.path.splitext(play_song)
    if filedata[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else :
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    mins,secs =divmod(total_length,60)
    mins =round(mins)
    secs =round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text'] = "Total length is "+"-"+timeformat
    print(mins,secs)
    t1= threading.Thread(target=start_count,args =(total_length,))
    t1.start()

def start_count(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            #paused = TRUE
            continue
        else:
            mins,secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentlabel['text'] = "Current time  is " + "-" + timeformat
            time.sleep(1)
            t = t-1
            #paused =FALSE

def play_btn():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = " World is safely Rescued!"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = Lb.curselection()
            selected_song =int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text']="Enjoy the Music! -" + play_it
            show_details(play_it)
            paused = FALSE
        except:
            tkinter.messagebox.showerror('Music', 'Select the file first')

def stop_btn():
    mixer.music.stop()
    statusbar['text'] = "End of World -" +"Last wishful Music was:" +filename

paused = FALSE
def pause_btn():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music stopped! - Rescue the World!"

def rewind_btn():
    play_btn()
    statusbar['text'] = "Music is rewinded!"



def set_vol(val):
    volume = eval(val)/100
    mixer.music.set_volume(volume)

muted = FALSE
def mute ():
    global muted
    if muted:
        mixer.music.set_volume(0.5)
        btn4.configure(image = photovol)
        scale.set(50)
        muted =FALSE
    else:
        mixer.music.set_volume(0)
        btn4.configure(image=photomut)
        scale.set(0)
        muted = TRUE



btn = ttk.Button(middleframe,image = photo,command = play_btn)
btn1 =ttk.Button(middleframe,image = photo1,command = stop_btn)
btn2 = ttk.Button(middleframe,image = photo2,command = pause_btn)
scale = ttk.Scale(bottomframe,from_=0,to=100,orient =HORIZONTAL,command= set_vol)
scale.set(50)
mixer.music.set_volume(0.5)
topframe.pack()
middleframe.pack()
btn.pack(side =LEFT,padx=10)
btn1.pack(side =LEFT,padx=10)
btn2.pack(side =LEFT,padx=10)
btn3 = ttk.Button(bottomframe,image = photo3,command = rewind_btn)




btn4 = ttk.Button(bottomframe,image = photovol,command = mute)
btn3.pack(side =RIGHT,padx=10,pady=10)


btn4.pack(side =LEFT,padx=10,pady=10)
scale.pack(pady=10)

bottomframe.pack()

def stop_music():
    mixer.music.stop()

def on_close():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_close)
#root.protocol("WM MAXIMIZE WINDOW",on_close)
root.resizable(0,0)
#leftframe.pack(side =LEFT)

root.mainloop()
