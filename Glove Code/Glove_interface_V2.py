#1st line!

from tkinter import *
from tkinter import Frame
import random
from webbrowser import BackgroundBrowser
import serial
import numpy as np


#Creating fax max and min
Max_default = 60
Min_default = 10
Max = np.array([Max_default,Max_default,Max_default,Max_default,Max_default])
Current = np.array([0.5,0.7,0.2,0.3,0.6]) #CHANGE ALL TO 0.5 WHEN DONE TESTING
Min = np.array([Min_default,Min_default,Min_default,Min_default,Min_default])


#settings
BarColors = ["#0089ff","#6c42f5","#e80c0c","#10c756","#e88e10"]
Background =  "#303134"
Txt = "#FFFFFF"
Colors = [Background,Txt,BarColors]

Barwidth = 4
SliderMax = 300
Slider = [Barwidth,Max,Min]

Port = "COM7"

settings = [Colors,Slider,Port]
FingerCount = 5


#Takes ardino input and Decodes the Unicode bytes to make an array of each of the values
def decode(RAWINPUT):
    DECODEDINPUT = str(RAWINPUT,'UTF-8').split()
    INPUTARR = np.array([int(DECODEDINPUT[0]),int(DECODEDINPUT[1]),int(DECODEDINPUT[2]),int(DECODEDINPUT[3]),int(DECODEDINPUT[4])])
    return INPUTARR

#rescale data for slider
def rescale(SliderMax,Value):
    #Value is between 0 and 1
    #SliderMax is the length of slider in pixels
    return SliderMax*(1-Value)

def Calibrate ():
    print("get joshed")

class MAIN():
    def __init__(self):
        #self.varname
        #will refance parrent obj and make a varible of the apropiate class
        #self.ctr = 0
        #self.tk_var = StringVar()
        #self.tk_var.set("0")

        #Fill Frames

        #intilize vars for the disp loop
        self.queuepos = 0
        self.dispdelay = 0


        self.updater()
        window.mainloop()
    
    def updater(self):
        #glove simulation
        SIMINPUT =[]
        for i in range(0,FingerCount):
            SIMINPUT.append(random.randrange(0,100)/100)
        Current = np.rint(np.multiply(SIMINPUT,100))
        

        #get new line as RAWINPUT Use decode()! 
        #RAWINPUT = arduino.readline()

        #change values of EVERYTHING
        for i in range(0,FingerCount):
            #Label Update
            MaxLabelList[i].config(width = 10,text="Max: " + str(Max[i]))
            CurLabelList[i].config(width = 10,text="Current: " + str(Current[i]))
            MinLabelList[i].config(width = 10,text="Min: " + str(Min[i]))

            #slider Update
            CanvasList[i].moveto(BarList[i],0,rescale(SliderMax,Current[i]/100))

        #Terminal update
        #Display
        maxcycle = 20
        
        if self.dispdelay > maxcycle:
            if len(dispqueue) > 1:
                if self.queuepos >= len(dispqueue):
                    self.queuepos = 0
                else:
                    Disp.config(text = dispqueue[self.queuepos])
                    self.queuepos = self.queuepos+1
            else:
                Disp.config(text = dispqueue[0])
            self.dispdelay=0
        else:
            self.dispdelay=self.dispdelay+1

        window.after(125, self.updater)

#intilize window
master = Tk()
window = Frame(master,width=680,height=480, bg = Background)
master.title('Glove Interface V2')


window.pack()

#Header
Label(window, text = "", bg = Background).grid(row = 0, column = 0)

#Frame Forming
Finger_frames = []
Slider_frames = []
Graph_frame = Frame(window,width=640,height=300,bg=Background)
Graph_frame.grid(row = 1, column = 0)
for i in range(0,FingerCount):
    #create Finger frames
    Fingers_FRAME = Frame(Graph_frame,width=128,height=300, bg = Background)
    Fingers_FRAME.grid(row=1, column = i)
    Finger_frames.append(Fingers_FRAME)
        
    #Create Slider Sub-frame
    Slider_FRAME = Frame(Fingers_FRAME,width=64,height=300)
    Slider_FRAME.grid(row=0, column = 1, rowspan=3)
    Slider_frames.append(Slider_FRAME)
    
Terminal = Frame(window,width=640,height=64,bg=Background)
Terminal.grid(row = 2, column = 0,)

#labels
LabelList = []
MaxLabelList = []
CurLabelList = []
MinLabelList = []
for i in range(0,FingerCount):
    #Int Labels
    MaxLabel = Label(Finger_frames[i],bg=Background,fg=BarColors[i])
    CurrentLabel = Label(Finger_frames[i],bg=Background,fg=BarColors[i])
    MinLabel = Label(Finger_frames[i],bg=Background,fg=BarColors[i])
    #Fill Labels
    MaxLabel.config(text = "Max: " + str(Max[i]))
    CurrentLabel.config(text = "Current: " + str(Current[i]))
    MinLabel.config(text = "Min: " + str(Min[i]))
    #Pack Labels
    MaxLabel.grid(row = 0, column = 0, sticky = 'e')
    CurrentLabel.grid(row = 1, column = 0, sticky = 'e')
    MinLabel.grid(row = 2, column = 0, sticky = 'e')
    #Label list construction
    MaxLabelList.append(MaxLabel)
    CurLabelList.append(CurrentLabel)
    MinLabelList.append(MinLabel)
    

CanvasList = []
BarList = []
#Create Sliders
for i in range(0,FingerCount):
    canvas = Canvas(Finger_frames[i],width=64,height=300,bg="#303134",)
    #Boxes
    box = canvas.create_rectangle(2, 2, 64, 300,outline=BarColors[i])
    #Bars
    canvas.pos = Current[i]*100
    pos = canvas.pos
    bar = canvas.create_rectangle(2,pos-Barwidth/2, 64,pos+Barwidth/2,outline="#000000",fill=BarColors[i])
    #pack it
    canvas.grid(row = 0, column = 1, rowspan=3)

    CanvasList.append(canvas)
    BarList.append(bar)

#Fill Terminal section
Label(Terminal,bg=Background).grid(row=0)
#disp
dispqueue = ["Idle","Test1","test2"]
Disp = Label(Terminal,bg=Background,fg=Txt,pady=16,width=64)
Disp.config(text = "Loading...",bd=4,highlightbackground=Txt,highlightthickness=2)
Disp.grid(row = 1, column = 0)
#PORT
Label(Terminal,bg=Background,width=2).grid(row=1,column=1)
# Dropdown menu options
ports = []
for port in range(7):
    ports.append("COM"+str(port+1))
#add the port check for the arduino

# initial menu text
clicked = StringVar()
clicked.set(ports[6]) #set this as the active port

drop = OptionMenu(Terminal,clicked,*ports)
drop.config(bg=Background,fg=Txt,pady=16,padx=48)
drop.grid(row = 1, column = 2)

#Recalibrate button
Label(Terminal,bg=Background,width=2).grid(row=1, column = 3)

CalibrateB = Button(Terminal, text = "Calibrate",command=Calibrate)
CalibrateB.config(bg=Background,fg=Txt,pady=16,padx=48)
CalibrateB.grid(row = 1, column = 4)


#test with glob
#arduino = serial.Serial(settings[2], 9600, timeout=1)

RUNMAIN = MAIN()
window.mainloop()

