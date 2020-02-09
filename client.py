import socket
import threading
import sys
import time

HOST = '18.195.107.195'
PORT = 5378
BUFFER = 4096


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #thread_receive = threading.Thread

    def __init__(self):
        self.connect()

        self.login()

        # send & receive

        #thread_send = threading.Thread(target=self.send)
        #thread_send.start()

        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()

        self.wait_for_command()

        #thread_wait_for_command = threading.Thread(target=self.wait_for_command)
        #thread_wait_for_command.start()

        # disconnect
        self.disconnect()

    def send(self):
        while True:
            string_bytes = sys.stdin.readline().encode("utf-8")
            self.sock.send(string_bytes)

    def receive(self):
        while True:
            data = self.sock.recv(BUFFER)
            if not data:
                print("Socket is closed.")
                #time.sleep(1)
                #self.wait_for_command()
                # FIXME if user exists, print is executed endlessly
            else:
                print(data.decode("utf-8"))
                #time.sleep(1)
                #self.wait_for_command()
                # time.sleep(10)

    def login(self):
        print("First, let's log in. Type in your name:")
        name = input()
        send_login = "HELLO-FROM " + name + "\n"
        send_login_as_bytes = send_login.encode("utf-8")
        self.sock.send(send_login_as_bytes)

    def wait_for_command(self):
        #print("Type a command:")
        command = input()
        if command == "!quit":
            self.quit_command(command)
        elif command == "!who":
            self.who_command(command)
        elif command[0] == '@':
            self.send_command(command[1:])

    def who_command(self, command):
        #print("who command here")
        send_who = "WHO\n"
        send_who_as_bytes = send_who.encode("utf-8")
        self.sock.send(send_who_as_bytes)
        self.wait_for_command()
        # self.receive()

    def quit_command(self, command):
        print("QUIT")
        self.disconnect()
        sys.exit()

    def send_command(self, command):
        name, msg = command.split(' ', 1)
        send_msg = "SEND " + name + " " + msg + "\n"
        send_msg_as_bytes = send_msg.encode("utf-8")
        self.sock.send(send_msg_as_bytes)
        self.wait_for_command()

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
        except:
            print('Cannot establish connection. Aborting.')
            sys.exit()

        print('Connected to remote host.')

    def disconnect(self):
        self.sock.close()
        sys.exit()


client = Client()
