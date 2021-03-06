import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import tkinter.scrolledtext as tkst
import speech_recognition as sr
from pydub import AudioSegment
from tkinter import ttk
import time

saveFile = None
r = sr.Recognizer()
mic_index = 0
recording = 0
recordingLength = 0

# Open the pop menu to select a file and stores the file in the variable audioFile
def openFileReader():
    audioFile = fd.askopenfilename(filetypes=(("Wav files","*.wav"),("All files","*.*")))
    try:        
        with sr.AudioFile(audioFile) as source:  
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            textField.insert(tk.INSERT, (text + "\n"))
    except:
        print("No suitable file selected")

#updates the selected recoding length to the selected value in the connected combobox
def updateLen(test):
    global recordingLength
    recordingLength = int(length_combo.get())

# Records the audio for the selected duration and converts it to text 
def recordTimedText():
    global mic_index
    global recordingLength
    print("Recognizing...")
    # convert speech to text
    try:
        with sr.Microphone(device_index=mic_index) as source:
             r.adjust_for_ambient_noise(source)
             audio = r.record(source, duration=recordingLength)         
             text = r.recognize_google(audio)
             textField.insert(tk.INSERT, text + ". \n")
    except:
        messageNoText()

#Records the audio as longer as there is no pause longer than 1 second and converts it to text 
def recordText():
    global mic_index
    print("Recognizing...")
    # convert speech to text
    try:
        with sr.Microphone(device_index=mic_index) as source:         
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            textField.insert(tk.INSERT, text + ". \n")
    except:
        messageNoText()

#Create a popup box saying that no text was recognized in the audio clip 
def messageNoText():
    print("test")
    tk.messagebox.showerror(title="No text recognized", message="There was no spoken text recognized in the recording")

# Copies the entire text fields text
def copyText():
    mainwindow.clipboard_clear()
    mainwindow.clipboard_append(textField.get('1.0', 'end-1c'))
    tk.messagebox.showinfo(title="Text copied", message="Copied the entire text to the clipboard")

# Clears the entire textfield
def clearText():
    confirmation = tk.messagebox.askquestion(title="Delete text confirmation", message="Are you sure you want to delete the text?")
    if confirmation == "yes":
        textField.delete('1.0', 'end')

#Saves the text from the text field into the desired file
def saveTextAs():
    global saveFile
    tempFile = fd.asksaveasfile(filetypes=(("Text files","*.txt"),("All files","*.*")) , defaultextension=".txt")
    if tempFile != None:
        saveFile = tempFile
        saveFile.write(textField.get('1.0', 'end-1c'))
        saveFile.close()

#Saves the text to the current save file or asks to select a file to save to.
def saveText():
    global saveFile
    if saveFile != None:
        saveFile = open(saveFile.name, "w")
        saveFile.write(textField.get('1.0', 'end-1c'))
        saveFile.close()
    else:
        #Problem to fix
        saveTextAs() 

#Loads the text contained in the open file into the textfield
def loadText():
    loadFile = fd.askopenfile(filetypes=(("Text files","*.txt"),("All files","*.*")))
    if loadFile != None:
        clearText()
        textField.insert(tk.INSERT, loadFile.read())
    
#updates the selected microphone to the selected value in the connected combobox
def updateMic(test):
    global mic_index
    mic_index = mic_combo.current()

# Creates the main window and sets the dimensions for the interface
mainwindow = tk.Tk()
windowWidth = 800
windowHeight = 600
mainwindow.geometry(str(windowWidth) + "x" + str(windowHeight))
mainwindow.minsize(windowWidth, windowHeight)

#Sets up the main menu
menubar = tk.Menu(mainwindow)
mainmenu = tk.Menu(menubar, tearoff=0)
mainmenu.add_command(label="Load text", command=loadText)
mainmenu.add_command(label="Save text", command=saveText)
mainmenu.add_command(label="Save text as", command=saveTextAs)
mainmenu.add_command(label="Exit", command=mainwindow.quit)
menubar.add_cascade(label="File", menu=mainmenu)

#Creates a frame for the audio related operations
audioframe = tk.Frame(mainwindow, bg="lightgrey")
audioframe.place(relwidth=0.5, relheight=1, anchor='nw')

#Creates the frame for the text display and operations
textframe = tk.Frame(mainwindow, bg="lightgrey")
textframe.place(relx=0.5, relwidth=0.5, relheight=1)

# Adds a scrollable textfield
textField = tkst.ScrolledText(textframe)
textField.place(x= 5, y=5, height=500, relwidth=0.98)

#Button to call the copyText function
copyTextButton = tk.Button(textframe, text="Copy text", font=30, command=copyText)
copyTextButton.place(y=510,x=5, width=90)

#Button to call the clearText function
clearTextButton = tk.Button(textframe, text="Clear text", font=30, command=clearText)
clearTextButton.place(y=510,x=100, width=90)

#Button to call the openFileReader function
openFileButton = tk.Button(audioframe, text="Convert Wav file to text", font=30, command=openFileReader)
openFileButton.place(y=5, x=5)

#Button to call the openFileReader function
recordButton = tk.Button(audioframe, text="Start Timed Recording", font=30, command=recordTimedText)
recordButton.place(y=145, x=5)

#Button to call the openFileReader function
recordButton = tk.Button(audioframe, text="Start Recording", font=30, command=recordText)
recordButton.place(y=190, x=5)

#Creates the combox to allow for my microphone selection
mic_list = sr.Microphone.list_microphone_names()
mic_combo = ttk.Combobox(audioframe, values=mic_list) 
mic_combo.current(0)
mic_combo.place(y=55, x=145, width=250)
mic_combo.bind('<<ComboboxSelected>>', updateMic)

durationLabel = tk.Label(audioframe, font=30, text="Duration of recording (in sec): ", bg="lightgrey")
durationLabel.place(y=105, x=5)

durationLabel = tk.Label(audioframe, font=30, text="Recording device: ", bg="lightgrey")
durationLabel.place(y=55, x=5)

#Creates the combox to allow for duration of recording selection
length_list = [5, 10, 30, 60, 120, 300, 600]
length_combo = ttk.Combobox(audioframe, values=length_list)
length_combo.current(0)
length_combo.place(y=105, x=245, width=150)
length_combo.bind('<<ComboboxSelected>>', updateLen)

#Adds the menu to the main window and open the application
mainwindow.config(menu=menubar)
mainwindow.mainloop()