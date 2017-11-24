import socket, time

class Client():
    def __init__(self, host, port, timeout = None):
        self.client = socket.create_connection((host, port))
        self.client.sendall('ping'.encode('utf8'))

    def put(self, name, val, timestamp = str(int(time.time()))):
        print ('put')
        try:
            self.client.send(name)
        finally:
            raise ClientError("PUT method got error")

    def get(self):
        print ('get')


class ClientError(Exception):
    def __init__(self, message):
        super(ClientError, self).__init__(message)


raise ClientError("My hovercraft is full of eels")
#myClient = Client('127.0.0.1',8080);
#myClient.put();