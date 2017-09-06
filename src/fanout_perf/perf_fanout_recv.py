#!/usr/bin/env python
import pika
import threading
import sys


def consumer(i):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='perf_fanout', exchange_type='fanout')

    #queue_name = 'fanout' + str(i)
    param = ''.join(sys.argv[1:])
    queue_name = 'fanout' + param

    channel.queue_declare(queue=queue_name)

    channel.queue_bind(exchange='perf_fanout', queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        #print(" [X] %r"% body)
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

