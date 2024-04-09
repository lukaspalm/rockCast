import socket
import os
from tkinter import *
import tkinter as tk
import pyautogui
from PIL import Image, ImageTk

os.system("chcp 65001")

# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept() 

print(f"[+] {address} is connected.")


def recieve_image():
    global client_socket, BUFFER_SIZE
    try: 

        print("[+] Receiving image size...")
        file_size = int(client_socket.recv(BUFFER_SIZE).decode())

        print(f"[+] Image size: {file_size}")
        image = b''
        print("[+] Receiving image...")
        bytes_received = 0
        while bytes_received < file_size:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            print(f"[+] Bytes read: {len(bytes_read)}")
            if not bytes_read:
                break
            image += bytes_read
            print("image: ", image)
            bytes_received += len(bytes_read)
        print("[+] Image received.")

        return image
    
    except Exception as e:
        print(f"[-] ERROR! Exiting...\n{e}")
        s.close()
        exit(1)



master = tk.Tk()
master.bind("q", lambda e: master.quit())
master.title("RockCast")
#master.attributes("-fullscreen", True)


limg = Label(master)
limg.pack()

screen_scaling_factor = master.winfo_screenheight() / master.winfo_screenwidth()

def update_image():

    print("[+] Receiving image...")
    img = recieve_image()
    print("[+] Updating image...")

    scaled_img = img.resize((int(img.width * screen_scaling_factor), int(img.height * screen_scaling_factor)))
    bgimg = ImageTk.PhotoImage(scaled_img)
    limg.config(image=bgimg)
    limg.image = bgimg

    print("[+] Image updated.")

    os.remove("temp.png")
    
    client_socket.send("success".encode())
    master.after(50, update_image)





update_image()

try:
    master.mainloop()
except KeyboardInterrupt:
    print("[+] Stopping...")
except Exception as e:
    print(f"[+] ERROR. Exiting...\n{e}")


client_socket.close()
s.close()