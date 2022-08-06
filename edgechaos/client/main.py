import logging
import os
import time

from edgechaos.client.factory import create_client
from edgechaos.executor.api import ChaosCommand

logging.basicConfig(level=os.environ.get('edgechaos_logging_level', 'INFO'))
logger = logging.getLogger(__name__)


def main():
    logger.info('Start client')
    client = create_client()
    if client is None:
        logger.error('Client is None')
        return

    cmd = ChaosCommand('stress-ng', {'cpu': 8}, 'start')
    client.send(cmd)
    time.sleep(5)
    cmd = ChaosCommand('stress-ng', {'cpu': 8}, 'stop')
    client.send(cmd)


if __name__ == '__main__':
    main()
