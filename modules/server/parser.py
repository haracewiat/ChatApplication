'''
    Parser for the Chat Application Api (SERVER SIDE)
'''


def get_response(message):
    '''
    Chat Application Protocol for the SERVER side:
    HELLO-FROM <username>\n     : handshake 
    SEND <username> <message>\n : send
    WHO\n                       : who
    '''

    # Decode from utf-8 and seperate the words
    message = message.split(' ')
    argument = ['', '']

    if len(message) > 1:
        argument[0] = message[1]
    if len(message) > 2:
        argument[1] = message[2:]

    switch = {
        'HELLO-FROM ' + argument[0] + '\n': return_handshake(message)
    }

    translated_message = switch.get(
        message, return_error(message))

    # Encode to utf-8
    encoded_message = translated_message.encode('utf-8')

    return encoded_message


def return_handshake(message):
    return b'HELLO '
    pass


def return_error(message):
    print('invalid message')
    pass
