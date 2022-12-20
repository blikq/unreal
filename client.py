import socket, errno
import time
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost', 8090))
request = None
try:
    # while request != 'quit':
        # request = str(input('>> '))
    with open("200k.txt", "r", encoding="utf-8") as f:
        start = time.time()
        for i in f.readlines():
            # print(f.readline())
            try:
                server.send(i.strip().encode('utf8'))
                response = server.recv(1024).decode('utf8')
            except:
                continue
            # print(response)
            # print("done ", count)
            # print(request)
        end = time.time()
        print("finished in {} seconds".format(end-start))
except KeyboardInterrupt:
    server.close()