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


def get_username(message):
    return message.decode('utf-8').split(' ')[1].rstrip()


def get_message(message):
    text = ' '.join(map(str, message.decode('utf-8').split(' ')[2:]))
    print(text)
    return text


def get_active_users(users_list):

    users_list.remove('SERVER')
    users = ','.join(map(str, users_list))

    response = 'WHO-OK ' + users + '\n'

    return bytes(response, 'utf-8')


def verify_handshake(message):
    pass


def verify_send(message):
    pass


def verify_who(message):
    pass

    '''
    Chat Application Protocol for the SERVER side:
    BAD-RQST-BODY\n : Your message contains an error and cannot be sent.
    '''
