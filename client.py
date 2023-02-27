import socket

IP = "127.0.0.1"
PORT = 2000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


def main():
    connected = True
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
        hello_msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {hello_msg}")
    except ConnectionRefusedError:
        print("[NO CONNECTION]")
        input("Enter the empty string > ")
        return False
    try:
        while connected:
            msg = ''
            while msg == '':
                msg = input("> ")
            client.send(msg.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
    except (EOFError, KeyboardInterrupt, ConnectionAbortedError):
        print("[CONNECTION] Connection lost")


if __name__ == "__main__":
    main()
