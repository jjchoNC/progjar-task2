import socket
import threading

def run(client_id):
    try:
        with socket.create_connection(('172.16.16.101', 45000)) as sock:
            sock.sendall(b"TIME\r\n")
            response = sock.recv(1024).decode()
            print(f"[Client {client_id}] Received: {response.strip()}")
            sock.sendall(b"QUIT\r\n")
    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")

def main():
    threads = []
    NUM_CLIENTS = 10
    for i in range(NUM_CLIENTS):
        t = threading.Thread(target=run, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
