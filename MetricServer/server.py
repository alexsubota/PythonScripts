import asyncio


class ClientServerProtocol(asyncio.Protocol):
    myDict = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        if resp:
            self.transport.write(resp.encode())
        self.transport.close()

    def process_data(self, data):
        dataSplitted = data.split()
        commandType = dataSplitted[0].upper
        metricName = dataSplitted[1]
        if commandType == 'PUT':
            try:
                if metricName in self.myDict:
                    tempList = self.myDict.get(metricName)
                    tempList.append((dataSplitted[2], dataSplitted[3]))
                else:
                    tempList = [(dataSplitted[2], dataSplitted[3])]
                tempDict = {metricName: tempList}
                self.myDict = {**self.myDict, **tempDict}
                self.transport.write('ok')
            except:
                self.transport.write('error')
        elif commandType == 'GET':
            try:
                self.transport.write('ok')
                if metricName == '*':
                    return self.myDict
                else:
                    return self.myDict.get(metricName)
            except:
                self.transport.write('error')
        else:
            self.transport.write('error')
            self.transport.write('wrong command')

loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8888
)

server = loop.run_until_complete(coro)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()