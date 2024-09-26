import socket  # noqa: F401

# Create a message of 8 bytes(message length + correlation ID, 4 bytes each)
def create_message(msg_len, corr_id):
    return msg_len.to_bytes(4, byteorder="big") + corr_id.to_bytes(4, byteorder="big")

# Handle the client connection
def handle_client(client):
    # Receive the request from the client
    req = client.recv(1024)

    # Extract the Correlation ID from the request
    corrId = int.from_bytes(req[8:12], byteorder="big")

    # Send the response with the extracted correlation ID
    client.sendall(create_message(0,corrId))

    # Close the connection
    client.close()

def main():
    # Print statement for debugging
    print("Logs from your program will appear here!")

    # Create a TCP server socket on localhost at port 9092 (common for Kafka)
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    
    # Create an infinite loop waiting for incoming client connections
    while True:
        client, addr = server.accept()
        handle_client(client)

if __name__ == "__main__":
    main()
    