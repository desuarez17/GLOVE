try:
    #import Tkinter as tk     ## Python 2.x
except ImportError:
    import tkinter as tk     ## Python 3.x



class UpdateLabel():
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Ausgangsposition")
        self.win.minsize(800, 600)
        self.ctr = 0
        self.tk_var = tk.StringVar()
        self.tk_var.set("0")
        lab=tk.Label(self.win, textvariable=self.tk_var,
                       bg='#40E0D0', fg='#FF0000')
        lab.place(x=20, y=30)
        self.updater()
        self.win.mainloop()

    def updater(self):
        self.ctr += 1
        self.tk_var.set(str(self.ctr))
        if self.ctr < 10:
            self.win.after(1000, self.updater)
        else:
            self.win.quit()

UL=UpdateLabel()