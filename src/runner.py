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
        found_artifacts = 0
        for artifact in artifacts:
            files = []
            if '*' in artifact:
                p = Path(artifact)
                _, stdout, stderr = self.ssh_client.exec_command(f"find {workspace}/{p.parents[0]} -name '{p.name}'")
                if stderr.channel.recv_exit_status() != 0 :
                    logger.error(f"Failed collecting artifact in path ({artifact})")
                else :
                    files = stdout.read().decode("utf-8").splitlines()
            else:
                if Path(artifact).exists():
                    files = [artifact]
                else:
                    logger.error(f"Failed collecting artifact in path ({artifact})")
            for file in files:
                f = Path(file)
                try:
                    self.ftp_client.get(file, local_path + f.name)
                except FileNotFoundError as e:
                    logger.error(f"Failed collecting artifact in path ({file}) with error : {e}")
                    Path(local_path + f.name).unlink()
            found_artifacts += len(files)

        logger.info(f"Collected {found_artifacts} artifacts.")
        if found_artifacts == 0 :
            Path(local_path).rmdir()
        return found_artifacts

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