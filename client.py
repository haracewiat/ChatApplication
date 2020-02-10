import socket
import threading
import sys
import time

HOST = '18.195.107.195'
PORT = 5378
BUFFER = 4096


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    thread_list = []
    socket_closed = False
    login_correct = False

    def __init__(self):
        self.connect()
        self.login()
        thread_receive = threading.Thread(target=self.receive,  daemon=True)
        thread_receive.start()
        if not self.socket_closed:
            self.wait_for_command()
        else:
            sys.exit()

    def receive(self):
        while True:
            data = self.sock.recv(BUFFER)
            if not data:
                print("Socket is closed.")
                self.socket_closed = True
                break
                # FIXME if user exists, print is executed endlessly
            else:
                print(data.decode("utf-8"))
        sys.exit()

    def send_as_bytes(self, send_this):
        send_this_as_bytes = send_this.encode("utf-8")
        self.sock.send(send_this_as_bytes)

    def login(self):
        print("First, let's log in. Type in your name:")
        name = input()
        if name == "!quit":
            self.quit_command(name)
        send_login = "HELLO-FROM " + name + "\n"
        self.send_as_bytes(send_login)
        #login_response_as_bytes = self.sock.recv(BUFFER)
        #login_response = login_response_as_bytes.decode("utf-8")
        #print(login_response)
        #if login_response == "IN-USE\n":
         #   print(login_response)
          #  print("Try another name: ")
           # newname = input()
            #if newname == "quit":
             #   self.quit_command()
            #send_login = "HELLO-FROM " + name + "\n"
            #self.send_as_bytes(send_login)


    def wait_for_command(self):
        command = input()
        if command == "!quit":
            self.quit_command(command)
        elif command == "!who":
            self.who_command(command)
        elif command[0] == '@':
            self.send_command(command[1:])

    def who_command(self, command):
        send_who = "WHO\n"
        self.send_as_bytes(send_who)
        self.wait_for_command()

    def quit_command(self, command):
        self.disconnect()

    def send_command(self, command):
        name, msg = command.split(' ', 1)
        send_msg = "SEND " + name + " " + msg + "\n"
        self.send_as_bytes(send_msg)
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
        print("Closed socket. Exiting...")
        sys.exit()


client = Client()
