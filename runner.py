import subprocess
import paramiko
import logging
from pathlib import Path
logger = logging.getLogger('root')

class RunnerSSH():
    def __init__(self, node):
        self.node = node
        self.ssh_client = paramiko.SSHClient()
        self.ftp_client = None

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
            output += stdout.read().decode("utf-8") +  stderr.read().decode("utf-8") + '\n'
            if stderr.channel.recv_exit_status() != 0:
                status = "failed"
        return output, status

    def get_files(self, artifacts, local_path, workspace):
        # Create local path if doesn't exist
        Path(local_path).mkdir(parents=True, exist_ok=True)

        # Init sftp session if not existing yet
        if not self.ftp_client:
            self.ftp_client = self.ssh_client.open_sftp()

        # If wildcard, multiple files will be searched else only the file that matches the path for
        # each artifact
        for artifact in artifacts:
            files = [artifact]
            if '*' in artifact:
                p = Path(artifact)
                _, stdout, _ = self.ssh_client.exec_command(f"find {workspace}/{p.parents[0]} -name '{p.name}'")
                files = stdout.read().decode("utf-8").splitlines()
            for file in files:
                f = Path(file)
                self.ftp_client.get(file, local_path + f.name)

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