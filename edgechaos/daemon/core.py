import logging

from edgechaos.listeners.api import ChaosCommandListener

logger = logging.getLogger(__name__)


class EdgeChaosDaemon:

    def __init__(self, chaos_listener: ChaosCommandListener):
        self.chaos_listener = chaos_listener
        self.running = False

    def run(self):
        logger.info('Start edge chaos daemon...')
        self.running = True
        try:
            for cmd in self.chaos_listener.listen():
                if not self.running:
                    break
                logger.debug(f'Received command: {cmd}')
        except Exception as e:
            logger.error(e)
        finally:
            logger.info('Stopping edge chaos daemon...')
            self.stop()

    def stop(self):
        if self.running:
            self.running = False
            self.chaos_listener.stop()
