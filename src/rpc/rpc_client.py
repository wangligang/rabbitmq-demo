#!/usr/bin/env python
import pika
import uuid
import time


class FibonacciRpcClient(object):
    def __init__(self):
        self.count = 0
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                   correlation_id=self.corr_id),
                                   body=str(n))

        self.begin = time.time()
        while self.response is None:
            self.count += 1
            self.connection.process_data_events()
        self.end = time.time()
        print(" [#] cost time %r" % (self.end-self.begin))
        return int(self.response)

    def get_counts(self):
        return self.count

fibonacci_rpc = FibonacciRpcClient()

print(" [X] Requesting fib(10)")
response = fibonacci_rpc.call(10)
print(" [.] Got %r" % response)
count = fibonacci_rpc.get_counts()
print(" [.] Count: %d" % count)
