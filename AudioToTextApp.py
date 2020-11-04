
import tkinter as tk
from tkinter import filedialog as fd
import tkinter.scrolledtext as tkst
import speech_recognition as sr
from pydub import AudioSegment


saveFile = None
r = sr.Recognizer()


# Open the pop menu to select a file and stores the file in the variable audioFile
def openFileReader():
    audioFile = fd.askopenfilename()
    with sr.AudioFile(audioFile) as source:  
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        textField.insert(tk.INSERT, text)  

#
def recordText():
    with sr.Microphone() as source:
         # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        text = r.recognize_google(audio_data)
        textField.insert(tk.INSERT, text)

# Copies the entire text fields text
def copyText():
    mainwindow.clipboard_clear()
    mainwindow.clipboard_append(textField.get('1.0', 'end-1c'))

# Clears the entire textfield
def clearText():
    textField.delete('1.0', 'end')

#Saves the text from the text field into the desired file
def saveTextAs():
    global saveFile
    saveFile = fd.asksaveasfile()
    saveFile.write(textField.get('1.0', 'end-1c'))
    saveFile.close()

#
def saveText():
    global saveFile
    if saveFile != None:
        saveFile.open()
        saveFile.write(textField.get('1.0', 'end-1c'))
        saveFile.close()
    else:
        #Problem to fix
        saveTextAs

    

#Loads the text contained in the open file into the textfield
def loadText():
    loadFile = fd.askopenfile()
    clearText()
    textField.insert(tk.INSERT, loadFile.read())   


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
audioframe = tk.Frame(mainwindow, bg="blue")
audioframe.place(relwidth=0.5, relheight=1, anchor='nw')

#Creates the frame for the text display and operations
textframe = tk.Frame(mainwindow, bg="green")
textframe.place(relx=0.5, relwidth=0.5, relheight=1)

# Adds a scrollable textfield
textField = tkst.ScrolledText(textframe)
textField.place(x= 5, y=5, height=500, relwidth=0.98)

#Button to call the copyText function
openFileButton = tk.Button(textframe, text="Copy text", font=30, command=copyText)
openFileButton.place(y=510,x=5, width=90)

#Button to call the clearText function
openFileButton = tk.Button(textframe, text="Clear text", font=30, command=clearText)
openFileButton.place(y=510,x=100, width=90)

#Button to call the openFileReader function
openFileButton = tk.Button(audioframe, text="Convert Wav file to text", font=30, command=openFileReader)
openFileButton.place(y=5, x=5)

#Button to call the openFileReader function
openFileButton = tk.Button(audioframe, text="Recording to text", font=30, command=recordText)
openFileButton.place(y=55, x=5)


#Adds the menu to the main window and open the application
mainwindow.config(menu=menubar)
mainwindow.mainloop()

