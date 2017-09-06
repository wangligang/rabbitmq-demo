#!/usr/bin/env python
import threading
import pika


def consumer(i):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'hello' + str(i)
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        #print(" [X] Receive %r" % body)
        #print( '[X] Done')
        return 

    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.basic_qos(prefetch_count=2)

    print(' [*] Waiting for a message. To exit press CTRL+C')

    channel.start_consuming()


def main():
    threads = []
    num = 4
    for i in range(0, num):
        t = threading.Thread(target=consumer, args=(i,))
        threads.append(t)

    for i in range(0, num):
        threads[i].start()
    
    for i in range(0, num):
        threads[i].join()


if __name__ == '__main__':
    main()

