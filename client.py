'''
    1. socket
    2. connect (blocks)
    3. send
    4. receive (blocks)
    5. close

    Requirements:
    1. Connect to the chat server and log in using a unique name.
    2. Ask for another name is the chosen name is already taken.
    3. Shutdown the client by typing !quit.
    4. List all currently logged-in users by typing !who.
    5. Send messages to other users by typing @username message.
    6. Receive messages from other users and display them to the user.

'''

import socket
import threading
import sys
import select

HOST = '18.195.107.195'
PORT = 5378


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.connect()

        # login

        # send & receive
        thread_send = threading.Thread(target=self.send)
        thread_send.start()

        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()

        # disconnect

    def send(self):
        '''
        string_bytes = "Sockets are great!".encode("utf-8")
        self.sock.sendall(string_bytes)
        '''
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

    def receive(self):
        data = self.sock.recv(4096)
        if not data:
            print("Socket is closed.")
        else:
            print("Socket has data.")

    def login(self):
        pass

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
        except:
            print('Cannot establish connection. Aborting.')
            sys.exit()

        print('Connected to remote host.')

    def disconnect(self):
        self.sock.close()


client = Client()
