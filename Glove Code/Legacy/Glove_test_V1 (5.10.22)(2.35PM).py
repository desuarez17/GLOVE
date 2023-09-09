# Import modules
# Attempt to import matplot
from ast import In
from cProfile import label
from tkinter import Frame

from black import main


try:
    import matplotlib
except ModuleNotFoundError as e:
    print("Missing matplotlib library!")
    raise e
# Attempt to import time
try:
    import time
except ModuleNotFoundError as e:
    print("Missing time library!")
    raise e
# Attempt to import pySerial
try:
    import serial
except ModuleNotFoundError as e:
    print("Missing pySerial library!")
    raise e
# Attempt to import numpy
try:
    import numpy as np
except ModuleNotFoundError as e:
    print("Missing numpy library!")
    raise e

# Attempt to import tkinter
try:
    import tkinter as tk
except ModuleNotFoundError as e:
    print("Missing tkinter library!")
    raise e

window = tk.Tk()
window.title('Glove Interface V1')
window.geometry('680x480')
Finger_frames = []
Slider_frames = []




#Creating DATA OBJECT
Max_default = 100
Min_default = 0
Max = np.array([Max_default,Max_default,Max_default,Max_default,Max_default])
Current = np.array([30,40,50,70,60]) #CHANGE TO EMPTY WHEN DONE TESTING
Min = np.array([Min_default,Min_default,Min_default,Min_default,Min_default])
DATA = [Max,Current,Min]

Colors = ["#0089ff","#6c42f5","#e80c0c","#10c756","#e88e10"]
Barwidth = 4
Slider = [Barwidth]
settings = [Colors,Slider]

#Header
tk.Label(window, text = "" ).grid(row = 0, column = 0)

Graph_frame = Frame(window,width=640,height=288)

def disp(DATA,settings):
    
    #Creates the frames for each finger slider and labels
    for F in range(0,5):
        #create Finger frame
        Fingers_FRAME = Frame(window,width=128,height=288)
        Fingers_FRAME.grid(row=1, column = F)
        Finger_frames.append(Fingers_FRAME)
        
        #Create Slider Sub-frame
        Slider_FRAME = Frame(Fingers_FRAME,width=64,height=288)
        Slider_FRAME.grid(row=0, column = 1, rowspan=3)
        Slider_frames.append(Slider_FRAME)

        #Populate frame
        #Labels
        tk.Label(Fingers_FRAME, text = "Max: " + str(DATA[0][F]) ).grid(row = 0, column = 0, sticky = 'e')
        tk.Label(Fingers_FRAME, text = "Current: " + str(DATA[1][F]) ).grid(row = 1, column = 0, sticky = 'e')
        tk.Label(Fingers_FRAME, text = "Min: " + str(DATA[2][F]) ).grid(row = 2, column = 0, sticky = 'e')
        #Slider
        slider(DATA,settings,Fingers_FRAME,F)



    
    #V NEEDS TO BE OUTSIDE DISP function V
    #Creates the status Label

    #Creates the COM PORT menu

    #Creates the Recalibrate Button

#Creates a slider with magic
def slider(DATA,settings,FRAME,F):
    z = (288-2)/(Max_default-Min_default)
    slider = tk.Canvas(FRAME,width=64,height=288)
    #Boxes
    slider.create_rectangle(2, 2+(100-DATA[0][F])*z, 64, 288-DATA[2][F]*z,outline="#000000")
    #Bars
    slider.create_rectangle(2, 288-DATA[1][F]*z - settings[1][0]/2, 64, 288-DATA[1][F]*z + settings[1][0]/2,outline="#000000",fill=settings[0][F])
    
    slider.grid(row = 0, column = 1, rowspan=3)

#def updatesliders(DATA,settings,FRAME,F):


# Ask for port
#port = input("Enter port for Arduino (ex: COM4): ")
port = "COM7" #for testing
arduino = serial.Serial(port, 9600, timeout=1)

#intialize Window
disp(DATA,settings)

buffer = np.array([0,0,0,0,0])

def mainloop():

    #print("going")
    
    #Takes ardino input and Decodes the Unicode bytes to make an array of each of the values
    RAWINPUT = arduino.readline()
    if len(RAWINPUT) == 17:
        DECODEDINPUT = str(RAWINPUT,'UTF-8').split()
        INPUTARR = np.array([int(DECODEDINPUT[0]),int(DECODEDINPUT[1]),int(DECODEDINPUT[2]),int(DECODEDINPUT[3]),int(DECODEDINPUT[4])])
        
        DATA[1] = RAWINPUT

        #check for change in value
        if (np.linalg.norm(INPUTARR-buffer)) == 0:
            INPUTdelta = INPUTARR-buffer

            for i in range(0,INPUTARR.size):
                #slider(50,100,INPUTARR[i],70,0,"#0089ff")
                print(INPUTARR)

            #buffer = INPUTARR
        
        
        
        #print(INPUTdelta)
    window.after(100,mainloop)


window.after(1000,mainloop)

window.mainloop()