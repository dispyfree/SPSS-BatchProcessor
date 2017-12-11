#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The SPSS Batch Processor is designed to run SPSS/PSPP syntaxes in batch mode. It can accept an arbitrary number of files and applies a given SPSS/PSPP routine to each file individually. Information specific to each subject (it is recommended to have one subject per file) can be extracted from the filename.
All commands are executed using the command line (PSPP) or line-wise using the SPSS Python API.

Author: Valentin Dreismann
Last modified: 2017

Psychologische Diagnostik. Differentielle Psychologie und Persönlichkeitspsychologie
University of Kiel
"""

#GUI imports
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

#system imports
import os
from os.path import basename
import re
import queue
import subprocess
import io
import time
import datetime
import argparse
import shutil

#project imports
from Lang import Lang
from Configuration import Configuration
from PSPPExecutor import PSPPExecutor
from SPSSExecutor import SPSSExecutor

class BatchProcessor:
    """
    Processing backend; breaks work down into tasks and arranges for their execution. Additionally, monitors progress
    """

    """
    Wraps execution by a specific statistics engine. 
    Available are PSPPExecutor and SPSSExecutor
    """
    executor = SPSSExecutor()


    # SPSS Processing
    # ----------------------------------------------------------------------------------------------------------------

    # run the processing itself, iterate over files and update progress indicator
    def runProcessing(self):
        print(Lang.get('Started processing...'))
        self.gui.GUIToConfig();

        totalUsedTime = 0.0;

        if not(self.runPreprocessingChecks()):
            return False

        self.config.opt['simulateProcessing'] = (self.gui.simulateProcessingVar.get() == 1);

        self.populateTaskQueue()
        self.trackProgress()

        # show debugging information upon completion
        if (self.config.opt['simulateProcessing']):
            # need try/catch here; depending on error, queue may be empty
            try:
                debuggingInfo = self.debuggingResultQueue.get_nowait();
                self.showDebuggingInformation(debuggingInfo)
            except queue.Empty as e:
                pass

        # transfer information from queue to log (i.e. workers => backend)
        self.transferLogQueue()
        completedMsg = Lang.get('Processing for {} files completed in {:.2f} seconds').format(
            len(self.config.opt['inputFiles']), totalUsedTime)
        self.executionLog.append(completedMsg)
        tk.messagebox.showinfo(Lang.get('Processing completed'), completedMsg);



    def trackProgress(self):
        """
        Indicates computation progress using progress bar in main window
        """
        alreadyProcessedFiles = 0;
        # keep updating the progress bar
        # at least one of debugging result queue OR errorQueue is expected to fill as well
        # queue may be empty immediately, as worker may "snatch" task before this function is even called.
        while (not (self.queue.empty()) or (self.debuggingResultQueue.empty() and self.errorQueue.empty())):
            processedAsOfNow = (self.totalFileNum - self.queue.qsize());
            processedJustNow = processedAsOfNow - alreadyProcessedFiles;
            alreadyProcessedFiles = processedAsOfNow;

            # advance progressbar
            self.gui.pb.step(processedJustNow / float(self.totalFileNum) * 100.0);
            totalUsedTime = (time.time() - self.start_time);

            # update estimated time
            estimate = self.estimateRemainingTime(self.totalFileNum, alreadyProcessedFiles, totalUsedTime)
            self.gui.remainingTimeLabel.config(text=Lang.get('Remaining time: %.2f seconds ') % estimate);

            # propagate changes to GUI
            self.gui.parent.update();
            time.sleep(0.5);



    def transferLogQueue(self):
        """
        Move events from logQueue (i.e. workers) to the backend log
        :return:
        """
        while not self.logQueue.empty():
            entry = self.logQueue.get_nowait()
            self.executionLog.append(entry)


    def runPreprocessingChecks(self):
        if len(self.config.opt['inputFiles']) == 0:
            self.err(Lang.get("You did not select any files"));
            return False

        #todo:check whether REGEX matches all files
        return True



    def populateTaskQueue(self):
        #populate execution log as well
        self.executionLog = []
        self.executionLog.append(Lang.get('Execution log on {}').format(datetime.datetime.now()))
        self.executionLog.append(Lang.get('Configuration dump: ') + os.linesep + self.config.toJSON())
        self.executionLog.append( os.linesep + Lang.get('Execution log:'))


        #for debugging, only very first file will be processed
        if(self.config.opt['simulateProcessing']):

            #if we do not accumulate, choose only one
            if not(self.config.opt['accumulateData']):
                self.config.opt['inputFiles'] = self.config.opt['inputFiles'][0:1]
            #otherwise, we need at least two
            else:
                self.config.opt['inputFiles'] = self.config.opt['inputFiles'][0:2]


        # we need copy here: we may reload the configuration file and do not want to
        # remove files permanently.
        inputFilesToUse = self.config.opt['inputFiles'][:]
        self.totalFileNum = 0

        #if we accumulate data, move and rename the very last entry, but do not touch the others
        if(self.config.opt['accumulateData']):
           self.moveRenameAccumulationFile(inputFilesToUse)


        self.start_time = time.time()
        # fill up queue of tasks/files
        for filePath in inputFilesToUse:
            self.defineDefaultPlaceholders(filePath);
            outputFilePath = self.getOutputFilePath(filePath);
            # attention: pickling in Python is seriously broken. passing self.config will mess up the configuration
            # (there are literally values missing)
            # parsing it to JSON and converting back works just fine.
            configStr = self.config.toJSON();
            self.queue.put([filePath, outputFilePath, configStr]);
            self.totalFileNum += 1



    def moveRenameAccumulationFile(self, inputFilesToUse):
        """
        Move very last file to destination, rename it and accumulate all other data on top
        :param inputFilesToUse: list of input paths
        """
        lastFilePath = inputFilesToUse.pop()
        self.totalFileNum += 1
        #override with input from GUI
        Configuration.accumulationFileName  = self.config.opt['outputFilePattern'];
        newFilePath = os.path.join(self.config.opt['outputDir'], Configuration.accumulationFileName)
        shutil.copyfile(lastFilePath, newFilePath)

        # furthermore, set spss execution file to template
        self.config.opt['spssFile'] = Configuration.accumulationFileTemplate
        self.config.opt['inputRegexPattern'] = self.config.opt['accumulationFilePattern']

        #propagate changes back to GUI
        self.gui.updateConfigGUI()



    def showDebuggingInformation(self, debuggingInfo):
        """
        Spawns new window, allows to inspect parameters and generated code for a single file
        :param debuggingInfo: dictionary with keys 'placeholders' and 'commands'
        :return:
        """
        t = tk.Toplevel(self.gui.parent)
        t.wm_title(Lang.get("Debugging information"))

        #organize placeholders and resulting source code into panes
        n = ttk.Notebook(t)

        n.add(self.gui.createFrameWithText(n, debuggingInfo['placeholders']), text=Lang.get('Placeholders'))
        n.add(self.gui.createFrameWithText(n, debuggingInfo['commands']), text=Lang.get('Sourcecode'))
        n.pack(expand=1, fill="both")

        # propagate changes to GUI
        self.gui.parent.update();



    def estimateRemainingTime(self, totalFiles, processedFiles, usedTime):
        if(processedFiles == 0):
            return 0.0;
        else:
            return (float(totalFiles - processedFiles) / float(processedFiles)) * usedTime;


    @classmethod
    def loadRawCommandsFromFile(cls, config):
        """
        Returns list of commands from file (which must be UTF-8 encoded)
        :param config: key 'spssFile' will be used
        :return: list of commands
        """
        with io.open(config.opt['spssFile'], "r", encoding='utf8') as f:
            if(f == None):
                cls.err(Lang.get("Unable to obtain file handle for SPSS file"))
            else:
                spssCommands = f.read()
        #by definition, commands end with "." and a newline
        #@todo: check if there's a way to catch \n and \r\n simultaneously
        spssCommands = spssCommands.split(".\n");
        return spssCommands



    @classmethod
    def instantiatePlaceholders(cls, config, inputFilePath, outputFilePath):
        fileName = os.path.basename(inputFilePath);
        inputFileNameMatch = re.match(config.opt['inputRegexPattern'], fileName)

        inputPath, fileName = os.path.split(inputFilePath);
        # set special placeholders
        config.opt['placeholders']['INFILE'] = inputFilePath;
        # input Path doesn't have a trailing slash
        config.opt['placeholders']['INPUTDIR'] = inputPath + '/';
        config.opt['placeholders']['OUTPUTFILE'] = outputFilePath;
        # output Path doesn't have a trailing slash
        config.opt['placeholders']['OUTPUTDIR'] = config.opt['outputDir'] + '/';
        config.opt['placeholders']['fileName'] = basename(inputFilePath);

        # incorporate the capture groups in the input file name into REGEX file
        # get groupnames themselves
        for grpName, grpValue in inputFileNameMatch.groupdict().items():
            config.opt['placeholders'][grpName] = grpValue;



    @classmethod
    def applyPlaceholders(cls, command, config):
        # replace placeholders
        for placeholderKey, substitute in config.opt['placeholders'].items():
            command = command.replace("<" + placeholderKey + ">", substitute);
        return command



    @staticmethod
    def runSPSSProcessOnFile(inputFilePath, outputFilePath, config, logQueue, debuggingResultQueue, errorQueue):
        """
        process single given file with SPSS template and save to output File
        returns the time it used up (in seconds)
        """
        #create dedicated TK instance; tk _always_ requires a window, however we just want message Boxes
        # create and hide main window
        root = tk.Tk()
        root.withdraw()

        start_time = time.time()

        logMsg = Lang.get("Processing ") +  inputFilePath + "..."
        print(logMsg);
        logQueue.put(logMsg)

        # read in commands
        spssCommands = BatchProcessor.loadRawCommandsFromFile(config)
        allCommands = [];
        BatchProcessor.instantiatePlaceholders(config, inputFilePath, outputFilePath)

        #execute file command by command
        for command in spssCommands:
            #ignore encoding line
            if(command.find('Encoding') != -1):
                continue;

            command = BatchProcessor.applyPlaceholders(command, config)
            allCommands.append(command)
            print(Lang.get("Executing: "), command);

        try:
            pointPlusNewline = '.' + os.linesep
            debuggingResultQueue.put({'placeholders': config.ObjToJSON(config.opt['placeholders']), 'commands':
                pointPlusNewline.join(allCommands)});

            BatchProcessor.executor.execute(allCommands)
        except subprocess.CalledProcessError as e:
            #halt processing
            errorQueue.put(e)
            logQueue.put(Lang.get('Error occurred; execution incomplete'))
            raise


        usedTime = (time.time() - start_time);
        logQueue.put(Lang.get('Processing finished in {:.2f}s').format(usedTime))

        return usedTime;



    @staticmethod
    def err(errMsg):
        """
        Shows given error message in Messagebox
        """
        tk.messagebox.showerror(Lang.get("Error"), errMsg)


    def defineDefaultPlaceholders(self, inputFilePath):
        inputPath, fileName = os.path.split(inputFilePath);

        # reset all placeholders. This is mandatory, as previous runs (other subjects) may have left values here
        # however, ALL placeholders existing before applying custom placeholders are considered to be PREDEFINED
        # (and will thus not be affected by custom placeholders)
        self.config.opt['placeholders'] = {};
        # set special placeholders
        self.config.opt['placeholders']['INFILE'] = inputFilePath;
        # input Path doesn't have a trailing slash
        self.config.opt['placeholders']['INPUTDIR'] = inputPath + '/';
        # output Path doesn't have a trailing slash
        self.config.opt['placeholders']['OUTPUTDIR'] = self.config.opt['outputDir'] + '/';
        self.config.opt['placeholders']['fileName'] = basename(inputFilePath);



    def getOutputFilePath(self, oldFilePath):
        """
        constructs output file path from given path and inputRegexPattern; also populates inputFileNameMatch
        """
        path = os.path.dirname(oldFilePath)
        file = os.path.basename(oldFilePath);
        # extract information from input file path using regex
        m = re.match(self.config.opt['inputRegexPattern'], file)
        self.inputFileNameMatch = m;

        if(m == None):
            self.err(Lang.get("Could not match input filename with pattern. Please check defined and used placeholders. "));

        # find all spots in the output file name to replace
        # they have the form <name1>, <name2> ...
        namedGroupPattern = '<([\w]*)>';
        placeholders = re.findall(namedGroupPattern, self.config.opt['outputFilePattern']);

        outputFileName = self.config.opt['outputFilePattern'];
        #replace the placeholders
        for placeholder in placeholders:
            try:
                #check whether it is a predefined placeholder
                if (placeholder in self.config.opt['placeholders']):
                    replacement = self.config.opt['placeholders'][placeholder];
                else:
                    replacement = m.group(placeholder)
                    # if placeholder is PREDEFINED (already exists in above array), this is a serisous error
                    # predefined placeholders may NOT be overwritten.
                    if(placeholder in self.config.opt['placeholders']):
                        msg = Lang.get('Predefined placeholders must not be redefined: attempted to define placeholder,  which already exists: ');
                        raise RuntimeError( msg + ' ' + placeholder);
            except IndexError:
                BatchProcessor.err(Lang.get("Placeholder in ouput file pattern refers to a placeholder which has not been defined"));

            # perhaps the placeholder is not in use after all (defined but not populated)
            if(replacement != None):
                outputFileName = outputFileName.replace('<' + placeholder + '>', replacement)
        return self.config.opt['outputDir'] + '/' + outputFileName



    def __init__(self, gui, parent, workerProcess, logQueue, taskQueue, debuggingResultQueue, errorQueue):
        """
        initialize with process and queue; please note that as TK handles _cannot_ be pickled, we need to create
        structures related to multiprocessing _before_ initializing the GUI (i.e. this class)
        :param gui: BatchProcessorGUI instance
        :param parent: TKinter frame instance (to draw into)
        :param workerProcess:
        :param logQueue:
        :param taskQueue:
        :param debuggingResultQueue:
        :param errorQueue:
        """
        self.p = workerProcess;
        self.queue, self.logQueue, self.debuggingResultQueue, self.errorQueue = taskQueue, logQueue, debuggingResultQueue, errorQueue;
        self.config = Configuration();

        parent.title(Lang.get("BatchProcessing"))
        self.gui = gui

        self.executionLog = []


