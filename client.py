import socket
import threading
import sys
import time

HOST = '18.195.107.195'
PORT = 5378
BUFFER = 4096


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):

        # Connect to the host
        self.connect()

        # Send and receive messages
        thread_send = threading.Thread(target=self.send)
        thread_send.start()

        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()

    def receive(self):
        while True:
            data = self.sock.recv(BUFFER)
            if not data:
                print("Socket is closed.")
                # FIXME should loop to allow another try
                self.disconnect()
            else:
                print(Parser.decode(data))

    def send(self):
        # FIXME Why are the messages not sent? Wrong encoding?
        while True:
            # message = Parser.encode(input())
            # print(message, type(message))
            # self.sock.sendall(message)
            string_bytes = sys.stdin.readline().encode("utf-8")
            # print(string_bytes, type(string_bytes))
            self.sock.send(string_bytes)

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
        except:
            print("Cannot establish connection. Aborting.")
            sys.exit()
        print("Connected to remote host.")

    def disconnect(self):
        self.sock.close()
        print("Disconnected.")
        sys.exit()


class Parser:

    def encode(message):
        '''
        Chat Application Protocol for the CLIENT side:
        <username>  : HELLO-FROM <username>
        @<username> : SEND <username> <message>
        !who        : WHO
        !quit       : QUIT
        '''

        switch = {
            # anything that follows '!' is a command itself
            '!': message[1:].upper(),
            # anything that follows '@' needs to be preceded with 'SEND '
            '@': 'SEND ' + message[1:]
        }

        # Default (starts neither with '!' or '@'): must be first hand-shake (login)
        translated_message = switch.get(message[0], 'HELLO-FROM ' + message)

        # Encode to utf-8
        encoded_message = translated_message.encode('utf-8')

        return encoded_message

    def decode(message):
        '''
        Chat Application Protocol for the SERVER side:
        HELLO           : Successfully logged in as <username>
        WHO-OK          : Available users: <username>, ...
        SEND-OK\n       : Sent successfully.
        UNKNOWN         : Username does not exist
        DELIVERY        : <username>: <message>
        IN-USE          : The username <username> is already taken.
        BUSY            : The total number of users is exceeded. Try later.
        BAD-RQST-HDR    : Unknown command. 
        BAD-RQST-BODY   : Your message contains an error and cannot be sent.
        '''

        # Decode from utf-8 and seperate the words
        decoded_message = message.decode('utf-8')
        decoded_message = decoded_message.split(' ')

        # FIXME Strings have different lenght. Can't hardcode indexes like decoded_message[1],
        #       because SEND-OK has no index of 1 and it will throw an error.
        #       Find a way to go around this issue (index out of bounds) and replace the dynamic
        #       values.

        switch = {
            'HELLO': 'Successfully logged in as <username>',
            'WHO-OK': 'Available users: <username>, ...',
            'SEND-OK\n': 'Sent successfully.',
            'UNKNOWN': 'Username does not exist',
            'DELIVERY': '<username>: <message>',
            'IN-USE': 'The username <username> is already taken. Choose a different one.',
            'BUSY': 'The total number of users is exceeded. Try connecting later.',
            'BAD-RQST-HDR': 'Unknown command.',
            'BAD-RQST-BODY': 'Your message contains an error and cannot be sent.'
        }

        # Look for translation in the switch
        translated_message = switch.get(
            decoded_message[0], 'Unknown response.')

        return translated_message


client = Client()

# FIXME Why can't I exit with ctrl+c?
