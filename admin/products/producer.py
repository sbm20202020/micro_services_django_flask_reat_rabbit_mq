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
    pika.ConnectionParameters(host="10.10.0.200", heartbeat=0))

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key='admin', body=json.dumps(body), properties=properties)


def send_all(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
