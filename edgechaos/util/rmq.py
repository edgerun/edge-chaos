import logging
import os

import pika
from pika import URLParameters

logger = logging.getLogger(__name__)


def connection_from_env():
    # expects connection url: https://pika.readthedocs.io/en/stable/examples/using_urlparameters.html
    url = os.environ.get('edgechaos_rabbitmq_url')
    if url is None:
        raise ValueError('RabbitMq connection url not set')
    connection = pika.BlockingConnection(parameters=URLParameters(url))
    return connection


def try_setup_exchange(connection: pika.BlockingConnection, exchange: str):
    channel = None
    try:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type='topic')
        logger.debug(f'Declared topic  exchange {exchange}')
    except Exception as e:
        logger.error('Error during setting up exchange', e)
        raise e
    finally:
        if channel is not None:
            channel.close()


def try_setup_queue(connection: pika.BlockingConnection, exchange: str, host: str):
    channel = None
    try:
        channel = connection.channel()
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(
            exchange=exchange, queue=queue_name, routing_key=host)
        logger.debug(f'Bound queue ({queue_name}) to exchange ({exchange})')
        return queue_name
    except Exception as e:
        logger.error('Error during setting up queue', e)
        raise e
    finally:
        if channel is not None:
            channel.close()
