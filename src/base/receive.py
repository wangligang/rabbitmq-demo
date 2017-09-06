#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [X] Receive %r" % body)

channel.basic_consume(callback, queue='hello', no_ack=True)

print(' [*] Waiting for a message. To exit press CTRL+C')

channel.start_consuming()
