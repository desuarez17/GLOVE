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
Max_default = 60
Min_default = 10
Max = np.array([Max_default,Max_default,Max_default,Max_default,Max_default])
Current = np.array([30,40,50,70,60]) #CHANGE TO EMPTY WHEN DONE TESTING
Min = np.array([Min_default,Min_default,Min_default,Min_default,Min_default])
DATA = [Max,Current,Min]

#settings
Colors = ["#0089ff","#6c42f5","#e80c0c","#10c756","#e88e10"]
Barwidth = 4
Slider = [Barwidth]
settings = [Colors,Slider]

#Header
tk.Label(window, text = "" ).grid(row = 0, column = 0)

Graph_frame = Frame(window,width=640,height=288)
LabelLIST = []
def disp(DATA,settings):
    Graph_frame.grid(row = 1, column = 0)
    #Creates the frames for each finger slider and labels
    for F in range(0,5):
        #create Finger frame
        Fingers_FRAME = Frame(Graph_frame,width=128,height=288)
        Fingers_FRAME.grid(row=1, column = F)
        Finger_frames.append(Fingers_FRAME)
        
        #Create Slider Sub-frame
        Slider_FRAME = Frame(Fingers_FRAME,width=64,height=288)
        Slider_FRAME.grid(row=0, column = 1, rowspan=3)
        Slider_frames.append(Slider_FRAME)

        #Populate frame
        #Labels
        tk.Label(Fingers_FRAME, text = "Max: " + str(DATA[0][F]) ).grid(row = 0, column = 0, sticky = 'e')
        currentLabel = tk.Label(Fingers_FRAME, text = "Current: " + str(DATA[1][F]) ).grid(row = 1, column = 0, sticky = 'e')
        tk.Label(Fingers_FRAME, text = "Min: " + str(DATA[2][F]) ).grid(row = 2, column = 0, sticky = 'e')

        #make a list of current labels
        LabelLIST.append(currentLabel)
        #Slider
        slider(settings,Fingers_FRAME,DATA[2],F)
    

    #V NEEDS TO BE OUTSIDE DISP function V
    #Creates the status Label

    #Creates the COM PORT menu

    #Creates the Recalibrate Button

#Creates a slider with magic
barLIST = []
SliderLIST = []
def slider(settings,FRAME,min,F):
    L = 288-2
    pos = L - min[F]
    slider = tk.Canvas(FRAME,width=64,height=288)
    #Boxes
    box = slider.create_rectangle(2, 2, 64, 288,outline="#000000")
    #Bars
    bar = slider.create_rectangle(2,pos-settings[1][0]/2, 64,pos+settings[1][0]/2,outline="#000000",fill=settings[0][F])
    #add a thresh hold for up or down state

    SliderLIST.append(slider)
    barLIST.append(bar)
    slider.grid(row = 0, column = 1, rowspan=3)

#moves the sliders each frame
def updatesliders(DATA1,Buffer,stepsize):
    delta = DATA1-Buffer
    for i in range(0,5):
        #move bar
        SliderLIST[i].move(barLIST[i],0,-delta[i]*stepsize[i])
        #update label
        print(LabelLIST)
        #LabelLIST[i].label.text.set(text = "Current: " + str(DATA[1][i]))


#Takes ardino input and Decodes the Unicode bytes to make an array of each of the values
def decode(RAWINPUT):
    DECODEDINPUT = str(RAWINPUT,'UTF-8').split()
    INPUTARR = np.array([int(DECODEDINPUT[0]),int(DECODEDINPUT[1]),int(DECODEDINPUT[2]),int(DECODEDINPUT[3]),int(DECODEDINPUT[4])])
    return INPUTARR

# Ask for port
#port = input("Enter port for Arduino (ex: COM4): ")
#port = "COM7" #for testing
#arduino = serial.Serial(port, 9600, timeout=1)
print("Broke arduino")

#intialize Window
disp(DATA,settings)


buffer = []
buffer = np.array([0,0,0,0,0])

def mainloop():
    
    #print("going")
    
    buffer = DATA[1]
    RAWINPUT = arduino.readline()
    if len(RAWINPUT) == 17: #checks to see if out of range       
        DATA[1] = decode(RAWINPUT)

    #check for change in value
    #if (np.linalg.norm(DATA[1]-buffer)) == 0:
        #INPUTdelta = DATA[1]-buffer

        #updatesliders(INPUTdelta)
        
    print(DATA[1][0])
    stepsize = []
    for n in range(0,5):
        stepsize.append(((288-2)/(DATA[0][n]-DATA[2][n])))
    updatesliders(DATA[1],buffer,stepsize)
    window.after(10,mainloop)


window.after(1000,mainloop)

window.mainloop()