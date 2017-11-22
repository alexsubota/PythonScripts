import socket, time

class Client():
    def __init__(self, host, port, timeout = None):
        self.client = socket.create_connection((host, port))
        self.client.sendall('ping'.encode('utf8'))

    def put(self, name, val, timestamp = str(int(time.time()))):
        print ('put')

    def get(self):
        print ('get')


class ClientError():
    def __init__(self):
        pass


myClient = Client('127.0.0.1',8080);
myClient.put();