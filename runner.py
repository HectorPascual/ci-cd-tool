import subprocess
import paramiko
import logging

logger = logging.getLogger('root')

class RunnerSSH():
    def __init__(self, node):
        self.node = node
        self.ssh_client = paramiko.SSHClient()

    def connect(self):
        try:
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.ssh_client.connect(self.node.ip_addr, self.node.port, self.node.user, self.node.password)
            logging.info("[SSH] Connection established successfully")
        except Exception as e:
            logging.warning(f'[SSH] There was an error while establishing connection {e}')

    def run_commands(self, commands):
        output = ""
        cmd_list = commands.split(';')
        status = "passed"
        for cmd in cmd_list:
            logging.info(f"Executing shell command : {cmd}")
            _ , stdout , stderr = self.ssh_client.exec_command(f"cd {self.node.workspace};{cmd}")
            output += stdout.read().decode("utf-8") + '\n'
            err = stderr.read().decode("utf-8")
            if err != '':
                status = "failed"
                output += f"Last command executed with error code : {stderr.channel.recv_exit_status()}\n{err}"
                logging.error(err)
        return output, status


class RunerLOCALHOST():
    def __init__(self, node):
        self.node = node

    def run_commands(self, commands):
        output = ""
        cmd_list = commands.split(';')
        status = "passed"
        for cmd in cmd_list:
            logging.info(f"Executing shell command : {cmd}")
            try :
                output += subprocess.check_output(f"cd {self.node.workspace};{cmd}",
                                              stderr=subprocess.STDOUT, shell=True).decode('utf-8')
            except subprocess.CalledProcessError as e:
                logging.error(e)
                status = "failed"
        return output, status