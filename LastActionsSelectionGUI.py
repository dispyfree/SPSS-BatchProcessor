import tkinter as tk
import tkinter.ttk as ttk

from Lang import Lang
from GUIComponent import GUIComponent

class LastActionsSelectionGUI (GUIComponent):
    """
    Spawns dedicated window to let operator choose among last actions
    instantiates BatchProcessorGUI if action is selected
    """
    # maximum number of last actions to display
    lastActionsNum = 10

    # width of actions list in pixels
    actionsListWidth = 400

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
        self.selectedActionList.config(width = self.actionsListWidth)
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
        lastActions = self.mainWindow.state['actions']['recentActions']
        noOfActions = min(len(lastActions), self.lastActionsNum)
        lastActions = lastActions[0:noOfActions]

        for actionPath in lastActions:
            self.selectedActionList.insert(self.selectedActionList.size(), actionPath)


    def __init__(self, parent, mainWindow):
        self.parent, self.mainWindow = parent, mainWindow

        self.init_GUI(self.parent)
        self.centerWindow()
