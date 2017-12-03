import asyncio


class ClientServerProtocol(asyncio.Protocol):
    myDict = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        strOut = ''
        if resp != 0:
            for key, item in resp.items():
                for t, value in item:
                    strOut += str(key) + ' ' + str(value) + ' ' + str(t) +'\n'
            strOut = strOut + '\n'
            self.transport.write(strOut.encode())

    def process_data(self, data):
        print (data)
        dataSplitted = data.split()
        commandType = dataSplitted[0].upper()
        metricName = dataSplitted[1]
        if commandType == 'PUT':
            try:
                if metricName in ClientServerProtocol.myDict.keys():
                    tempList = ClientServerProtocol.myDict.get(metricName)
                    if (dataSplitted[3], dataSplitted[2]) not in tempList:
                        tempList.append((dataSplitted[3], dataSplitted[2]))
                else:
                    tempList = [(dataSplitted[3], dataSplitted[2])]
                tempDict = {metricName: tempList}
                ClientServerProtocol.myDict = {**ClientServerProtocol.myDict, **tempDict}
                self.transport.write('ok\n\n'.encode())
                return 0
            except:
                self.transport.write('error\n\n'.encode())
                return 0
        elif commandType == 'GET':
            try:
                if metricName == '*':
                    self.transport.write('ok\n'.encode())
                    return ClientServerProtocol.myDict
                else:
                    if ClientServerProtocol.myDict.get(metricName):
                        self.transport.write('ok\n'.encode())
                        return {metricName: (ClientServerProtocol.myDict.get(metricName))}
                    else:
                        self.transport.write('ok\n\n'.encode())
                        return 0
            except:
                self.transport.write('error\n\n'.encode())
                return 0
        else:
            self.transport.write('error\n'.encode())
            self.transport.write('wrong command\n\n'.encode())
            return 0


def run_server(host, port):
    loop = asyncio.get_event_loop()
    print('Start server')
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()