import time
import socket

def send_packets(port=12000):

    for pings in range(10):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(1.0)
        message = b'test'
        addr = ("127.0.0.1", 12000)

        start = time.time()
        client_socket.sendto(message, addr)
        try:
            data, server = client_socket.recvfrom(1024)
            end = time.time()
            elapsed = end - start
            print(f'{data} {pings} {elapsed}')
        except socket.timeout:
            print('REQUEST TIMED OUT')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UDP Server arguments.')
    parser.add_argument('-host', nargs='?', default='localhost')
    parser.add_argument('-port', nargs='?', default=1234)
    parser.add_argument('-message', nargs='?')
    parser.add_argument('-count', nargs='?')
    args = parser.parse_args()