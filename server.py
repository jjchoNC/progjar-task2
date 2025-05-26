import socket
import threading
import time
import logging

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                data = b''
                while not data.endswith(b'\r\n'):
                    chunk = self.connection.recv(1)
                    if not chunk:
                        break
                    data += chunk

                if not data:
                    break

                command = data.decode().strip()
                logging.warning(f"Received command from {self.address}: {command}")

                if command == "TIME":
                    now = time.strftime("%d %m %Y %H:%M:%S", time.localtime())
                    response = f"JAM {now}\r\n"
                    self.connection.sendall(response.encode('utf-8'))
                elif command == "QUIT":
                    break
                else:
                    self.connection.sendall(b"UNKNOWN COMMAND\r\n")
        finally:
            self.connection.close()
            logging.warning(f"Connection closed from {self.address}")

class TimeServer(threading.Thread):
    def __init__(self, port):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', self.port))
        self.my_socket.listen(5)
        logging.warning(f"Time server started on port {self.port}")
        try:
            while True:
                connection, address = self.my_socket.accept()
                logging.warning(f"Connection accepted from {address}")
                client_thread = ProcessTheClient(connection, address)
                client_thread.start()
        finally:
            self.my_socket.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(message)s')
    server = TimeServer(port=45000)
    server.start()
