"""Client for generate chains and send to the server."""

import socket
import random
import string
import logging

logging.basicConfig(filename='client.log', level=logging.INFO)

def generate_chains(num_chains=1000000):
    """
    Generate a list of random chains.

    Each chain is a string of random length between 50 and 100 characters, containing a mix of letters, digits, and spaces.
    The number of spaces in each chain is between 3 and 5.

    Args:
        num_chains (int): The number of chains to generate. Defaults to 1000000.

    Returns:
        list: A list of generated chains.
    """
    chains = []
    for _ in range(num_chains):
        chain = ''.join(random.choice(string.ascii_letters + string.digits + ' ') for _ in range(random.randint(50, 100)))
        while not (3 <= chain.count(' ') <= 5):
            chain = ''.join(random.choice(string.ascii_letters + string.digits + ' ') for _ in range(random.randint(50, 100)))
        chains.append(chain)
    return chains

def send_chains_to_server(chains, host, port):
    """
    Send a list of chains to a server and save the response.

    Args:
        chains (list): The list of chains to send.
        host (str): The host of the server.
        port (int): The port of the server.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        message = '\n'.join(chains).encode()
        s.sendall(message)
        response = s.recv(4096).decode()
        with open('response.txt', 'w') as f:
            f.write(response)

if __name__ == '__main__':
    num_chains = int(input("Enter the number of chains to generate (default=1000000): ") or 1000000)
    logging.info(f"Generating {num_chains} chains...")
    chains = generate_chains(num_chains)
    logging.info("Chains generated. Saving to file...")
    with open('chains.txt', 'w') as f:
        logging.info("Chains saved to file. Sending to server...")
        f.write('\n'.join(chains))
    try:
        send_chains_to_server(chains, 'localhost', 8080)
        logging.info("Chains sent to server.")
    except Exception as e:
        logging.error("Error occurred: %s", e)