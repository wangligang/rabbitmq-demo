#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello world!"
channel.basic_publish(exchange='', routing_key='task_queue', body=message,properties=pika.BasicProperties(delivery_mode=2))

print(" [X] Send %r" % message)

connection.close()

