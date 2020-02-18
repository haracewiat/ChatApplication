'''
    Parser for the Chat Application Api.
'''


def encode(message):
    '''
    Chat Application Protocol for the CLIENT side:
    <username>  : HELLO-FROM <username>\n
    @<username> : SEND <username> <message>\n
    !who        : WHO\n
    !quit       : QUIT\n
    '''

    # Case of an invalid message: don't send to the server
    if len(message) == 0:
        return bytes('INVALID\n', 'utf-8')

    switch = {
        '!': message[1:].upper() + '\n',
        '@': 'SEND ' + message[1:] + '\n'
    }

    translated_message = switch.get(
        message[0], 'HELLO-FROM ' + message + '\n')

    # Encode to utf-8
    encoded_message = translated_message.encode('utf-8')

    return encoded_message


def decode(message):
    '''
    Chat Application Protocol for the SERVER side:
    HELLO           : Successfully logged in as <username>
    WHO-OK          : Available users: <username>, ...
    SEND-OK\n       : Sent successfully.
    UNKNOWN\n       : Username does not exist
    DELIVERY        : <username>: <message>
    IN-USE\n        : The username <username> is already taken.
    BUSY\n          : The total number of users is exceeded. Try later.
    BAD-RQST-HDR\n  : Unknown command. 
    BAD-RQST-BODY\n : Your message contains an error and cannot be sent.
    '''

    # Decode from utf-8 and seperate the words
    decoded_message = message.decode('utf-8')
    decoded_message = decoded_message.split(' ')
    argument = ['', '']

    if len(decoded_message) > 1:
        argument[0] = decoded_message[1]
    if len(decoded_message) > 2:
        argument[1] = decoded_message[2:]

    switch = {
        'HELLO': 'Successfully logged in as ' + argument[0],
        'WHO-OK': 'Available users: ' + argument[0],
        'SEND-OK\n': 'Sent successfully.',
        'UNKNOWN\n': 'Username does not exist',
        'DELIVERY':  argument[0] + ': ' + ' '.join(argument[1]),
        'IN-USE\n': 'The username ' + argument[0] + ' is already taken. Choose a different one.',
        'BUSY\n': 'The total number of users is exceeded. Try connecting later.',
        'BAD-RQST-HDR\n': 'Unknown command.',
        'BAD-RQST-BODY\n': 'Your message contains an error and cannot be sent.'
    }

    # Look for translation in the switch
    translated_message = switch.get(
        decoded_message[0], 'Unknown response.')

    return translated_message
