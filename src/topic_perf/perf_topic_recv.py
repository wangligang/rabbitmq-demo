#!/usr/bin/env python
import threading
import pika
import sys


def consumer(i):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='perf_topic', exchange_type='topic')

    queue_name = 'hello' + str(i)
    channel.queue_declare(queue=queue_name)

    binding_key = 'hello.world.' + str(i)
    channel.queue_bind(exchange='perf_topic', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properities, body):
        #print(" [X] %r:%r" % (method.routing_key, body))
        return

    channel.basic_consume(callback, queue=queue_name, no_ack=True)

    channel.start_consuming()


def main():
    threads = []
    num = 4
    for i in range(0, num):
        t = threading.Thread(target=consumer, args=(i, ))
        threads.append(t)

    for i in range(0, num):
        threads[i].start()
    
    for i in range(0, num):
        threads[i].join()


if __name__ == '__main__':
    main()

