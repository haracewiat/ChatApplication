def contains_eol(message):
    if message.decode('utf-8').find('/n'):
        return True


def extract(message):
    return message.decode('utf-8').split('/n')


def remove(text, message):
    new_message = message.decode('utf-8')
    if text:
        for t in text:
            new_message.replace(t, '')

    return bytes(new_message, 'utf-8')


def get_header(message):
    return message.decode('utf-8').split(' ')[0]


def get_recipient(message):
    return message.decode('utf-8').split(' ')[1]


def get_username(message):
    return message.decode('utf-8').split(' ')[1].rstrip()


def get_message(message):
    text = ' '.join(map(str, message.decode('utf-8').split(' ')[2:]))
    return text


def get_active_users(users_list):

    users_list.remove('SERVER')
    users = ','.join(map(str, users_list))

    response = 'WHO-OK ' + users + '\n'

    return bytes(response, 'utf-8')
