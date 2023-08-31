import logging
from functools import partial

import backoff
import pika
from pika.exceptions import AMQPConnectionError
from pydantic import ValidationError

import logging_config  # noqa
from config import settings
from models import EmailNotification
from senders import BaseSender, DebugSender, SendgridSender

logger = logging.getLogger(__name__)


@backoff.on_exception(
    backoff.expo,
    AMQPConnectionError,
    max_time=60,
    backoff_log_level=logging.ERROR,
    raise_on_giveup=True,
    logger=logger,
)
def init_rabbit():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            credentials=pika.PlainCredentials(username=settings.rabbitmq_user, password=settings.rabbitmq_password),
        )
    )
    channel = connection.channel()
    return channel


def send_email(channel, method, properties, body, sender: BaseSender):
    try:
        notification = EmailNotification.parse_raw(body)
    except ValidationError:
        logger.exception("Error on parsing body %s", body)
    else:
        if (msg := sender.send(notification, priority=properties.priority)) is not None:
            resend_properties = pika.BasicProperties(delivery_mode=2, priority=properties.priority)
            channel.basic_publish(
                exchange="", routing_key=settings.email_dlq, properties=resend_properties, body=msg.json()
            )
    finally:
        channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    if settings.debug:
        sender = DebugSender()
    else:
        sender = SendgridSender()
    callback = partial(send_email, sender=sender)

    channel = init_rabbit()

    channel.queue_declare(queue=settings.email_queue, durable=True, arguments={"x-max-priority": 10})
    channel.queue_declare(
        queue=settings.email_dlq,
        durable=True,
        arguments={
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": settings.email_queue,
            "x-message-ttl": settings.retry_interval_ms,
        },
    )
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=settings.email_queue, on_message_callback=callback)

    logger.info("Start listening on queues %s, %s", settings.email_queue, settings.email_dlq)
    channel.start_consuming()


if __name__ == "__main__":
    main()
