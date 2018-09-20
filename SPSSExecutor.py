import os
import subprocess
import spss ,spssaux
import sys

from spssaux import u

class SPSSExecutor:

    def execute(self, commands):
        transformedCommands = ['* Encoding: UTF-8.']
        for command in commands:
           # command = command.replace("\n", " ");
            if (len(command) >= 1 and not(command[-1] == '.')):
                command += '.'
            # SPSS probably only understands ASCII
            transformedCommands.append(command)
        #try:
            """
            Execute all commands as batch; this allows to execute BEGIN DUMMY. [...] END DUMMY. as well
            i.e. BEGIN MATRIX. [...] END MATRIX. 
            """
        spss.Submit(transformedCommands)
        #except spss.SpssError as e:
            #raise RuntimeError(str(spss.GetLastErrorMessage()))