import pika, json

params = pika.URLParameters('amqps://dwfanozl:Zgno-JgwU0wWrNhSK7pA6mmRMom9TxnP@puffin.rmq2.cloudamqp.com/dwfanozl')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)