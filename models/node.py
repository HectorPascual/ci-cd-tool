import subprocess

class Node:
    _id = 0
    def __init__(self, ip_addr, workspace):
        self.id = Node._id
        self.workspace = workspace
        self.ip_addr = ip_addr
        self.proto = ""

        Node._id += 1

    def __iter__(self):
        return iter(vars(self))

    def run_commands(self, cmd_list):
        output = ""

        for cmd in cmd_list:
            output += subprocess.check_output(f"cd {self.workspace};" + cmd, shell=True).decode('utf-8')
        return output
