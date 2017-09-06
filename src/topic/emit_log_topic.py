#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello world!'
channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
print(" [X] Sent %r:%r" % (routing_key, message))

connection.close()

