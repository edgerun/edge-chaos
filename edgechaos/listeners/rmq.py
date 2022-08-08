import logging
import os
from typing import Generator

import pika

from edgechaos.executor.api import ChaosCommand
from edgechaos.listeners.api import ChaosCommandListener
from edgechaos.util.env import read_host_env
from edgechaos.util.rmq import connection_from_env, try_setup_exchange, try_setup_queue

logger = logging.getLogger(__name__)

POISON_PILL = 'STOP'


class RabbitMqChaosCommandListener(ChaosCommandListener):

    def __init__(self, exchange: str, routing_key: str, queue_name: str, connection: pika.BlockingConnection):
        self.exchange = exchange
        self.routing_key = routing_key
        self.queue_name = queue_name
        self.connection = connection
        self.running = True

    def listen(self) -> Generator[ChaosCommand, None, None]:
        channel = None
        try:
            channel = self.connection.channel()

            for method_frame, properties, body in channel.consume(queue=self.queue_name, auto_ack=True):
                logger.debug(f'Got message: {body}')
                body = body.decode()
                if body == POISON_PILL:
                    self.running = False
                    break
                try:
                    yield ChaosCommand.from_json(body)
                except Exception as e:
                    logger.error('Reading command failed', e)
        except Exception as e:
            logger.error(f'Listening failed', e)
        finally:
            if channel is not None:
                channel.close()
            self.connection.close()

    def stop(self):
        try:
            self.connection.channel().basic_publish(self.exchange, self.routing_key, bytes(POISON_PILL))
        except Exception as e:
            logger.error('Error happened during stop', e)

    @staticmethod
    def from_env():
        logging.getLogger("pika").setLevel(logging.WARNING)
        connection = connection_from_env()
        edgechaos_host = read_host_env()
        exchange = os.environ.get('edgechaos_rabbitmq_exchange', 'edgechaos')
        try_setup_exchange(connection, exchange)
        queue_name = try_setup_queue(connection, exchange, edgechaos_host)
        return RabbitMqChaosCommandListener(exchange, edgechaos_host, queue_name, connection)
