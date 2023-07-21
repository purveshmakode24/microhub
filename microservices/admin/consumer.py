import pika, json

import os, django
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')

# Configure Django settings
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://dwfanozl:Zgno-JgwU0wWrNhSK7pA6mmRMom9TxnP@puffin.rmq2.cloudamqp.com/dwfanozl')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(channel, method, properties, body):
    print('Received in admin!')
    data = json.loads(body)
    print(data)
    product = Product.objects.get(id=data)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased.')

    # Acknowledge the message after successful processing and committing
    channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=False)

print('Started Consuming...')

channel.start_consuming()

channel.close()