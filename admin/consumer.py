# from dotenv import load_dotenv
# import os

import pika
import json

# Get variables from .env file
# load_dotenv(override=True)

# docker exec -ti rabbitmq sh
# /# hostname -i to get ip adresse of rabbitmq server in this case IP_ADD_RABBIT_MQ in .env file
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(os.getenv("IP_ADD_RABBIT_MQ")))
connection = pika.BlockingConnection(
    pika.ConnectionParameters("10.10.0.200"))
print('-----------------------------------------------')
print('--------------------Admin Consumer---------------------------')

channel = connection.channel()


channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('--------------------------------------')
    print('Received this in admin')
    data = json.loads(body)
    print(data)
    print('--------------------------------------')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
