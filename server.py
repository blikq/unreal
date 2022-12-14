import asyncio
import socket
import threading
import logging
import time
from signal import signal, SIGPIPE, SIG_DFL

logging.basicConfig(filename="log.txt")
level=logging.INFO


async def read_config(query: str, is_true: dict):
    with open("config.txt", 'r', encoding="utf-8") as config_file:
        # Read each line of the config file
        for line in config_file:
            if line.strip().startswith("linuxpath="):
                # Remove the prefix "linuxpath=" and strip any whitespace
                file_path = line.removeprefix('linuxpath=').strip()
                # Open the file specified in the config line and check if the query appears in it
                try:
                    with open(file_path, 'r') as query_file:
                        if query_file.read().find(query) != -1:
                            is_true.update({"is_true": "STRING EXISTS"})
                            return None
                        else:
                            pass
                except Exception as e:
                    # logging.exception(e)
                    pass
    is_true.update({"is_true": "STRING NOT FOUND"})

# thread1 = threading.Thread(target = read_config, args = ()

async def handle_client(client):
    loop = asyncio.get_event_loop()
    request = None

    while request != 'quit':
        logging.exception(client)
        # try:
        request = (await loop.sock_recv(client, 255)).decode('utf8')
        # except Exception as e:
        #     logging.exception(f"execption is {e}")
        # print(request)
        response = str(eval(request)) + '\n'
        is_true = {"is_true": False}
        # read_config(str(request), is_true)

        # thread1 = threading.Thread(target = read_config, args = (request, is_true))

        # thread1.start()
  
        # thread1.join()

        # response = eval str(is_true["is_true"]) + '\n'
        await loop.sock_sendall(client, response.encode('utf8'))
        logging.exception("reached c")
    
        # await loop.sock_sendall(client, request)

    client.close()


async def run_server():
    signal(SIGPIPE, SIG_DFL)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1556))
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    client, _ = await loop.sock_accept(server)
    loop.create_task(handle_client(client))

asyncio.run(run_server())

# read_config("18;0;11;11;0;18;4;0;", is_true)
# print(is_true["is_true"])