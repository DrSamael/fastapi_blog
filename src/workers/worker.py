import pika
import time
import json

from src.database import post_collection

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='tasks_queue', durable=True)
print("Worker started. Waiting for tasks!!!")


def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    print(f" [x] Received task: {data}")

    time.sleep(3)

    print(" [✔] Task processed.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue='tasks_queue',
    on_message_callback=callback
)

channel.start_consuming()
