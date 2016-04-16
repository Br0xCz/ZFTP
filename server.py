import socket
import threading
import json
import os
import unified

lock = threading.Lock()

status = {
    "not found": 0,
    "internal err": 1,
    "dir not set": 2,
    "no root directory": 3,
    "dir is not folder": 4,
    "dir is not file": 5,
}


class Transmitter:
    callable_commands = ('GETFILE', 'CD', 'UP', 'LIST', 'WRITE', 'SIZEOF')
    # callable_commands_dict={'GETFILE':Commands.getfile,}

    default_route = ('C:/Users/kuba')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, adress, port, is_server):
        self.adress = adress
        self.port = port

    def start_server(self):
        self.s.bind((self.adress, self.port))
        self.s.listen(10)
        print('Server is running on adress: ' + str(self.adress) + ' : ' + str(self.port))

        # start a waiting event
        while (True):
            conn, addr = self.s.accept()
            self.t = threading.Thread(target=self.connection_handle, args=(addr, conn))
            self.t.daemon = True
            self.t.start()
            type(conn)

    def connection_handle(self, addr, conn=socket.socket()):
        print('Got connection from ' + addr[0])
        msg = conn.recv(256)
        msg = msg.decode('utf-8')

        request = unified.decode(msg)
        response = self.process_request(request)
        conn.send(response.encode())

    def process_request(self, request):

        if (request['header']['type'] in self.callable_commands):

            kwargs = {'request': request}
            content, data, status = getattr(self, request['header']['type'].lower())(**kwargs)
            # content,data,status=self.Commands.getfile(**kwargs)

            response = {
                'header': {'type': 'OK', 'argument': status}, 'params': {}, 'data': data
            }
            if (not content is None):
                for i in content:
                    response['params'][i] = content[i]
            response['params']['working-directory'] = request['params']['working-directory']
            response['params']['selected-disk'] = request['params']['selected-disk']

            text_response = unified.encode(response)
            return text_response

    ''' Was supposed to add comas to path where vas space, python resolves it for itself
    def surround(self, name_surround):
        return '"'+name_surround+'"'

    def removeSpaces(self, name):
        if(' ' in name):
            if('/' in name):
                temporary=name.split('/')
                for i in range(temporary.lenght):
                    if(' ' in temporary[i]):
                        temporary[i] = self.surround(temporary[i])
                        return '/'.join(temporary)
            return self.surround(name)
        return name
    '''

    '''commands functions'''

    def getfile(self, **kwargs):
        request = kwargs['request']

        if (request['params']['working-directory'] is None):
            return None, None, 3

        selected_disk = request['params']['selected-disk'] + ':/'
        working_directory = request['params']['working-directory'] + '/'
        file_name = request['header']['argument']
        path = selected_disk + working_directory + file_name
        try:
            with open(path, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(e)
            return None, None, 0
        data = data.decode('utf-8')
        dataType = {'data-type': 'bytes'}

        return None, data, 1

    def cd(self, request):
        folder_name = request['header']['argument']+'/'
        selected_disk = request['params']['selected-disk'] + ':/'
        working_directory = request['params']['working-directory'] + '/'
        path=selected_disk+working_directory+folder_name
        print(path)
        print(os.path.isdir(path))
        return None,None, 0

    def list(self, **kwargs):
        '''

        '''
        request = kwargs['request']

        selected_disk = request['params']['selected-disk'] + ':/'
        working_directory = request['params']['working-directory'] + '/'

        path = selected_disk + working_directory

        files = os.listdir(path)

        files_list = list()
        for i in files:
            if (os.path.isdir(path + i)):
                files_list.append((i, True))
            else:
                files_list.append((i, False))
        print(files_list)
        data_json = json.dumps(files_list)

        dataType = {'data-type': 'json'}

        return None, data_json, 0

    def write(self, request):
        pass

    def sizeof(self, request):
        pass


if (__name__ == '__main__'):
    server = Transmitter('0.0.0.0', 1919, True)
    server.start_server()
