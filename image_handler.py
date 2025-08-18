# image_handler.py

import mss
import mss.tools
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import requests
import io

def get_image_from_upload():
    """
    Opens a file dialog to let the user select an image file.
    Returns the image data in bytes.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    filepath = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if not filepath:
        return None
    with open(filepath, "rb") as f:
        return f.read()

def get_image_from_screenshot():
    """
    Takes a screenshot of the primary monitor.
    Returns the image data in bytes.
    """
    with mss.mss() as sct:
        # Get a screenshot of the first monitor
        sct_img = sct.grab(sct.monitors[1])
        # Convert to a format that can be saved to bytes
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        # Save image to a memory buffer
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

def get_image_from_web(prompt):
    """
    Fetches an image from the web based on a prompt using Unsplash.
    Returns the image data in bytes.
    """
    print(f"🔎 Searching for an image of '{prompt}'...")
    try:
        # Using Unsplash Source for simplicity - no API key needed for this.
        url = f"https://source.unsplash.com/800x600/?{prompt}"
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raises an exception for bad status codes
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not fetch image from the web: {e}")
        return None