import os
from typing import Optional

from edgechaos.client.api import ChaosClient
from edgechaos.client.rds import RedisChaosClient


def create_client() -> Optional[ChaosClient]:
    if os.environ.get('chaosedge_client_type') == 'redis':
        return RedisChaosClient.from_env()
    else:
        return None
