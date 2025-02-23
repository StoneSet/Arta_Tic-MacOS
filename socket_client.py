import socket
import subprocess

HOST = '127.0.0.1'
PORT = 65432

def execute_ticcmd(command_str):
    args = command_str.split()
    try:
        result = subprocess.check_output(["ticcmd"] + args, text=True)
    except subprocess.CalledProcessError as e:
        result = f"Erreur lors de l'exécution : {e}"
    return result

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Serveur ticcmd en attente de commandes...")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connexion de {addr}")
            data = conn.recv(1024)
            if not data:
                continue
            command_str = data.decode('utf-8')
            print(f"Commande reçue : {command_str}")
            output = execute_ticcmd(command_str)
            conn.sendall(output.encode('utf-8'))
