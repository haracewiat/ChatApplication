def is_eol(message):
    if message[-1] == 10:
        return True


def is_valid(message):

    switch = {
        b'HELLO-FROM': verify_handshake(message),
        b'WHO': verify_who(message),
        b'SEND': verify_send(message)
    }

    return switch.get(message[0], False)


def get_header(message):
    return message.decode('utf-8').split(' ')[0]


def get_recipient(message):
    return message.decode('utf-8').split(' ')[1]


def get_message(message):
    return message.decode('utf-8').split(' ')[2]


def verify_handshake(message):
    pass


def verify_send(message):
    pass


def verify_who(message):
    pass

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
