from os.path import abspath, dirname
import json
from src.schemas import *
from src.app import db
from src.runner import *
import yaml
logger = logging.getLogger('root')

# Nodes with connection established
runners = {}

def get_builds(job_id, build_id=None):
    try :
        if build_id:
            logger.info(f"[DB Access] Getting build nº {build_id} of job {job_id}")
            build = Build.query.filter_by(job_id=job_id, id=build_id).first()
            build_json=json.dumps(build.to_dict())
            return build_json
        else:
            logger.info(f"[DB Access] Getting all builds on job {job_id}")
            builds = Build.query.filter_by(job_id=job_id)
            builds_json=json.dumps([build.to_dict() for build in builds])
            return builds_json
    except Exception as e:
        logger.info(f"[DB Access] There was a problem trying to get builds\n{e}")
        return json.dumps([])

def create_build(job_id, commands, node_id, description, artifacts):
    job = Job.query.get(job_id)
    node = Node.query.get(node_id)

    id = len(job.builds) + 1
    logger.info(f"New build from job {job_id} will run on node : {node_id}")

    if not node.id in runners:
        logging.info(f"The node {node_id} is not a runner (no connection established)")
        if node.ip_addr == 'localhost':
            logging.info(f"Creating a localhost runner for node {node_id}")
            runners[node.id] = RunerLOCALHOST(node)  # Add to runners dict a new instance
        else:
            logging.info(f"Creating an SSH runner for node {node_id} to IP {node.ip_addr} using configured credentials.")
            runner = RunnerSSH(node)
            runner.connect()
            runners[node.id] = runner
    else:
        logging.info(f"The node {node_id} is already a runner (has a connection established)")

    logger.info(f"[DB Access] Creating build nº : {id} on job {job_id}")
    output, status = runners[int(node_id)].run_commands(commands)

    # Manage archive required artifacts
    if artifacts :
        runners[int(node_id)].get_files(artifacts,
                                        f"{dirname(dirname(dirname(abspath(__file__))))}/artifacts/"
                                        + f"job_{job_id}/build_{id}/", node.workspace)

    db.session.add(Build(id = id, job_id=job_id, commands=commands, output = output,
                         node_id = node_id, description = description, status=status))
    db.session.commit()

def delete_build(job_id, build_id):
    try:
        build = Build.query.filter_by(job_id=job_id, id=build_id).first()
        logger.info(f"[DB Access] Deleting build nº {build_id} from job {job_id}")
        db.session.delete(build)
        db.session.commit()
    except Exception as e:
        return json.dumps([])

def parse_yaml(cmd_file):
    content = yaml.load(cmd_file, Loader=yaml.FullLoader)
    commands = ';'.join([cmd for item in content for cmd in item.get('stage',{}).get('commands',[])])
    artifacts = [item.get('archive') for item in content if item.get('archive')]
    logger.info(f"Parsing command file for new build, commands obtained : {commands}")
    return commands, artifacts