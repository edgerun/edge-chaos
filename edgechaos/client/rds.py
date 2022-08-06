import logging

import redis

from edgechaos.client.api import ChaosClient
from edgechaos.executor.api import ChaosCommand
from edgechaos.util.rds import redis_from_env, read_channel

logger = logging.getLogger(__name__)


class RedisChaosClient(ChaosClient):

    def __init__(self, channel: str, rds: redis.Redis):
        self.channel = channel
        self.rds = rds

    def send(self, cmd: ChaosCommand):
        msg = ChaosCommand.to_json(cmd)
        self.rds.publish(self.channel, msg)

    @staticmethod
    def from_env():
        channel = read_channel()
        logger.info(f'Client publishes on {channel}')
        return RedisChaosClient(channel, redis_from_env())
