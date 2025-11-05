#!/usr/bin/python3
from colorama import Fore
import os
from os import name, system
import socket
import threading
import json
from datetime import datetime

def RaverText():
	print(Fore.RED + """
░█████████                                                    ░█████████     ░███    ░██████████
░██     ░██                                                   ░██     ░██   ░██░██       ░██    
░██     ░██  ░██████   ░██    ░██  ░███████  ░██░████         ░██     ░██  ░██  ░██      ░██    
░█████████        ░██  ░██    ░██ ░██    ░██ ░███     ░██████ ░█████████  ░█████████     ░██    
░██   ░██    ░███████   ░██  ░██  ░█████████ ░██              ░██   ░██   ░██    ░██     ░██    
░██    ░██  ░██   ░██    ░██░██   ░██        ░██              ░██    ░██  ░██    ░██     ░██    
░██     ░██  ░█████░██    ░███     ░███████  ░██              ░██     ░██ ░██    ░██     ░██    
	\n By C-r0 | V 0.0.1""")

def Clear():
	if name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

Clear()
RaverText()

host = "0.0.0.0"
port = 5000
logs = 'ip.log'

def ip_log(data):
    with open(logs, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')

def handle_client(conn, addr):
    client_ip, client_port = addr
    print(f"[+] Connection {client_ip}:{client_port}")

    # Tentar ler até 4 KB (suficiente para o JSON enviado)
    try:
        data = conn.recv(4096)
        if data:
            try:
                payload = json.loads(data.decode('utf-8').strip())
            except json.JSONDecodeError:
                payload = {"raw_data": data.decode('utf-8', errors='ignore')}
        else:
            payload = {}
    except Exception as e:
        payload = {"error": str(e)}

    print(f"[+] {payload}")

    # Monta registro para o log
    log_entry = {
        "time": datetime.utcnow().isoformat() + "Z",
        "client_ip": client_ip,
        "client_port": client_port,
        "payload": payload
    }
    ip_log(log_entry)

    # Fechar conexão
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Server TCP listening on {host}:{port}")
        while True:
            conn, addr = s.accept()  # addr = (ip, port)
            # lançar thread para não bloquear accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if 1==1:
    main()
