import os
import subprocess
import spss
import sys

class SPSSExecutor:

    def execute(self, commands):
        transformedCommands = []
        for command in commands:
            command = command.replace("\n", " ");
            if (not (command[-1] == '.')):
                command += '.'
            transformedCommands.append(command)
        try:
            """
            Execute all commands as batch; this allows to execute BEGIN DUMMY. [...] END DUMMY. as well
            i.e. BEGIN MATRIX. [...] END MATRIX. 
            """
            spss.Submit(transformedCommands)
        except spss.SpssError as e:
            raise RuntimeError(str(spss.GetLastErrorMessage()))