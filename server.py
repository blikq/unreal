# Import the threading and socket modules
import threading
import socket
import logging

logging.basicConfig(filename="log.txt")
level=logging.INFO

# Define a function to read a config file and search for a query string
def read_config(query: str, is_true: dict):
    # Open the config file for reading, with utf-8 encoding
    with open("config.txt", 'r', encoding="utf-8") as config_file:
        # Read each line of the config file
        for line in config_file:
            # If the line starts with the prefix "linuxpath=", process it
            if line.strip().startswith("linuxpath="):
                # Remove the prefix "linuxpath=" and strip any whitespace
                file_path = line.removeprefix('linuxpath=').strip()
                # Open the file specified in the config line and check if the query appears in it
                try:
                    with open(file_path, 'r') as query_file:
                        if query_file.read().find(query) != -1:
                            # If the query string is found, update the is_true dictionary and return
                            return is_true.update({"is_true": "STRING EXISTS"})
                        else:
                            # If the query string is not found, do nothing
                            pass
                except Exception as e:
                    # If an error occurs while opening or reading the file, log the exception (currently commented out)
                    # logging.exception(e)
                    pass
    # If the query string is not found and no errors occurred, update the is_true dictionary with "STRING NOT FOUND"
    is_true.update({"is_true": "STRING NOT FOUND"})

# Define a function to handle a client's request
def handle_client(client_socket):
    # Keep processing the client's request until it closes the connection
    while True:
        # Read the request from the client (up to 1024 bytes)
        request = client_socket.recv(1024)

        try:
            # Initialize the is_true dictionary
            is_true = {"is_true": False}
            # Call the read_config function to process the request
            read_config(str(request.decode('utf8')), is_true)
            # Set the response to the value in the is_true dictionary
            response = is_true["is_true"]
        except:
            # If an error occurs while processing the request, set the response to "Invalid Request Type"
            response = "Invalid Request Type"
        # Send the response back to the client
        client_socket.send(response.encode('utf8'))
        # Close the client's socket
        client_socket.close()

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to localhost:8090
server_socket.bind(("localhost", 8090))
# Listen for up to 5 incoming connections
server_socket.listen(5)

# Run the server indefinitely
while True:
    # Accept an incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Received connection from {client_address}")
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    client_thread.join()