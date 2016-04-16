def decode(msg):

    msg = msg.split('\n')

    command,command_argument= str(msg[0]).split(' ', 1)
    i = 0

    for line in msg[1:-1]:
        if line == '' or line == msg[-1]:
            break
        i += 1
    arguments_temp = msg[1:i+1]
    arguments = dict()
    for j in arguments_temp:
        argument_name, argument_content=j.split(':')
        arguments[argument_name] = argument_content

    if msg[i] == msg[-1]:
        content = None
    elif msg[i+2] == msg[-1]:
        content=msg[-1]
    else:
        content = '\n'.join(msg[i+2:-1])


    request = dict()
    request['header']=dict()
    request['header']['type'] = command
    request['header']['argument'] = command_argument
    request['params'] = arguments
    request['data'] = content

    return request


def encode(response):
    text_response = response['header']['type']+' '+str(response['header']['argument'])+'\n'

    for i in response['params']:
        text_response += i + ':' + response['params'][i] + '\n'
    text_response += '\n'

    if not response['data'] is None:
        text_response += response['data']

    return text_response
