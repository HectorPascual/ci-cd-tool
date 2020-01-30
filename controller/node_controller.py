import json
import logging
from schemas import Node
from app import db

logger = logging.getLogger('root')


def get_nodes(node_id=None):
    try :
        if node_id:
            logger.info(f"[DB Access] Getting node : {node_id}")
            node = Node.query.get(node_id)
            node_json = json.dumps(node.to_dict())
            return node_json
        else:
            logger.info(f"[DB Access] Getting all nodes")
            nodes = Node.query.all()
            nodes_json=json.dumps([node.to_dict() for node in nodes])
            return nodes_json
    except Exception as e:
        logger.info(f"[DB Access] There was a problem trying to get nodes\n{e}")
        print(e)
        return json.dumps([])

def create_node(workspace, ip_addr, port, user=None, password=None):
    node = Node(workspace=workspace, ip_addr=ip_addr, port=port, user=user, password=password)
    logger.info(f"[DB Access] Creating node : {node}")
    db.session.add(node)
    db.session.commit()

def delete_node(node_id):
    try:
        node = Node.query.get(node_id)
        logger.info(f"[DB Access] Deleting node {node_id}")
        db.session.delete(node)
    except Exception as e:
        return json.dumps([])
