import socket, time, string
#https://www.coursera.org/learn/programming-in-python/programming/aG3x3/kliient-dlia-otpravki-mietrik
class Client():
    def __init__(self, host, port, timeout = None):
        self.client = socket.create_connection((host, port))

    def put(self, name, val, timestamp = str(int(time.time()))):
        myStr = 'put ' + str(name) + ' ' + str(val) + ' ' + str(timestamp) + '\n'
        self.client.send(myStr.encode())
        data = self.client.recv(1024).decode()
        if data.split()[0] == 'error':
            raise ClientError('MYERROR')

    def get(self, *args):
        #try:
        for item in args:
            myStr = 'get ' + str(item) + '\n'
            self.client.send(myStr.encode())
            data = self.client.recv(1024).decode()
            if data.split()[0] != 'error':
                dataSplit = data.split()
                retDict = {}
                tempDict = {}
                curPos = 1
                while curPos < len(dataSplit):
                    tempList = []
                    if dataSplit[curPos] in tempDict:
                        tempList= retDict.get(dataSplit[curPos])
                    tempList.append((int(dataSplit[curPos + 2]), float(dataSplit[curPos + 1])))
                    tempDict = {dataSplit[curPos] : tempList}
                    retDict = {**retDict, **tempDict}
                    curPos += 3
            else:
                raise ClientError('MYERROR')
        return retDict


class ClientError(Exception):
    def __init__(self, message):
        super(ClientError, self).__init__(message)