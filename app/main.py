import socket  # noqa: F401

# Error code for unsupported version
UNSUPPORTED_VERSION = 35

# Create a response for the client
def create_message(corr_id, error_code=None):
    # Response to be sent to the client
    message = corr_id.to_bytes(4, byteorder="big", signed=True)

    # Check if error code exits
    if error_code is not None:
        message += error_code.to_bytes(2, byteorder="big", signed=True)
    
    # Find the length of the message
    message_len = len(message).to_bytes(4, byteorder="big", signed=False)
    
    return message_len + message

# Handle the client connection
def handle_client(client):
    # Receive the request from the client
    req = client.recv(1024)

    # Extract the API version 
    api_version = int.from_bytes(req[4:8], byteorder="big")

    # Extract the Correlation ID from the request
    corr_id = int.from_bytes(req[8:12], byteorder="big")

    # Check if the api version is supported
    if api_version not in [0, 1, 2, 3, 4]:
        # Respond with UNSUPPORTED_VERSION error code
        client.sendall(create_message(corr_id, UNSUPPORTED_VERSION))
    else:
        # Normal response (no error, just echo the correlation ID)
        client.sendall(create_message(corr_id))

    # Close the connection
    client.close()

def main():
    # Print statement for debugging
    print("Logs of the program executed!!")

    # Create a TCP server socket on localhost at port 9092 (common for Kafka)
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    
    # Create an infinite loop waiting for incoming client connections
    while True:
        client, addr = server.accept()
        handle_client(client)

if __name__ == "__main__":
    main()
