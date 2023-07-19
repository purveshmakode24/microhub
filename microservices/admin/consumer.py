import pika

params = pika.URLParameters('amqps://dwfanozl:Zgno-JgwU0wWrNhSK7pA6mmRMom9TxnP@puffin.rmq2.cloudamqp.com/dwfanozl')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(channel, method, properties, body):
    print('Recived in admin!')
    print(body)

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming...')

channel.start_consuming()

channel.close()