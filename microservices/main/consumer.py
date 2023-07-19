import pika, json
from main import Product, db, app

params = pika.URLParameters('amqps://dwfanozl:Zgno-JgwU0wWrNhSK7pA6mmRMom9TxnP@puffin.rmq2.cloudamqp.com/dwfanozl')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(channel, method, properties, body):
    print('Recived in main!')
    data = json.loads(body)
    print('data:', data)

    with app.app_context():
        if properties.content_type == 'product_created':
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product Created!')

        elif properties.content_type == 'product_updated':
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product Updated!')

        elif properties.content_type == 'product_deleted':
            product = Product.query.get(data)  # Here data is Id
            db.session.delete(product)
            db.session.commit()
            print('Product Deleted!')

    # Acknowledge the message after successful processing and committing
    channel.basic_ack(delivery_tag=method.delivery_tag)

# auto-ack=False (by default) to make sure messages are not lost incase of consumer system failure.
channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=False)

print('Started Consuming...')

channel.start_consuming()

channel.close()