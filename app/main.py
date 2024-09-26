import socket  # noqa: F401

# Create a message of 8 bytes(message length + correlation ID, 4 bytes each)
def create_message(msg_len, corr_id):
    return msg_len.to_bytes(4, byteorder="big") + corr_id.to_bytes(4, byteorder="big")

# Handle the client connection
def handle_client(client):
    client.recv(1024)
    client.sendall(create_message(7))
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