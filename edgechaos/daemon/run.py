import logging
import os
import signal

from edgechaos.daemon.core import EdgeChaosDaemon
from edgechaos.listeners.factory import create_listener

logging.basicConfig(level=os.environ.get('edgechaos_logging_level', 'INFO'))
logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    logger.info('SIGINT received...')
    raise KeyboardInterrupt()


def main():
    listener = create_listener()

    signal.signal(signal.SIGINT, signal_handler)

    if listener is None:
        logger.error(f'Unknown listener type `{os.environ.get("edgechaos_listener_type")}` set')
        return

    chaos_daemon = EdgeChaosDaemon(listener)
    try:
        chaos_daemon.run()
    finally:
        chaos_daemon.stop()


if __name__ == '__main__':
    main()
