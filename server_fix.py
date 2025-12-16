import socket
import threading

# Server Lokal
HOST = '0.0.0.0'
PORT = 5555 # Gunakan port ini

mailbox = {}

def handle_client(client_socket, addr):
    print(f"[BARU] Koneksi dari {addr}")
    connected = True
    while connected:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg or msg == "!KELUAR":
                connected = False
                break
            
            parts = msg.split("|")
            command = parts[0]
            response = ""

            if command == "KIRIM":
                recipient = parts[1]
                content = parts[2]
                if recipient not in mailbox: mailbox[recipient] = []
                mailbox[recipient].append(content)
                response = f"SUKSES: Pesan terkirim ke {recipient}"
                print(f"[LOG] Disimpan Untuk {recipient}")
                print(f"[LOG] Pesan dari Client: {content}") 

            elif command == "BACA":
                user = parts[1]
                if user in mailbox and mailbox[user]:
                    response = "\n".join(mailbox[user])
                else:
                    response = "KOSONG"
                print(f"[LOG] {user} cek inbox.")

            else:
                response = "ERROR"
            client_socket.send(response.encode('utf-8'))
        except:
            connected = False
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Trik agar port bisa langsung dipakai ulang jika server mati
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
    except OSError:
        print(f"ERROR: Port {PORT} sedang dipakai. Ganti PORT di kodingan jadi 5556.")
        return

    server.listen()
    
    # Cara ambil IP Laptop Windows yang benar
    hostname = socket.gethostname()
    ip_add = socket.gethostbyname(hostname)
    
    print("="*40)
    print(f"[SERVER BERJALAN DI WINDOWS CMD]")
    print(f"IP YANG HARUS DIPAKAI CLIENT: {ip_add}")
    print("="*40)
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()