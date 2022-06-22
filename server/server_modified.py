import socket
from threading import Thread

# server's IP address

test = 'ok'
SERVER_HOST = "192.168.178.130"

computerRun = input('Server running on pc? [y/n] ')
if computerRun == 'y' or computerRun == 'Y':
    SERVER_HOST = socket.gethostbyname(socket.gethostname())
else:
    pass

SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print('CoreOS chat server active')
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
   """
   This function keep listening for a message from `cs` socket
   Whenever a message is received, broadcast it to all other connected clients
   """
   while True:
       try:
           # keep listening for a message from `cs` socket
           msg = cs.recv(1024).decode()
       except Exception as e:
           # client no longer connected
           # remove it from the set
           print(f"[!] Error: {e}")
           client_sockets.remove(cs)
       else:
           # if we received a message, replace the <SEP>
           # token with ": " for nice printing
           msg = msg.replace(separator_token, ": ")
       # iterate over all connected sockets
       for client_socket in client_sockets:
           # and send the message
           print(f'\n{msg}')
           client_socket.send(msg.encode())


while True:
   client_socket, client_address = s.accept()
   print(f"[+] {client_address} connected.")
   client_sockets.add(client_socket)
   t = Thread(target=listen_for_client, args=(client_socket,))
   t.daemon = True
   t.start()

# close client sockets
for cs in client_sockets:
   cs.close()
# close server socket
s.close()


