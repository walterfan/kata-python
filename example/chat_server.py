import argparse
import collections
import json
import selectors
import socket


SERVER_NUM_CONNECTIONS = 1000
BUFFER_SIZE = 1000

Message = collections.namedtuple('Message', ['user', 'text'])


class ChatServer:

   def __init__(self, **kwargs):
       self._selector = selectors.DefaultSelector()
       self._connections_msg_queue = {}
       self._host = kwargs['host']
       self._port = kwargs['port']

   ##### SELECT FUNCTIONS ########################

   def _accept(self, sock, mask):
       conn, addr = sock.accept()
       self._add_connection(conn)

   def _read_write(self, conn, mask):
       if mask & selectors.EVENT_READ:
           self._read(conn, mask)
       if mask & selectors.EVENT_WRITE:
           self._write(conn, mask)

   def _read(self, conn, mask):
       self._read_message(conn)

   def _write(self, conn, mask):
       self._write_pending_messages(conn)

   ##### CHAT FUNCTIONS ########################

   def _add_connection(self, conn):
       # register new client connection for reading (accepting new messages)
       print(f'{conn.getpeername()} hello!')
       self._connections_msg_queue[conn] = collections.deque()
       conn.setblocking(False)
       self._selector.register(conn, selectors.EVENT_READ, self._read)

   def _remove_connection(self, conn):
       print(f'{conn.getpeername()} bye bye!')
       self._selector.unregister(conn)
       conn.close()
       del self._connections_msg_queue[conn]

   def _read_message(self, conn):
       data = conn.recv(BUFFER_SIZE)  # Should be ready
       if data:
           self._add_message(conn, data)
       else:
           self._remove_connection(conn)

   def _add_message(self, sender_conn, raw_msg):
       try:
           msg = json.loads(raw_msg)
           message = Message(msg['user'], msg['text'])
           print(f"{sender_conn.getpeername()}: [{msg['user']}] {msg['text']}")
       except (json.JSONDecodeError, KeyError,) as e:
           print(f"We got unknown type of message: {raw_msg}; error: {e}")
           return

       # register every client connection for writing (broadcast recent messages)
       for conn, messages in self._connections_msg_queue.items():
           conn.setblocking(False)  # not sure if needed
           self._selector.modify(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, self._read_write)
           messages.append(message)

   def _write_pending_messages(self, conn):
       messages = self._connections_msg_queue[conn]
       while messages:
           msg = messages.popleft()
           try:
               conn.send(f'[{msg.user}] {msg.text}'.encode('utf-8'))
           except Exception as e:
               print('Error occurred', e)
               self._remove_connection(conn)
               return

       # if no more message to send, don't listen to available for write
       conn.setblocking(False)  # not sure if needed
       self._selector.modify(conn, selectors.EVENT_READ, self._read)

   def run(self):
       # create and register server socket for reading (accepting new connections)
       server_sock = socket.socket()
       server_sock.bind((self._host, self._port))
       server_sock.listen(SERVER_NUM_CONNECTIONS)
       server_sock.setblocking(False)
       self._selector.register(server_sock, selectors.EVENT_READ, self._accept)

       while True:
           events = self._selector.select()
           for key, mask in events:
               callback = key.data
               callback(key.fileobj, mask)


parser = argparse.ArgumentParser(description='Chat server arguments.')
parser.add_argument('-host', nargs='?', default='localhost')
parser.add_argument('-port', nargs='?', default=1234)
args = parser.parse_args()

chat = ChatServer(**vars(args))
chat.run()