import socket  # noqa: F401

# Common error codes
UNSUPPORTED_VERSION = 35
NO_ERROR = 0

# API key for APIVersions request
API_VERSIONS_KEY = 18
MAX_API_VERSION = 4  # Max version for ApiKey 18

# Create a response for the client
def create_message(corr_id, error_code=NO_ERROR, api_key_versions=None):
    # Response to be sent to the client
    message = corr_id.to_bytes(4, byteorder="big", signed=True)

    message += error_code.to_bytes(2, byteorder="big", signed=True)

    # Add API_VERSIONS key info if api_key_versions is provided
    if api_key_versions is not None:
        # Number of API versions (1 entry for API_VERSIONS key)
        message += len(api_key_versions).to_bytes(4, byteorder="big", signed=False)
        
        # For each API key, append its information
        for api_key, (min_version, max_version) in api_key_versions.items():
            message += api_key.to_bytes(2, byteorder="big", signed=False)  # API Key
            message += min_version.to_bytes(2, byteorder="big", signed=False)  # Min Version
            message += max_version.to_bytes(2, byteorder="big", signed=False)  # Max Version
    
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
        # Normal response with API_VERSIONS key information
        api_key_versions = {API_VERSIONS_KEY: (0, MAX_API_VERSION)}  # API Key 18, MinVersion 0, MaxVersion 4
        client.sendall(create_message(corr_id, NO_ERROR, api_key_versions))

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
