#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The SPSS Batch Processor is designed to run spss syntaxes in batch mode. It can accept an arbitrary number of files
and applies a given SPSS routine to each file individually. Information specific to each subject (it is recommended
to have one subject per file) can be extracted from the filename.
All commands are executed line-wise using the SPSS Python API.

Author: Valentin Dreismann
Last modified: 2017

Psychologische Diagnostik. Differentielle Psychologie und Persönlichkeitspsychologie
University of Kiel
"""
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk

import os
from os.path import basename
import re
from multiprocessing import Process, Queue
import json
#import spss
import io
import time

import argparse

from Lang import Lang
from Configuration import Configuration


class BatchProcessor:

    # SPSS Processing
    # ----------------------------------------------------------------------------------------------------------------

    # run the processing itself, iterate over files and update progress indicator
    def runProcessing(self):
        print(Lang.get('Started processing...'))
        self.GUIToConfig();
        start_time = time.time()
        totalFileNum = len(self.inputFiles);
        fileCounter = 0;
        totalUsedTime = 0.0;

        if len(self.inputFiles) == 0:
            self.err(Lang.get("You did not select any files"));
            return False;

        #for simulation, simulate only first file
        if (self.simulateProcessingVar.get() == 1):
            self.inputFiles = self.inputFiles[:1]
        self.config.opt['simulateProcessing'] = (self.simulateProcessingVar.get() == 1);

        #fill up queue of tasks/files
        for filePath in self.inputFiles:
            self.defineDefaultPlaceholders(filePath);
            outputFilePath = self.getOutputFilePath(filePath);
            # attention: pickling in Python is seriously broken. passing self.config will mess up the configuration
            # (there are literally values missing)
            # parsing it to JSON and converting back works just fine.
            configStr = self.config.toJSON();
            self.queue.put([filePath, outputFilePath, configStr]);

        alreadyProcessedFiles = 0;
        #keep updating the progress bar
        while(not(self.queue.empty())):
            processedAsOfNow = (totalFileNum - self.queue.qsize());
            processedJustNow = processedAsOfNow - alreadyProcessedFiles;
            alreadyProcessedFiles = processedAsOfNow;

            #advance progressbar
            self.pb.step(processedJustNow / float(totalFileNum) * 100.0);
            totalUsedTime = (time.time() - start_time);

            #update estimated time
            self.remainingTimeLabel.config(text=Lang.get('Remaining time: %.2f seconds ') % self.estimateRemainingTime(
                len(self.inputFiles), alreadyProcessedFiles, totalUsedTime));

            #propagate changes to GUI
            self.parent.update();
            time.sleep(0.5);

        if (self.config.opt['simulateProcessing']):
            debuggingInfo = self.debuggingResultQueue.get(True, 0.1); # raises Empty exception if no result is present
            self.showDebuggingInformation(debuggingInfo)

        tk.messagebox.showinfo(Lang.get('Processing completed'), Lang.get('Processing for %d files completed in %f seconds') % (
            len(self.inputFiles), totalUsedTime));


    def showDebuggingInformation(self, debuggingInfo):
        t = tk.Toplevel(self.parent)
        t.wm_title(Lang.get("Debugging information"))

        #organize placeholders and resulting source code into panes
        n = tk.Notebook(t)

        n.add(self.createFrameWithText(n, debuggingInfo['placeholders']), text=Lang.get('Placeholders'))
        n.add(self.createFrameWithText(n, debuggingInfo['commands']), text=Lang.get('Sourcecode'))
        n.pack(expand=1, fill="both")

        # propagate changes to GUI
        self.parent.update();


    def estimateRemainingTime(self, totalFiles, processedFiles, usedTime):
        if(processedFiles == 0):
            return 0.0;
        else:
            return (float(totalFiles - processedFiles) / float(processedFiles)) * usedTime;

    # process single given file with SPSS template and save to output File
    # returns the time it used up (in seconds)
    @staticmethod
    def runSPSSProcessOnFile(inputFilePath, outputFilePath, config, debuggingResultQueue):
        #create dedicated TK instance; tk _always_ requires a window, however we just want message Boxes
        # create and hide main window
        root = tk.Tk()
        root.withdraw()

        start_time = time.time()
        
        print(Lang.get("Processing "), inputFilePath, "...");
        
        fileName = os.path.basename(inputFilePath);
        inputFileNameMatch = re.match(config.opt['inputRegexPattern'], fileName)

        # read in commands
        spssCommands = '';
        allCommands = '';
        try:
            with io.open(config.opt['spssFile'], "r", encoding='utf8') as f:
                if(f == None):
                    BatchProcessor.err(Lang.get("Unable to obtain file handle for SPSS file"))
                else:
                    spssCommands = f.read()
            #by definition, commands end with "." and a newline
            spssCommands = spssCommands.split(".\n");
        except:
            BatchProcessor.err(Lang.get("Unable to open SPSS file"))

        inputPath, fileName = os.path.split(inputFilePath);
        # set special placeholders
        config.opt['placeholders']['INFILE'] = inputFilePath;
        # input Path doesn't have a trailing slash
        config.opt['placeholders']['INPUTDIR'] =  inputPath + '/';
        config.opt['placeholders']['OUTPUTFILE'] = outputFilePath;
        # output Path doesn't have a trailing slash
        config.opt['placeholders']['OUTPUTDIR'] = config.opt['outputDir'] + '/';
        config.opt['placeholders']['fileName'] = basename(inputFilePath);

        # incorporate the capture groups in the input file name into REGEX file
        # get groupnames themselves
        for grpName, grpValue in inputFileNameMatch.groupdict().iteritems():
            config.opt['placeholders'][grpName] = grpValue;

        #execute file command by command
        for command in spssCommands:
            #ignore encoding line
            if(command.find('Encoding') != -1):
                continue;

            #replace placeholders
            for placeholderKey, substitute in config.opt['placeholders'].iteritems():
                command = command.replace("<" + placeholderKey + ">", substitute);

            #submit command itself to SPSS
            # TODO: deal with errors, how? Currently, they show up in console. Probably best way to go anyway.
            if(not(config.opt['simulateProcessing'])):
                print(Lang.get("Executing: "), command);
                #spss.Submit(command + ".");
            else:
                allCommands += command + ".\n";

        usedTime = (time.time() - start_time);

        debuggingResultQueue.put({'placeholders' : config.ObjToJSON(config.opt['placeholders']), 'commands' :
            allCommands});

        return usedTime;

    @staticmethod
    def err(errMsg):
        tk.messagebox.showerror(Lang.get("Error"), errMsg)

    def defineDefaultPlaceholders(self, inputFilePath):
        inputPath, fileName = os.path.split(inputFilePath);
        # set special placeholders
        self.config.opt['placeholders']['INFILE'] = inputFilePath;
        # input Path doesn't have a trailing slash
        self.config.opt['placeholders']['INPUTDIR'] = inputPath + '/';
        # output Path doesn't have a trailing slash
        self.config.opt['placeholders']['OUTPUTDIR'] = self.config.opt['outputDir'] + '/';
        self.config.opt['placeholders']['fileName'] = basename(inputFilePath);

    # constructs output file path from given path and inputRegexPattern; also populates inputFileNameMatch
    def getOutputFilePath(self, oldFilePath):
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
            except IndexError:
                BatchProcessor.err(Lang.get("Placeholder in ouput file pattern refers to a placeholder which has not been defined"));

            # perhaps the placeholder is not in use after all (defined but not populated)
            if(replacement != None):
                outputFileName = outputFileName.replace(unicode('<' + placeholder + '>'), replacement)
        return self.config.opt['outputDir'] + '/' + outputFileName


    def parseCommandLine(self):
        self.parser = argparse.ArgumentParser(description= Lang.get('Applies an SPSS file on a given set of files'))
        self.parser.add_argument('--config', dest='passedConfigurationFile', 
                            help=Lang.get('configuration file to load'))
        self.parser.add_argument('--executeAutomatically', action='store_true',
                                 help=Lang.get('begin processing upon startup'))
        self.parser.add_argument('--placeholders', help=Lang.get('specify placeholders as [ph1][valueOf ph1] [ph2] [valueOf '
                                                        'ph2]...'));

        self.commandLineArgs = self.parser.parse_args()

    def loadPredefinedConfiguration(self):
        if(self.commandLineArgs.passedConfigurationFile is not None):
            self.loadConfigFromFile(self.commandLineArgs.passedConfigurationFile);
            self.parseCommandLinePlaceholders();
            if(self.commandLineArgs.executeAutomatically):
                self.selectFiles();
        else:
            self.parseCommandLinePlaceholders();
            if(self.commandLineArgs.executeAutomatically):
                self.err(Lang.get("You cannot specify automatic execution while not providing a configuration. Please provide "
                         "--config"));


    def parseCommandLinePlaceholders(self):
        # group parameters, pH = placeHolder
        pHList = self.commandLineArgs.placeholders;
        N = 2;
        if(pHList is not None):
            lst = [pHList[n:n + N] for n in range(0, len(pHList), N)]
        else:
            lst = [];

        #now set placeholders
        for pair in lst:
            key, value = pair[0], pair[1]
            if(placeholderKey in self.config.reservedPlaceholders):
                self.err(Lang.get("You cannot set reserved placeholders: ") + placeholderKey);
            else:
                placeholderKey = '<' + key + '>';
                self.config.opt['placeholders'][placeholderKey] = value;

    #initialize with process and queue; please note that as TK handles _cannot_ be pickled, we need to create
    #structures related to multiprocessing _before_ initializing the GUI (i.e. this class)
    def __init__(self, gui, parent, workerProcess, taskQueue, debuggingResultQueue):
        self.p = workerProcess;
        self.queue, self.debuggingResultQueue = taskQueue, debuggingResultQueue;
        self.config = Configuration();

        parent.title(Lang.get("BatchProcessing"))
        self.gui = gui

        self.inputFiles = [];
        self.parseCommandLine()
        self.loadPredefinedConfiguration()


