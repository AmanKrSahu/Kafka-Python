import socket  # noqa: F401

def main():
    # Print statement for debugging
    print("Logs from your program will appear here!")

    # Create a TCP server socket on localhost at port 9092 (common for Kafka)
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    server.accept() # Waiting for client to connect

if __name__ == "__main__":
    main()