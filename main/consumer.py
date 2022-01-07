# from dotenv import load_dotenv
# import os

from main import Product, db
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
print('--------------------Main Flask Consumer---------------------------')

channel = connection.channel()


channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('--------------------------------------')
    print('Received this data in admin django by rappidmq')
    data = json.loads(body)
    print(data)
    print('--------------------------------------')

    if properties.content_type == "all_products":
        products_ids = db.session.query(Product.id).all()

        db_prod = []
        for i in products_ids:
            db_prod.append(i[0])

        api_data = []
        #####
        for p in data:
            api_data.append(p['id'])
        x = api_data-db_prod
        print(x)
        #####

        # for p in data:
        #     if p['id'] not in db_prod:
        #         product = Product(
        #             id=p['id'], title=p['title'], image=p['image'])
        #         db.session.add(product)
        # db.session.commit()

    if properties.content_type == "product_created":
        product = Product(
            id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created successfully')

    elif properties.content_type == "product_updated":
        product = Product.query.get(data['id'])
        if product:
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product updated successfully')
        else:
            print('Product does not exist !')

    elif properties.content_type == "product_deleted":
        product = Product.query.get(data)
        if product:
            db.session.delete(product)
            db.session.commit()
            print('Product deleted successfully')
        else:
            print('Product does not exist !')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
