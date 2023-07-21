import pika, json

params = pika.URLParameters('amqps://dwfanozl:Zgno-JgwU0wWrNhSK7pA6mmRMom9TxnP@puffin.rmq2.cloudamqp.com/dwfanozl')

# connection = pika.BlockingConnection(params)
# channel = connection.channel()

# def publish(method, body):
#     properties = pika.BasicProperties(method)
#     channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

connection = None
channel = None

class ConnectionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class PublishError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def establish_connection():
    global connection, channel
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
    except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelClosed) as e:
        print(f"Error while establishing connection: {str(e)}")
        raise ConnectionError('Error while establishing connection.')

def publish(method, body):
    global connection, channel
    try:
        if not connection or not channel or connection.is_closed or channel.is_closed:
            establish_connection()
        properties = pika.BasicProperties(method)
        channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
    except Exception as e:
        print(f"Error while publishing: {str(e)}")
        raise PublishError(str(e))

def close_connection():
    global connection, channel
    try:
        if connection and connection.is_open:
            connection.close()
            channel = None
            connection = None
            print("Connection closed.")
    except Exception as e:
        print(f"Error while closing connection: {str(e)}")

import atexit
atexit.register(close_connection)