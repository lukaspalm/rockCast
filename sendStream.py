import socket
import os
import pyautogui
import time
import sys

if os.getenv("OS") == "Windows_NT":
    os.system("chcp 65001")

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

host = sys.argv[1]

port = 5001

filename = "test.png"

if os.path.exists(filename) is False:
    pyautogui.screenshot(filename)

filesize = os.path.getsize(filename)





try:
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    while True:
        print("[+] Sending image...")
        time.sleep(0.5)
        if os.path.exists(filename):
            print("[+] Removing old image")
            os.remove(filename)

        print("[+] Capturing screenshot")
        pyautogui.screenshot(filename)
        
        print("[+] Sending...")
        s.send(f"{os.path.getsize(filename)}".encode())
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:

                    break
                s.sendall(bytes_read)
        print("[+] Image sent.")

        print("[+] Waiting for response...")
        s.recv(1024)

except KeyboardInterrupt:
    print("\n[+] Stopping.")
    s.close()
except Exception as e:
    print(f"[-] ERROR! Exiting...\n{e}")
    s.close()
    exit(1)
