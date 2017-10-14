import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
import json

import configparser, os

from multiprocessing import Process, Queue
from BatchProcessorGUI import BatchProcessorGUI

from Lang import Lang

class MainWindow:

    userStateFileName = '~/.batchProcessor.txt'

    userStateDefaults = {
        'actions' :{
            'recentActions': [],
            'lastAction' : None,
        },
        'settings' :{
            'language' : []
        }
    }
    userStateSections = ['actions', 'settings']

    @staticmethod
    def getItemStyle():
        return {
            'bg': 'white'
        }

    def __init__(self):
        self.readUserState()
        #make sure it exists
        self.saveUserState()
        self.initializeWorkerAndGUI()

        self.parent.withdraw()
        self.mainWindow = tk.Toplevel(self.parent)
        self.initGUI()
        self.centerWindow()
        self.parent.mainloop()


    def redoAction(self):
        pass


    def spawnNewConfiguration(self):
        self.showBatchProcessor()


    def readUserState(self):
        expandedFileName =  os.path.expanduser(self.userStateFileName)

        if not(os.path.isfile(expandedFileName)):
            self.state = self.userStateDefaults
        else:
            try:
                file = open(expandedFileName, 'r')
                self.state =  json.load(file);
                file.close()
            except:
                self.err('Unable to load user state file')

    def saveUserState(self):

        with open(os.path.expanduser(self.userStateFileName), 'w+') as f:
            if f is None:
                self.err("Unable to save user state file")
            f.write(json.dumps(self.state))
            f.close()



    def configurePadding(self):
        # do some padding
        for child in self.centerFrame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def initGUI(self):
        self.mainWindow.configure(background='white')
        self.mainWindow.title("SPSS Toolbox")

        self.centerFrame = tkinter.Frame(self.mainWindow)
        self.centerFrame.configure(padx = 50, pady = 50, height=200, background='white')

        spssToolboxLabel = tk.Label(self.centerFrame, text=Lang.get("SPSS Toolbox"), **self.getItemStyle(),
                 font = ('Times', 25, 'bold'))
        spssToolboxLabel.grid(row=0, column=0, sticky=tk.W + tk.E);


        self.actionsFrame = tkinter.Frame(self.centerFrame)
        self.recentActionsButton = tk.Button(self.actionsFrame, text=Lang.get("Last Actions"),
                                              command=self.redoAction, **self.getItemStyle())
        self.recentActionsButton.grid(row=0, column=0, sticky=tk.W + tk.E)

        self.redoLastActionButton = tk.Button(self.actionsFrame, text=Lang.get("Redo Last"),
                                      command=self.redoAction, **self.getItemStyle())
        self.redoLastActionButton.grid(row=0, column=1, sticky=tk.W+ tk.E)

        #assign non-zero weights (1 for both columns) to allow buttons to take up extra space
        self.actionsFrame.grid(row = 5, column = 0, sticky=tk.W+ tk.E)
        self.actionsFrame.grid_columnconfigure(0, weight=1)
        self.actionsFrame.grid_columnconfigure(1, weight=1)


        self.loadConfigurationButton = tk.Button(self.centerFrame, text=Lang.get("Load Configuration"),
                                           command=self.redoAction, **self.getItemStyle())
        self.loadConfigurationButton.grid(row=6, column=0, sticky=tk.W + tk.E)

        self.newConfigurationButton = tk.Button(self.centerFrame, text=Lang.get("New Configuration"),
                                                 command=self.spawnNewConfiguration, **self.getItemStyle())
        self.newConfigurationButton.grid(row=7, column=0, sticky=tk.W+ tk.E)

        self.helpButton = tk.Button(self.centerFrame, text=Lang.get("Help"),
                                                command=self.showHelp, **self.getItemStyle())
        self.helpButton.grid(row=8, column=0, sticky=tk.W + tk.E)


        self.configurePadding()
        spssToolboxLabel.grid(pady = (0, 30))
        self.centerFrame.pack()
        self.adaptGUIToState()



    def adaptGUIToState(self):
        # disable if there is none
        if self.state['actions']['lastAction'] == None:
            self.redoLastActionButton.config(state='disabled')

        if(len(self.state['actions']['recentActions']) == 0):
            self.recentActionsButton.config(state = 'disabled')

    def centerWindow(self):
        # define measurements and center with respect to those
        w = 600
        h = 300

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))



    def initializeWorkerAndGUI(self):
        self.taskQueue = Queue()
        # returns the parsed script/placeholders to the calling process
        # please note that Tkinter is NOT threadsafe.
        self.debuggingResultQueue = Queue()
        self.p = Process(target=SPSSWorkerProcess, args=(self.taskQueue, self.debuggingResultQueue));

        # start worker process
        # could be starting a pool of workers as well
        self.p.start()

        self.parent = root = tk.Tk();


    def showBatchProcessor(self):

        batchProcessorArgs = {'parent': self.parent,
                              'workerProcess': self.p,
                              'taskQueue': self.taskQueue,
                              'debuggingResultQueue': self.debuggingResultQueue}
        self.gui = BatchProcessorGUI(tk.Toplevel(self.parent), batchProcessorArgs);


    def showHelp(self):
        tkinter.messagebox.showinfo(
            "Help",
            "Find detailed information on github.com"
        )

    @staticmethod
    def err(errMsg):
        tk.messagebox.showerror(Lang.get("Error"), errMsg)


def SPSSWorkerProcess(taskQueue, debuggingResultQueue):
    while(True):
        #block until next job is fetched
        job = taskQueue.get(True);
        [inputFilePath, outputFilePath, configStr] = job;
        config = Configuration()
        config.loadFromString(configStr);
        BatchProcessor.runSPSSProcessOnFile(inputFilePath, outputFilePath, config, debuggingResultQueue);



def main():
    mainWindow = MainWindow()

if __name__ == '__main__':
    main()
