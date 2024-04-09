import socket
import os
import pyautogui
import time
import sys
import io
import PIL.Image as Image

os.system("chcp 65001")

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

host = sys.argv[1]

port = 5001





try:
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    while True:
        print("[+] Sending image...")
        time.sleep(0.2)
        image = pyautogui.screenshot()
        im = Image.fromarray(image)
        b = io.BytesIO()
        im.save(b, format="PNG")
        image_bytes = b.getvalue()
        print("[+] Image captured. Size: ", len(image_bytes))
        with open("out.txt", "a") as f:
            f.write(str(image_bytes))
        

        s.send(f"{len(image_bytes)}".encode())
        for i in range(0, len(image), BUFFER_SIZE):
            if i+BUFFER_SIZE > len(image_bytes):
                byte = image_bytes[i:]
            else:
                byte = image_bytes[i:i+BUFFER_SIZE]
            s.sendall(byte)
            print(f"[+] Sent {len(byte)} bytes.")
        print("[+] Image sent.")
        s.recv(1024)

except KeyboardInterrupt:
    print("\n[+] Stopping.")
    s.close()
except Exception as e:
    print(f"[-] ERROR! Exiting...\n{e}")
    s.close()
    exit(1)
