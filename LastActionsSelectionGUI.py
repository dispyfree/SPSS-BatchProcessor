import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk

from Lang import Lang


class LastActionsSelectionGUI:

    @staticmethod
    def getItemStyle():
        return {
            'bg': 'white'
        }


    def init_GUI(self, parent):
        parent.title(Lang.get('Processing'))
        # select nice style, if possible
        s = ttk.Style(parent)
        styles = s.theme_names()

        s.configure('TLabel', bg='white')
        s.configure('TNotebook', background='#ffffff')
        s.configure('TNotebook.Tab', background='#ffffff')
        parent.configure(background='white')


        self.selectedActionList = tk.Listbox(self.parent)
        self.selectedActionList.grid(row=1, rowspan=6,
                                    column=0, columnspan=6, sticky=tk.W + tk.E)
        actionsListWidth = 400
        self.selectedActionList.config(width = actionsListWidth)
        self.populateActionsList()

        self.openSelectedActionsButton = tk.Button(self.parent, text= Lang.get('Open selected Configuration'),
            command=self.openSelectedAction, **self.getItemStyle()).grid(row=7,column=0,sticky= tk.E + tk.W)



    def openSelectedAction(self):
        selection = self.selectedActionList.curselection()
        if(not(len(selection) == 1)):
            self.mainWindow.err(Lang.get('You must select exactly one entry.'))
        else:
            selectedIndex = selection[0]
            actionPath = self.mainWindow.state['actions']['recentActions'][selectedIndex]
            self.parent.destroy()
            self.mainWindow.showBatchProcessor()
            self.mainWindow.gui.loadConfigFromFile(actionPath)


    def populateActionsList(self):
        # clear list
        self.selectedActionList.delete(0, tk.END)

        # create buttons for 5 last actions from backend
        lastActionsNum = 10
        lastActions = self.mainWindow.state['actions']['recentActions']
        noOfActions = min(len(lastActions), lastActionsNum)
        lastActions = lastActions[0:noOfActions]

        for actionPath in lastActions:
            self.selectedActionList.insert(self.selectedActionList.size(), actionPath)


    def centerWindow(self):
        # define measurements and center with respect to those
        self.w = 700
        self.h = 200

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - self.w) / 2
        y = (sh - self.h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))



    def __init__(self, parent, mainWindow):
        self.parent, self.mainWindow = parent, mainWindow

        self.init_GUI(self.parent)
        self.centerWindow()
