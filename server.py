import socket
import threading
import json
import os
import unified
import platform

SYSTEM = platform.system()

print('master test')

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
        msg = conn.recv(2048)
        msg = msg.decode('utf-8')

        request = unified.decode(msg)
        response = self.process_request(request)
        conn.send(response.encode('utf-8'))
        conn.close()

    def process_request(self, request):


        if request['header']['type'] in self.callable_commands:

            kwargs = {'request': request}

            content, data, status =self.functions[request['header']['type'].lower()](self,**kwargs)

            response = {
                'header': {'type': 'OK', 'argument': status}, 'params': {}, 'data': data
            }
            if not(content is None):
                for i in content:
                    response['params'][i] = content[i]
            response['params']['working-directory'] = request['params']['working-directory']
            response['params']['selected-disk'] = request['params']['selected-disk']
            text_response = unified.encode(response)

            return text_response



    '''commands functions'''

    def exists(self, path):
        return os.path.isdir(path)

    def makepath(self, disk, directory):

        if SYSTEM == 'Linux':
            return '/' + directory
        elif SYSTEM == 'Windows':
            return disk + directory

    def getfile(self, **kwargs):
        request = kwargs['request']

        if (request['params']['working-directory'] is None):
            return None, None, 3

        selected_disk = request['params']['selected-disk'] + ':/'
        working_directory = request['params']['working-directory'] + '/'
        file_name = request['header']['argument']
        path = self.makepath(selected_disk, working_directory) + file_name
        try:
            with open(path, 'rb') as f:
                data = f.read()
        except Exception as e:
            print(e)
            return None, None, 0
        #data = data.decode('utf-8')
        dataType = {'data-type': 'bytes'}

        return None, str(data), 1

    def cd(self, **kwargs):
        request = kwargs['request']
        if request['header']['argument'] == '..' and '/' in request['params']['working-directory']:
            try:
                path = request['params']['working-directory'].split('/')
                path = '/'.join(path[0:-1])
                print(path)
                directory = {'working-directory': path}
                return directory, None, 0

            except Exception as e:
                print('Boep error')

        elif not ('/' in request['header']['argument']):
            pass

        folder_name = request['header']['argument'] + '/'
        selected_disk = request['params']['selected-disk'] + ':/'
        working_directory = request['params']['working-directory'] + '/'
        path = self.makepath(selected_disk, working_directory) + folder_name
        print(path)
        print(os.path.isdir(path))
        directory = {'working-directory': working_directory + folder_name}
        return None, None, 0

    def list(self, **kwargs):
        """
        empty for now
        """
        request = kwargs['request']

        selected_disk = request['params']['selected-disk'] + ':/'
        working_directory = request['params']['working-directory'] + '/'

        path = self.makepath(selected_disk, working_directory)

        files = os.listdir(path)

        files_list = list()
        for i in files:
            if os.path.isdir(path + i):
                files_list.append((i, True))
            else:
                files_list.append((i, False))

        data_json = json.dumps(files_list, ensure_ascii=False)
        dataType = {'data-type': 'json'}

        return None, data_json, 0

    def write(self, **kwargs):
        print('error')

        request = kwargs['request']
        selected_disk = request['params']['selected-disk'] + ':/'
        working_directory = request['params']['working-directory'] + '/'
        file_name = request['header']['argument']

        path = self.makepath(selected_disk, working_directory) + file_name

        if request['params']['write-type'] is not None:
            if request['params']['write-type'] == 'overwrite':
                path = self.makepath(selected_disk, working_directory) + file_name
                if self.exists(path):
                    with open(path, 'w') as f:
                        f.write(request['data'])

            elif request['params']['write-type'] == 'create-new':
                path = self.makepath(selected_disk, working_directory)
                if self.exists(path) and not self.exists(path + file_name):
                    with open(path + file_name, 'w') as f:
                        print('Succesfully opened')

        pass

    def sizeof(self, request):
        pass

    functions = {
        'write':write,
        'getfile':getfile,
        'cd':cd,
        'list':list,
        'sizeof':sizeof,
    }


if __name__ == '__main__':
    server = Transmitter('0.0.0.0', 1919, True)
    server.start_server()
