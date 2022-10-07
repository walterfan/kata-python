import argparse
import collections
import json
import selectors
import socket
import sys


BUFFER_SIZE = 1000

Message = collections.namedtuple('Message', ['user', 'text'])


class ChatClient:

   def __init__(self, **kwargs):
       self._selector = selectors.DefaultSelector()
       self._sock = None
       self._host = kwargs['host']
       self._port = kwargs['port']
       self._name = kwargs['username'] or input('Enter username:')
       self._running = True

   def _read_stdin(self, input, mask):
       data = sys.stdin.readline().strip()
       if data:
           msg = json.dumps({'user': self._name, 'text': data}, ensure_ascii=False).encode('utf8')
           self._sock.send(msg) # We should wait for selector here, but it will work.

   def _read_msg(self, conn, mask):
       data = conn.recv(BUFFER_SIZE)  # Should be ready
       if data:
           print(data.decode("utf-8"))
       else:
           print('Connection to server has failed')
           self._running = False

   def run(self):
       self._selector.register(sys.stdin, selectors.EVENT_READ, self._read_stdin)

       self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self._sock.connect((self._host, self._port))
       self._sock.setblocking(False)
       self._selector.register(self._sock, selectors.EVENT_READ, self._read_msg)

       while self._running:
           events = self._selector.select()
           for key, mask in events:
               callback = key.data
               callback(key.fileobj, mask)


parser = argparse.ArgumentParser(description='Chat client arguments.')
parser.add_argument('-host', nargs='?', default='localhost')
parser.add_argument('-port', nargs='?', default=1234)
parser.add_argument('-username', nargs='?')
args = parser.parse_args()

chat = ChatClient(**vars(args))
chat.run()