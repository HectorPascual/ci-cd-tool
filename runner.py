import subprocess
import paramiko

class RunnerSSH():
    def __init__(self, node):
        self.node = node
        self.ssh_client = paramiko.SSHClient()

    def connect(self):
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh_client.connect(self.node.ip_addr, self.node.port, self.node.user, self.node.password)

    def run_commands(self, commands):
        output = ""
        cmd_list = commands.split(';')
        for cmd in cmd_list:
            _ , stdout , _ = self.ssh_client.exec_command(f"cd {self.node.workspace};{cmd}")
            output += str(stdout.read())
        return output


class RunerLOCALHOST():
    def __init__(self, node):
        self.node = node

    def run_commands(self, commands):
        output = ""
        cmd_list = commands.split(';')
        for cmd in cmd_list:
            output += subprocess.check_output(f"cd {self.node.workspace};{cmd}", shell=True).decode('utf-8')
            return output