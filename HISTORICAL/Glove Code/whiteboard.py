#1st line!

from tkinter import *
from tkinter import Frame
import tkinter
import serial
import numpy as np
    






class MAIN():
    def __init__(self):
        #self.varname
        #will refance parrent obj and make a varible of the apropiate class
        self.ctr = 0
        self.tk_var = StringVar()
        self.tk_var.set("0")
        lab.config(text="new")
        lab.pack()
        lab2 = Label(window, textvariable=self.tk_var,)
        lab2.pack()



        

        self.updater()
        window.mainloop()
    
    def updater(self):
        
        self.ctr += 1
        self.tk_var.set(str(self.ctr))

        
        print(clicked.get())
        
        window.after(100, self.updater)

#intilize window
window = Tk()
window.title('Glove Interface V2')
window.geometry('680x480')

lab = Label(window, text = "teast")


# Dropdown menu options
ports = []
for port in range(7):
    ports.append("COM"+str(port+1))


  
# initial menu text
clicked = StringVar()
clicked.set(ports[6])
  
# Create Dropdown menu
drop = OptionMenu( window , clicked , *ports )
drop.pack()



RUNMAIN = MAIN()
window.mainloop()

