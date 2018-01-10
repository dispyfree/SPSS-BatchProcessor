
# gui imports
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter.scrolledtext

#system imports
import os

#project imports
from Lang import Lang
from batchProcessor import BatchProcessor
from GUIComponent import GUIComponent

class BatchProcessorGUI (GUIComponent):
    """
    GUI component to the BatchProcessor backend
    """

    # GUI
    # -------------------------------------------------------------------------------------------------------------

    # Options for selection of input files to process
    def getInputFileOptions(self):
        options = {}
        options['defaultextension'] = '.txt';
        options['filetypes'] = [('all files', '.*'), ('text files', '*.txt'), ('csv files', '*.csv'),
                                ('sav files', '*.sav'), \
                                ('custom pattern', self.inputSearchPattern.get())]
        options['title'] = Lang.get('Add input files')
        options['multiple'] = True
        options['initialdir'] = self.conf('defaultInputDir')
        return options;

    # options for selection of template SPSS file
    def getSPSSFileOptions(self):
        options = {}
        options['defaultextension'] = '.spss';
        options['filetypes'] = [('SPSS files', '*.sps')]
        options['title'] = 'Select processing SPSS file'
        options['multiple'] = False
        options['initialdir'] = self.conf('defaultSPSSDir')
        return options;

    # options for selection dialog of output directory
    def getOutputDirOptions(self):
        options = {}
        options['mustexist'] = False
        options['title'] = Lang.get('Select output directory')
        options['initialdir'] = self.conf('defaultOutDir')
        return options;

    # options for selection dialog of output directory
    def getSyntaxOutputDirOptions(self):
        options = {}
        options['mustexist'] = False
        options['title'] = Lang.get('Select syntax output directory')
        options['initialdir'] = self.conf('defaultSyntaxOutDir')
        return options;


    def __init__(self, parent, mainWindow, batchProcessorArgs):
        """

        :param parent: tkinter frame object
        :param mainWindow: MainWindow instance
        :param batchProcessorArgs: arguments to pass on to the backend
        """
        self.parent = parent
        batchProcessorArgs['gui'] = self
        self.backend = BatchProcessor(**batchProcessorArgs);
        self.mainWindow = mainWindow

        self.centerWindow()
        self.init_GUI(parent)

        #keeps track of all configurations we loaded
        self.loadedConfigurationFilePaths = self.mainWindow.state['actions']['recentActions']


    def propagateToUserState(self):
        self.mainWindow.saveUserState()



    def init_GUI(self, parent):
        parent.title(Lang.get('Processing'))
        # select nice style, if possible
        s = ttk.Style(parent)
        styles = s.theme_names()

        s.configure('TLabel', bg='white')
        s.configure('TNotebook', background = '#ffffff')
        s.configure('TNotebook.Tab', background='#ffffff')
        parent.configure(background='white')


        self.notebook = ttk.Notebook(parent, padding=10)


        # Configuration
        #------------------------------------------------------------------------------------------------------

        self.configurationPane =   tk.Frame(self.notebook)
        self.configurationPane.configure(background = 'white')

        # input file selection
        # file pattern
        self.searchPatternLabel = tk.Label(self.configurationPane, text=Lang.get("Input search pattern"), **self.getItemStyle()).grid(
            row=0, column=0, sticky=tk.W);
        self.inputSearchPattern = tk.StringVar()
        self.inputSearchPattern.set('.txt');
        self.inputEntry = tk.Entry(self.configurationPane, textvariable=self.inputSearchPattern)
        self.inputEntry.grid(row=0, column=1, sticky=tk.W + tk.E)


        tk.Label(self.configurationPane, text=Lang.get("Input regex pattern"), **self.getItemStyle()).grid(row=1, column=0,
                                                                                           sticky=tk.W);
        self.inputRegexPattern = tk.StringVar()
        self.inputRegexPattern.set('(?P<fileName>[\w]*).txt');
        self.inputRegexEntry = tk.Entry(self.configurationPane, textvariable=self.inputRegexPattern, **self.getItemStyle())
        self.inputRegexEntry.grid(row=1, column=1, sticky=tk.W + tk.E, columnspan=1)

        # processing spss file
        self.processSPSSFileLabel = tk.Label(self.configurationPane, text=Lang.get("Processing SPSS file"), **self.getItemStyle()).grid(row=2, column=0,
                                                                                            sticky=tk.W);
        self.spssFile = tk.StringVar()
        self.spssFile.set('none selected')
        self.spssFileLabel = tk.Label(self.configurationPane, text=self.spssFile.get(), **self.getItemStyle());
        self.spssFileLabel.grid(row=2, column=1, sticky=tk.W + tk.E);
        self.selectSPSSFileButton = tk.Button(self.configurationPane, text=Lang.get("Select SPSS file"),
                                   command=self.selectSPSSFile, **self.getItemStyle())
        self.selectSPSSFileButton.grid(row=2, column=2,sticky=tk.W)


        # ouptut file pattern
        tk.Label(self.configurationPane, text=Lang.get("Output file pattern"), **self.getItemStyle()).grid(row=3, column=0,
                                                                                           sticky=tk.W);
        self.outputFilePattern = tk.StringVar()
        self.outputFilePattern.set('<fileName>.sav');
        self.outputEntry = tk.Entry(self.configurationPane, textvariable=self.outputFilePattern, **self.getItemStyle())
        self.outputEntry.grid(row=3, column=1, sticky=tk.W + tk.E)

        # ouptut directory
        tk.Label(self.configurationPane, text=Lang.get("Output directory"), **self.getItemStyle()).grid(row=4, column=0, sticky=tk.W);
        self.outputDir = tk.StringVar();
        self.outputDir.set('none selected');
        self.outputDirLabel = tk.Label(self.configurationPane, textvariable=self.outputDir, **self.getItemStyle());
        self.outputDirLabel.grid(row=4, column=1, sticky=tk.W);
        selectOutDirButton = tk.Button(self.configurationPane, text=Lang.get("Select output directory"),
                                       command=self.selectOutDir, **self.getItemStyle())
        selectOutDirButton.grid(row=4, column=2, sticky=tk.W);

        # special functions
        tk.Label(self.configurationPane, text=Lang.get("Special Functions"), **self.getItemStyle()).grid(row=5,
                                                                                                         column=0,
                                                                                                         sticky=tk.W);
        self.accumulateDataVar = tk.IntVar()
        self.accumulateDataButton = tk.Checkbutton(self.configurationPane, text=Lang.get("Accumulate Data"),
                                                   variable=self.accumulateDataVar,
                                                   command = self.updateByAccumulateButton,
                                                   indicatoron=0, **self.getItemStyle());
        self.accumulateDataButton.grid(row=5, column=1, sticky=tk.W + tk.E + tk.N + tk.S)

        # write out syntaxes
        tk.Label(self.configurationPane, text=Lang.get("Syntax generation"), **self.getItemStyle()).grid(row=6, column=0, sticky=tk.W)
        self.syntaxGenerationDirVar = tk.StringVar()
        self.syntaxGenerationDirVar.set('none');
        self.syntaxGenerationFolder = tk.Entry(self.configurationPane, textvariable=self.syntaxGenerationDirVar)
        self.syntaxGenerationFolder.grid(row=6, column=1, sticky = tk.W + tk.E);
        selectOutDirButton = tk.Button(self.configurationPane, text=Lang.get("Select output directory"),
                                       command=self.selectSyntaxOutputDir, **self.getItemStyle())
        selectOutDirButton.grid(row=6, column=2, sticky=tk.W);


        self.pad(self.configurationPane)
        self.notebook.add(self.configurationPane, text=Lang.get('Configuration'))



        # File Selection
        # ------------------------------------------------------------------------------------------------------
        self.fileSelectionPane = tk.Frame(self.notebook)
        self.fileSelectionPane.configure(background='white')

        selectFilesButton = tk.Button(self.fileSelectionPane, text=Lang.get("Select input files"),
                                      command=self.selectFiles, **self.getItemStyle())
        selectFilesButton.grid(row=0, column=0, sticky=tk.W)

        # load config
        selectFilesDirectoryButton = tk.Button(self.fileSelectionPane, text=Lang.get("Select Dir"),
                                               command=self.selectDir, **self.getItemStyle())
        selectFilesDirectoryButton.grid(row=0, column=1, sticky=tk.W);

        self.selectedFilesList = tk.Listbox(self.fileSelectionPane)
        self.selectedFilesList.grid(row=1, rowspan = 6,
                                    column = 0, columnspan = 6, sticky = tk.W + tk.E)
        # let it take up entire window
        self.fileSelectionPane.grid_columnconfigure(0, weight=1)
        self.fileSelectionPane.grid_columnconfigure(1, weight=3)

        self.removeFilesButton = tk.Button(self.fileSelectionPane, text=Lang.get('Remove selected files'),
                                           command = self.removeSelectedFiles, **self.getItemStyle())
        self.removeFilesButton.grid(row=7, column=2, sticky=tk.E)

        self.removeAllFilesButton = tk.Button(self.fileSelectionPane, text=Lang.get('Remove all files'),
                                           command=self.removeAllFiles, **self.getItemStyle())
        self.removeAllFilesButton.grid(row=7, column=3, sticky=tk.E)

        self.selectiontoClipboardButton = tk.Button(self.fileSelectionPane, text=Lang.get('Copy selection'),
                                              command=self.selectionToClipboard, **self.getItemStyle())
        self.selectiontoClipboardButton.grid(row=7, column=4, sticky=tk.E)

        self.pad(self.fileSelectionPane)
        self.notebook.add(self.fileSelectionPane, text=Lang.get('File Selection'))
        #self.notebook.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)



        # Execution
        # ------------------------------------------------------------------------------------------------------
        self.executionPane = tk.Frame(self.notebook)
        self.executionPane.configure(background='white')

        #maximum space it will take up
        portionOfScreenWidth = self.w - 200
        tk.Label(self.executionPane, text=Lang.get("runDescription"), wraplength = portionOfScreenWidth,
                 justify= tkinter.LEFT, **self.getItemStyle()).grid(row=0, column=0, columnspan = 6, sticky=tk.W);

        # progress bar
        self.pb = ttk.Progressbar(self.executionPane, orient="horizontal", length=portionOfScreenWidth,mode="determinate");
        self.pb.grid(row=2, column=0, sticky=tk.W + tk.E, columnspan=6)

        #check output files
        #todo: implement

        # Simulate
        self.simulateProcessingVar = tk.IntVar()
        self.simulateProcessingVar.set(0);  # defaults to no simulation
        self.simulateButton = tk.Checkbutton(self.executionPane, text=Lang.get("Simulate"),
                                             variable=self.simulateProcessingVar,
                                             indicatoron=0, **self.getItemStyle());
        self.simulateButton.grid(row=5, column=0, sticky= tk.W + tk.E)

        # run button
        runButton = tk.Button(self.executionPane, text=Lang.get("Run"),
                              command=self.backend.runProcessing, **self.getItemStyle())
        runButton.grid(row=5, column=1, columnspan = 5, sticky= tk.W + tk.E);

        self.remainingTimeLabel = tk.Label(self.executionPane, **self.getItemStyle());
        self.remainingTimeLabel.grid(row=5, column=6, sticky= tk.W + tk.E);

        saveLog = tk.Button(self.executionPane, text=Lang.get("Save Processing Log"),
                            command=self.saveProcessingLog, **self.getItemStyle())
        saveLog.grid(row=6, column=1, columnspan=5, sticky=tk.W + tk.E);

        self.pad(self.executionPane)
        self.notebook.add(self.executionPane, text=Lang.get('Execution'))


        # Save & Restore
        # ------------------------------------------------------------------------------------------------------
        self.saveRestorePane = tk.Frame(self.notebook)
        self.saveRestorePane.configure(background='white')

        # load config
        loadConfigButton = tk.Button(self.saveRestorePane, text=Lang.get("Load config"),
                                     command=self.loadConfig, **self.getItemStyle())
        loadConfigButton.grid(row=0, column=1, sticky=tk.W + tk.E);

        # save config
        saveConfigButton = tk.Button(self.saveRestorePane, text=Lang.get("Save config"),
                                     command=self.saveConfig, **self.getItemStyle())
        saveConfigButton.grid(row=0, column=2, sticky=tk.W + tk.E);

        self.pad(self.saveRestorePane)
        self.notebook.add(self.saveRestorePane, text=Lang.get('Save & Restore'))


        self.configurePadding()



    # Selection process
    # ---------------------------------------------------------------------------------------------------------------
    def selectFiles(self):
        tmpFiles = tk.filedialog.askopenfilename(**self.getInputFileOptions());
        if tmpFiles:
            # set defaults
            self.setConf('defaultInputDir', os.path.dirname(tmpFiles[0]));
            inputFiles = self.conf('inputFiles')
            inputFiles += list(tmpFiles)
            self.populateSelectedFileList()


    def populateSelectedFileList(self):
        #clear list
        self.selectedFilesList.delete(0, tk.END)

        for file in self.conf('inputFiles'):
            self.selectedFilesList.insert(self.selectedFilesList.size(), file)



    def removeSelectedFiles(self):
        selected = self.selectedFilesList.curselection()

        #remove from top to bottom to avoid wrong indices
        selected = list(selected)
        selected.sort()
        selected = reversed(selected)
        for index in selected:
            self.conf('inputFiles').pop(index)

        self.populateSelectedFileList()


    def removeAllFiles(self):
        self.setConf('inputFiles', [])
        self.populateSelectedFileList()


    def selectionToClipboard(self):
        self.parent.clipboard_clear()
        fileList = os.linesep.join(self.conf('inputFiles'))
        self.parent.clipboard_append(fileList)


    def selectDir(self):
        """
        Asks operator for directory and adds all files contained within to the current selections
        :return:
        """
        directory = tk.filedialog.askdirectory();
        if directory:
            # set defaults
            self.setConf('defaultInputDir', directory)
            paths = [os.path.join(directory, fn) for fn in next(os.walk(directory))[2]]
            inputFiles = self.conf('inputFiles')
            inputFiles += paths
            self.populateSelectedFileList()


    def selectOutDir(self):
        """
        Asks operator for output directory
        """
        dirName = tk.filedialog.askdirectory(**self.getOutputDirOptions())
        if dirName:
            # set defaults
            self.setConf('defaultOutDir', dirName);
            self.outputDir.set(dirName)
            self.outputDirLabel.config(text=self.outputDir.get())

    def selectSyntaxOutputDir(self):
        """
        Asks operator for output directory
        """
        dirName = tk.filedialog.askdirectory(**self.getSyntaxOutputDirOptions())
        if dirName:
            # set defaults
            self.setConf('defaultSyntaxOutDir', dirName);
            self.syntaxGenerationDirVar.set(dirName)
            self.syntaxGenerationFolder.config(text=self.syntaxGenerationDirVar.get())


    def selectSPSSFile(self):
        """
        Asks operator for SPSS file
        """
        fileName = tk.filedialog.askopenfilename(**self.getSPSSFileOptions())
        if (fileName):
            # set defaults
            self.setConf('defaultSPSSDir', os.path.dirname(fileName))
            self.spssFile.set(fileName)
            self.spssFileLabel.config(text=self.spssFile.get());


    # Configuration management
    # ----------------------------------------------------------------------------------------------------------------
    def conf(self, entry):
        #todo: remove
        if not(entry in self.backend.config.opt):
            return ''
        else:
            return self.backend.config.opt[entry]

    def setConf(self, entry, value):
        self.backend.config.opt[entry] = value;


    def updateByAccumulateButton(self):
        """
        Limits availability of other functionality depending on whether accumulation is chosen
        (i.e. specification of input regex pattern is not well-defined if accumulation is enabled)
        :return:
        """
        # first, disable/enable other buttons
        othersState = 'normal'
        if(self.accumulateDataVar.get() == 1.0):
            othersState = 'disabled'

        self.inputRegexEntry.config(state = othersState)
        self.spssFileLabel.config(state = othersState)
        self.selectSPSSFileButton.config(state = othersState)
        self.outputEntry.config(state=othersState)

        self.parent.update()


    def updateConfigGUI(self):
        """
        Propagates config to GUI
        """
        self.inputSearchPattern.set(self.conf(u'inputSearchPattern'));
        self.inputRegexPattern.set(self.conf(u'inputRegexPattern'));
        self.spssFile.set(self.conf(u'spssFile'));
        self.spssFileLabel.config(text=self.spssFile.get());
        self.outputFilePattern.set(self.conf(u'outputFilePattern'));
        self.outputDir.set(self.conf(u'outputDir'));
        self.simulateProcessingVar.set(self.conf('simulateProcessing'))
        self.accumulateDataVar.set(self.conf('accumulateData'))
        self.populateSelectedFileList()
        self.syntaxGenerationDirVar.set(self.conf('defaultSyntaxOutDir'))


    def GUIToConfig(self):
        """
        Propagates GUI to config
        """
        self.setConf('inputSearchPattern', self.inputSearchPattern.get())
        self.setConf('inputRegexPattern', self.inputRegexPattern.get())
        self.setConf('spssFile', self.spssFile.get())
        self.setConf('outputFilePattern', self.outputFilePattern.get())
        self.setConf('outputDir', self.outputDir.get())
        self.setConf('simulateProcessing', self.simulateProcessingVar.get() == 1.0)
        self.setConf('accumulateData', self.accumulateDataVar.get() == 1.0)
        self.setConf('defaultSyntaxOutDir', self.syntaxGenerationDirVar.get() )


    def loadConfig(self):
        """
        Inquires about configuration file, loads specified file
        :return:
        """
        filePath =  tk.filedialog.askopenfilename(filetypes = [('JSON files', '*.json')], initialdir = self.conf('defaultConfigDir'));
        if(filePath):
            self.loadConfigFromFile(filePath);
        else:
            self.err(Lang.get('You did not select a config file or the file could not be opened'))


    def loadConfigFromFile(self, filePath):
        self.backend.config.loadFromFile(open(filePath, 'r'));
        # set defaults
        self.setConf('defaultConfigDir', os.path.dirname(filePath))
        self.updateConfigGUI();

        #only add if it's not there yet
        if(filePath not in self.loadedConfigurationFilePaths):
            self.loadedConfigurationFilePaths.insert(0, filePath)

        self.propagateToUserState()
        self.updateByAccumulateButton()


    def saveConfig(self):
        """
        prompts the user for a filename and saves the configuration there
        """
        self.GUIToConfig();
        f = tk.filedialog.asksaveasfile(mode='w', filetypes=[('JSON files', '*.json')], defaultextension = '.json');
        if(f):
            f.write(self.backend.config.toJSON());
            f.close();
            tk.messagebox.showinfo(Lang.get("Configuration file saved"), Lang.get("The configuration file has been successfully saved"))
        else:
            self.err(Lang.get('You did not select a desetination file or the file could not be saved'))



    def saveProcessingLog(self):
        """
        transfers events from log queue to main log instance, asks operator for file name and exports log
        """
        self.backend.transferLogQueue()
        fileName = tk.filedialog.asksaveasfilename(initialdir= self.conf('defaultOutDir'), title=Lang.get('Select Logfile'),  filetypes=[("Log files", "*.txt"), ("all files","*.*")])

        if fileName is not None:
            with open(fileName, "w") as logFile:
                logFile.write(os.linesep.join(self.backend.executionLog))
                logFile.close()
                tk.messagebox.showinfo(Lang.get("Logfile saved"),
                                       Lang.get("The Logfile has been saved at the specified destination"))

    @classmethod
    def handleExecutionError(self, exception, taskQueue, debuggingResultQueue, errorQueue):
        """
        Inquires whether operators would like to continue or to skip all remaining files
        :param taskQueue:
        :param debuggingResultQueue:
        :param errorQueue:
        :return:
        """
        spssExecutionError = ''
        # CalledProcessError features the program's output in 'output'
        if hasattr(exception, 'output'):
            spssExecutionError = str(exception.output)
        errMsg =    Lang.get('The following error occured, please check the log for details' + \
        '\n Would you like to continue with the next file (Yes) or cancel processing (No) for all remaining files?')
        print(spssExecutionError + '\n' + str(exception))

        wantsToContinue = tk.messagebox.askyesno(Lang.get("Error occured, execution halted"),
                            errMsg)
        if not(wantsToContinue):
            # clear the queue
            while not taskQueue.empty():
                taskQueue.get_nowait()  # as docs say: Remove and return an item from the queue.
            print(Lang.get('Execution of remaining files has been aborted as by user\'s choice.'))


