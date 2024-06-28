"""Server to recieve connection and calculate"""
import socket
import logging
import re
import time

logging.basicConfig(filename='server.log', level=logging.INFO)

def calculate_chain_weight(chain):
    """
    Calculate the weight of a chain based on its composition.

    The weight is calculated:
    - If the chain contains the substring "aa" (case-insensitive), the weight is 1000.
    - Otherwise, the weight is the sum of the number of letters multiplied by 1.5, // 
    the number of digits multiplied by 2, divided by the number of spaces.

    Args:
        chain: The chain to calculate the weight for.

    Returns:
        float: The weight of the chain.
    """
    if re.search(r'[aA]{2}', chain):
        logging.warning(f'Double "a" rule detected >> {chain}')
        return 1000
    letters = sum(c.isalpha() for c in chain)
    numbers = sum(c.isdigit() for c in chain)
    spaces = chain.count(' ')
    return (letters * 1.5 + numbers * 2) / spaces

def handle_client(client_socket):
    """
    Handle a client connection.

    Receive data from the client, calculate the weight of each chain, and send the results back to the client.

    Args:
        client_socket: The socket object for the client connection.
    """
    start_time = time.time()
    data = client_socket.recv(4096)
    chains = data.decode().splitlines()
    weights = []
    for chain in chains:
        weight = calculate_chain_weight(chain)
        weights.append(str(weight))
    response = '\n'.join(weights).encode()
    client_socket.sendall(response)
    logging.info(f'Process completed in {time.time() - start_time:.2f} seconds')

def start_server(host, port):
    """
    Start a server listening on the specified host and port.

    Args:
        host: The host to listen on.
        port: The port to listen on.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        logging.info('Server started')
        while True:
            client_socket, address = s.accept()
            logging.info(f'Connected by {address}')
            handle_client(client_socket)

if __name__ == '__main__':
    start_server('localhost', 8080)