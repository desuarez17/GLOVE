# Import modules
# Attempt to import matplot
from ast import In
from cProfile import label
from tkinter import Frame
from turtle import right

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
window.geometry('640x480')

# Sliding Bar Function -FN counts from 0->4-
def sliders(x,y,value,max,min,color):
    barsize = [20,80]
    barwidth = 5
    delta = max-min
    sigma = value -min

    slider = tk.Canvas(window,height=200,width=200)
    slider.create_rectangle(0, 0, 200, 200,outline="#000000")
    slider.create_rectangle(x, y, x+barsize[0], y+barsize[1],outline="#000000")
    slider.create_rectangle(x, y + delta - sigma - barwidth/2, x+barsize[0], y + delta - sigma + barwidth/2,fill=color)

    tk.Label(window, text = "Max:", bd=2).grid(row = 0, column = 0)
    tk.Label(window, text = "current:", bd=2).grid(row = 1, column = 0)
    tk.Label(window, text = "Min:", bd=2).grid(row = 2, column = 0)

    slider.grid(row = 0, column = 1)

Finger_frames = []

#Creating DATA OBJECT
Max_default = 100
Min_default = 0
Max = np.array([Max_default,Max_default,Max_default,Max_default,Max_default])
Current = np.array([30,40,50,70,60]) #CHANGE TO EMPTY WHEN DONE TESTING
Min = np.array([Min_default,Min_default,Min_default,Min_default,Min_default])
DATA = [Max,Current,Min]

Colors = ["#0089ff","#6c42f5","#e80c0c","#10c756","#e88e10"]
settings = [Colors]
Graph_frame = Frame(window,width=640,height=288)
def disp(DATA,settings):

    #tk.Label(Graph_frame, text = F).grid(row = 0, column = F)

    #Creates the frames for each finger slider and labels
    for F in range(0,5):
        #create frame
        Fingers_FRAME = Frame(window,width=128,height=288, bg=settings[0][F])
        Fingers_FRAME.grid(row=0, column = F)
        Finger_frames.append(Fingers_FRAME)

        #Populate frame
        #Labels
        tk.Label(Fingers_FRAME, text = "Max:" + str(DATA[0][F]), justify=right).grid(row = 0, column = 0)
        tk.Label(Fingers_FRAME, text = "Current:" + str(DATA[1][F]), justify=right).grid(row = 1, column = 0)
        tk.Label(Fingers_FRAME, text = "Min:" + str(DATA[2][F]), justify=right).grid(row = 2, column = 0)
        #Slider


    #Creates the status Label

    #Creates the COM PORT menu

    #Creates the Recalibrate Button


disp(DATA,settings)

# Ask for port
#port = input("Enter port for Arduino (ex: COM4): ")
port = "COM7" #for testing
arduino = serial.Serial(port, 9600, timeout=1)


#sliders(50,100,40,70,0,"#0089ff")

buffer = np.array([0,0,0,0,0])
def mainloop():
    
    print("going")
    
    #Takes ardino input and Decodes the Unicode bytes to make an array of each of the values
    RAWINPUT = arduino.readline()
    if len(RAWINPUT) == 17:
        DECODEDINPUT = str(RAWINPUT,'UTF-8').split()
        INPUTARR = np.array([int(DECODEDINPUT[0]),int(DECODEDINPUT[1]),int(DECODEDINPUT[2]),int(DECODEDINPUT[3]),int(DECODEDINPUT[4])])
        
        
        #check for change in value
        if (np.linalg.norm(INPUTARR-buffer)) == 0:
            INPUTdelta = INPUTARR-buffer

            for i in range(0,INPUTARR.size):
                #slider(50,100,INPUTARR[i],70,0,"#0089ff")
                print(INPUTARR)

            #buffer = INPUTARR
        
        
        
        #print(INPUTdelta)
    window.after(1,mainloop)

#window.after(1000,mainloop)

window.mainloop()