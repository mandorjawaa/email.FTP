import socket

# PORT harus SAMA dengan Server
PORT = 5555

def start_client():
    print("\n=== APLIKASI CHAT CLIENT ===")
    
    # Masukkan IP yang muncul di Laptop A tadi
    server_ip = input("Masukkan IP Server: ")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print(f"Sedang menghubungi {server_ip}...")
    
    try:
        # Timeout 5 detik (biar gak hang kalau salah IP)
        client.settimeout(5)
        client.connect((server_ip, PORT))
        client.settimeout(None) # Reset timeout agar bisa chat normal
        print("[BERHASIL] HORE! Terhubung ke Server.")
    except Exception as e:
        print("\n[GAGAL KONEK]")
        print("Penyebab biasanya:")
        print("1. IP Salah (Harus sama persis dengan layar Server).")
        print("2. Laptop A Firewall belum mati.")
        print("3. Beda Wi-Fi.")
        print(f"Error detail: {e}")
        return

    while True:
        print("\n--- MENU ---")
        print("1. Kirim Pesan")
        print("2. Cek Inbox")
        print("3. Keluar")
        choice = input("Pilih (1-3): ")

        msg = ""
        if choice == '1':
            recipient = input("Kirim ke nama siapa: ")
            content = input("Isi Pesan: ")
            msg = f"KIRIM|{recipient}|{content}"
        elif choice == '2':
            user = input("Nama Anda siapa: ")
            msg = f"BACA|{user}"
        elif choice == '3':
            client.send("!KELUAR".encode('utf-8'))
            break
        else:
            print("Salah pilih angka.")
            continue

        try:
            client.send(msg.encode('utf-8'))
            # Tunggu balasan server
            response = client.recv(4096).decode('utf-8')
            print(f"\n[SERVER MENJAWAB]:\n{response}")
        except:
            print("[PUTUS] Koneksi hilang.")
            break

    client.close()

if __name__ == "__main__":
    start_client()