import socket
import random
from os import system
from threading import Thread
from datetime import datetime

serverHostInput = '192.168.178.130'
serverPortInput = '5002'

print('------------------------------------------')
defaultInput = input('Default Server? [y/n] ')
if defaultInput == 'y' or defaultInput == 'Y':
    pass
else:
    serverHostInput = str(input('Enter IP of server host:   '))
    serverPortInput = str(input('Enter Port of server host: '))


SERVER_HOST = serverHostInput
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message


s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
name = input("Enter your name: ")
system('cls')
print('-----------------------------------------------------------------')
print(f'[Server IP: {serverHostInput}] [Server Port: {serverPortInput}] ')
print('[Status: Connected]                             LCD Server Client')
print('-----------------------------------------------------------------\n')


def listen_for_messages():
   while True:
       message = s.recv(1024).decode()
       print("\n" + message)

# make a thread that listens for messages to this client & print them
# make the thread daemon so it ends whenever the main thread ends
t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

# start the thread
while True:
   message =  input()
   # put functions here
   if message.lower() == 'q':
       break
   date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   message = f"[{date_now}] {name}{separator_token}{message}"
   s.send(message.encode())

s.close()

