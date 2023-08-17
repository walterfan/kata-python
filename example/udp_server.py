import random
import socket
import argparse

def receive_packets(port=12000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    packet_count = 0
    while True:
        rand = random.randint(0, 10)
        message, address = server_socket.recvfrom(1024)
        message = message.upper()
        packet_count = packet_count + 1
        if rand >= 4:
            server_socket.sendto(message, address)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UDP Server arguments.')
    parser.add_argument('-host', nargs='?', default='localhost')
    parser.add_argument('-port', nargs='?', default=1234)
    parser.add_argument('-message', nargs='?')
    parser.add_argument('-count', nargs='?')
    args = parser.parse_args()