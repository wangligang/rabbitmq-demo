#!/usr/bin/env python
import pika
import threading


def publisher(i):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='perf_fanout', exchange_type='fanout')

    message = 'Hello world!'
    count = 1000000
    while(count > 0):
        channel.basic_publish(exchange='perf_fanout', routing_key='', body=message)
        count -= 1
    print(" [X] Send %r" % message)
    connection.close()

def main():
    threads = []
    num = 4
    for i in range(0, num):
        t = threading.Thread(target=publisher, args=(i, ))
        threads.append(t)

    for i in range(0, num):
        threads[i].start()

    for i in range(0, num):
        threads[i].join()


if __name__ == '__main__':
    main()

