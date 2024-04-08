from tkinter import *
import tkinter as tk
import pyautogui
import os
import time

master = tk.Tk()
master.bind("q", lambda e: master.quit())
master.title("RockCast")

# Create the Label widget once
limg = Label(master)
limg.pack()

def update_image():
    # Capture screenshot and save as temp.png
    pyautogui.screenshot("temp.png")

    # Load the image and update the Label widget
    bgimg = PhotoImage(file="temp.png")
    limg.config(image=bgimg)
    limg.image = bgimg  # Keep a reference to prevent garbage collection

    # Remove the temporary image file
    os.remove("temp.png")

    # Call update_image again after 500ms (0.5 seconds)
    master.after(50, update_image)

# Start the update_image loop
update_image()

# Start the Tkinter event loop
master.mainloop()
