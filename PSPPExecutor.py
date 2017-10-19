import os
import subprocess

class PSPPExecutor:

    def execute(self, commands):
        commandsTxt = os.linesep.join(commands)
        #write all commands to file
        with open("cmd.txt", "w") as cmd_file:
            cmd_file.write(commandsTxt)
            cmd_file.close()
            subprocess.check_output(['pspp', './cmd.txt'])