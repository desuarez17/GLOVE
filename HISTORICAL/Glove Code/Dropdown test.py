#1st line!

from tkinter import *
from tkinter import Frame
import tkinter
import serial
import numpy as np
    


# Create object
root = Tk()
  
# Adjust size
root.geometry( "200x200" )
  



import sys
import glob
import serial


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


#if __name__ == '__main__':
   # print(serial_ports())


# Change the label text
def show():
    label.config( text = clicked.get() )
# Dropdown menu options
ports = []
for port in range(7):
    ports.append("COM"+str(port+1))


# datatype of menu text
clicked = StringVar()
  
# initial menu text
clicked.set(ports[6])
  
# Create Dropdown menu
drop = OptionMenu( root , clicked , *ports )
drop.pack()
  
# Create button, it will change label text
button = Button( root , text = "click Me" , command = show ).pack()
  
# Create Label
label = Label( root , text = "" )
label.pack()
  
# Execute tkinter
root.mainloop()
