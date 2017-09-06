#!/usr/bin/env python
import pika
import threading


class Publisher(object):
    def __init__(self):
        self._count = 10000

    def publisher(self, i):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='exchange_headers', exchange_type='headers')
        channel.queue_declare(queue='headers_queue')

        message = "Hello world!"

        mess = {'name': 'jack',
                'age': '10'}
        properties = pika.BasicProperties(delivery_mode=2, headers=mess)

        while 0 < self._count:
            channel.basic_publish(exchange='exchange_headers', routing_key='', body=message, properties=properties)
            self._count -= 1

        print(" [X] Send %r" % message)

        connection.close()


def main():
    threads = []
    num = 1
    for i in range(0, num):
        pub = Publisher()
        t = threading.Thread(target=pub.publisher, args=(i,))
        threads.append(t)

    for i in range(0, num):
        threads[i].start()

    for i in range(0, num):
        threads[i].join()


if __name__ == '__main__':
    main()


