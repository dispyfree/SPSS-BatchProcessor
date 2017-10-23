import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.scrolledtext

from Lang import Lang

class GUIComponent:
    """
    Base class for all components (providing uniform styling)
    """

    @staticmethod
    def getItemStyle():
        return {
            'bg': 'white'
        }

    def configurePadding(self):
        # do some padding
        for child in self.parent.winfo_children():
            child.grid(padx=5, pady=5)

    def pad(self, parent):
        for obj in parent.winfo_children():
            obj.grid(padx = 10, pady = 10)


    def centerWindow(self):
        # define measurements and center with respect to those
        self.w = 750
        self.h = 400

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - self.w) / 2
        y = (sh - self.h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))


    def createFrameWithText(self, parent, textValue):
        frame = tk.Frame(parent)
        t = tkinter.scrolledtext.ScrolledText(frame, undo=True)
        t.pack()
        t.insert(tk.END, textValue)
        return frame

    @staticmethod
    def err(errMsg):
        tk.messagebox.showerror(Lang.get("Error"), errMsg)