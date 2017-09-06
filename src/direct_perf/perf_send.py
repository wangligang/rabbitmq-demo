#!/usr/bin/env python
import threading
import pika


def publisher(i):
    connection =pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'hello' + str(i)
    channel.queue_declare(queue=queue_name)

    message = "Hello world!"
    count = 1000000
    while(count > 0):
        channel.basic_publish(exchange='', routing_key=queue_name, body=message,properties=pika.BasicProperties(delivery_mode=2))
        count -= 1

    #print(" [X] Send %r" % message)
    print(" [X] Send ", count, "messages by ", queue_name)
    connection.close()


def main():
    threads = []
    num = 4
    for i in range(0, num):
        t = threading.Thread(target=publisher, args=(i,))
        threads.append(t)

    for i in range(0, num):
        threads[i].start()

    for i in range(0, num):
        threads[i].join()


if __name__ == '__main__':
    main()


