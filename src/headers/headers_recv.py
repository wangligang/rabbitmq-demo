#!/usr/bin/env python
import pika
import time
import threading


class Consumer(object):
    def __init__(self):
        self.count = 0

    def consumer(self, i):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='exchange_headers', exchange_type='headers')
        channel.queue_declare(queue='headers_queue')

        def callback(ch, method, properties, body):
            # print(" [X] Receive %r" % body)
            # time.sleep(body.count(b'.'))
            # print('[X] Done')
            self.count += 1
            if (10000 == self.count):
                print('[X] Done. Count = ', self.count)
            return

        mess = {'x-match': 'any',
                'name': 'jack',
                'age': '10'}

        channel.queue_bind(queue='headers_queue', exchange='exchange_headers', arguments=mess)

        channel.basic_consume(callback, queue='headers_queue', no_ack=True)
        channel.basic_qos(prefetch_count=2)

        print(' [*] Waiting for a message. To exit press CTRL+C')
        channel.start_consuming()


def main():
    threads = []
    num = 1
    for i in range(0, num):
        con = Consumer()
        t = threading.Thread(target=con.consumer, args=(i,))
        threads.append(t)

    for i in range(0, num):
        threads[i].start()

    for i in range(0, num):
        threads[i].join()


if __name__ == '__main__':
    main()

