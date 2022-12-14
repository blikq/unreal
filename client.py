import socket, errno
# import time
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


# start = time.time()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost', 1556))
request = None

try:
    while request != 'quit':
        request = str(input('>> '))
        if request:
            try:
                server.send(request.encode('utf8'))
                response = server.recv(255).decode('utf8')
            except socket.error as e:
                print("problem occurred")

            if response:
                print(response)
            # with open("200k.txt", 'r', encoding='utf-8') as reques:
            #     for request in reques.readlines():
            #         server.send(request.encode('utf8'))
            #         response = server.recv(255).decode('utf8')
            #         print(response.encode('utf8'))
except KeyboardInterrupt:
    server.close()