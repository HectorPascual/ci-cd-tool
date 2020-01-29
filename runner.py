import subprocess
from schemas import Node

class RunnerSSH():
    def __init__(self, node):
        self.node = node

    def connect(self):
        pass
    def run_commands(self):
        pass


class RunerLOCALHOST():
    def __init__(self, node):
        self.node = node

    def run_commands(self, commands):
        output = ""
        cmd_list = commands.split(';')
        for cmd in cmd_list:
            output += subprocess.check_output(f"cd {self.node.workspace};{cmd}", shell=True).decode('utf-8')
            return output