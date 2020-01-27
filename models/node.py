import subprocess


class Node:
    _id = 0
    def __init__(self, workspace):
        self.id = Node._id
        self.workspace = ""
        self.ip_addr = ""
        self.port = ""
        self.proto = ""

        Node._id += 1

    def run_commands(cmd_list, workspace):
        output = ""
        for cmd in cmd_list:
            output += subprocess.check_output(f"cd {workspace};" + cmd, shell=True).decode('utf-8')
        return output
