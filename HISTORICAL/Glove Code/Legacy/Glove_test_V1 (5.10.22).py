# Import modules
# Attempt to import matplot
from ast import In


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

# Sliding Bar Function
def slider(x,y,value,max,min,color):
    size = [20,80]
    barwidth = 5
    delta = max-min
    sigma = value -min

    slider = tk.Canvas(window,height=200,width=200)
    slider.pack()
    slider.create_rectangle(x, y, x+size[0], y+size[1],outline="#000000")

    slider.create_rectangle(x, y + delta - sigma - barwidth/2, x+size[0], y + delta - sigma + barwidth/2,fill=color)




# Ask for port
#port = input("Enter port for Arduino (ex: COM4): ")
port = "COM7" #for testing
arduino = serial.Serial(port, 9600, timeout=1)


#slider(50,100,40,70,0,"#0089ff")


buffer = np.array([0,0,0,0,0])
while True:
    
    #time.sleep(0.5)
    
    #Takes ardino input and Decodes the Unicode bytes to make an array of each of the values
    RAWINPUT = arduino.readline()
    if len(RAWINPUT) == 17:
        DECODEDINPUT = str(RAWINPUT,'UTF-8').split()
        INPUTARR = np.array([int(DECODEDINPUT[0]),int(DECODEDINPUT[1]),int(DECODEDINPUT[2]),int(DECODEDINPUT[3]),int(DECODEDINPUT[4])])
        
        
        #check for change in value
        if (np.linalg.norm(INPUTARR-buffer)) != 0:
            INPUTdelta = INPUTARR-buffer

            for i in range(0,1):
                slider(50,100,INPUTARR[i],70,0,"#0089ff")

            buffer = INPUTARR
        
        
        
        #print(INPUTdelta)
    

window.mainloop()