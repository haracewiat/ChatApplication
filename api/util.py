

def causes_disconnection(message):
    switch = {
        bytes('IN-USE\n', 'utf-8'): True,
        bytes('BAD-RQST-HDR\n', 'utf-8'): True
    }

    return switch.get(message, False)


def is_eol(message):
    if message[-1] == 10:
        return True


def is_ack(message):
    switch = {
        bytes('DELIVERY', 'utf-8'): False
    }

    return switch.get(message, True)
