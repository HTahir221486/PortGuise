import socket
import threading
import time

GREEN = "\033[92m"
RESET = "\033[0m"

ASCII_ART = f"""{GREEN}
| ██████   ██████  ██████  ████████  ██████  ██    ██ ██ ███████ ███████
| ██   ██ ██    ██ ██   ██    ██    ██       ██    ██ ██ ██      ██
| ██████  ██    ██ ██████     ██    ██   ███ ██    ██ ██ ███████ █████
| ██      ██    ██ ██   ██    ██    ██    ██ ██    ██ ██      ██ ██
| ██       ██████  ██   ██    ██     ██████   ██████  ██ ███████ ███████
{RESET}
"""

PORTS = {
    80: b"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\nContent-Length: 50\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Fake HTTP Server</h1></body></html>",
    22: b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\r\n",
    25: b"220 fake-smtp.example.com ESMTP Postfix (Ubuntu)\r\n",
    443: b"HTTP/1.1 200 OK\r\nServer: nginx/1.18.0 (Ubuntu)\r\nContent-Length: 50\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Fake HTTPS Server</h1></body></html>"
}

BANNERS = {
    'HTTP': PORTS[80],
    'SSH': PORTS[22],
    'SMTP': PORTS[25],
    'HTTPS': PORTS[443]
}

def start_spoofing(port, banner, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen()
        s.settimeout(timeout)
        print(f"{GREEN}[*] Listening on port {port}...{RESET}")

        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"{GREEN}[+] Connection from {addr[0]}:{addr[1]} on port {port}{RESET}")
                    try:
                        conn.sendall(banner)
                    except ConnectionResetError:
                        print(f"{GREEN}[!] Connection reset by peer on port {port}{RESET}")
                    except BrokenPipeError:
                        print(f"{GREEN}[!] Broken pipe on port {port}{RESET}")
            except socket.timeout:
                print(f"{GREEN}[!] Session timed out on port {port}.{RESET}")
                break

def display_menu():
    print("\n[======================== MENU =======================]")
    print("| [1] Spoof Custom Port")
    print("| [2] Exit")
    print("| [====================================================]")
    return input("| \n[+] Select option: ")

def main():
    timeout_duration = 15

    print(ASCII_ART)

    while True:
        choice = display_menu()

        if choice == '2':
            print("| [*] Exiting...")
            break

        if choice == '1':
            port = int(input("| [+] Enter the port number: "))
            service = input("| [+] Enter the service (HTTP, SSH, SMTP, HTTPS): ").strip().upper()
            if service in BANNERS:
                banner = BANNERS[service]
                t = threading.Thread(target=start_spoofing, args=(port, banner, timeout_duration))
                t.start()
                t.join()
            else:
                print("| [!] Invalid service selected.")
                continue

if __name__ == "__main__":
    main()