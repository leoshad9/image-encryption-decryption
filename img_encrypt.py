"""
Image Encryption Tool

This script encrypts images using a randomly generated key.
The encrypted image and key are saved for later decryption.

Author: Mohammad Shadman Khan
"""

from typing import List
import matplotlib.pyplot as plt
import numpy as np
import random
import logging
import os
import time
import tkinter as tk
from tkinter import filedialog

# Configure logging with more details
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_image(img_path: str) -> np.ndarray:
    """
    Load an image from a file path and ensure it's in uint8 format.
    """
    logging.info(f"Loading image from {img_path}")
    try:
        start_time = time.time()
        img = plt.imread(img_path)
        if img.dtype != np.uint8:
            img = (img * 255).astype(np.uint8)
        logging.info(f"Image loaded successfully in {time.time() - start_time:.2f} seconds")
        return img
    except Exception as e:
        logging.error(f"Failed to load image: {e}")
        raise

def display_image(img: np.ndarray, title: str):
    """
    Display an image with a given title.
    """
    logging.info(f"Displaying image: {title}")
    plt.title(title)
    plt.imshow(img)
    plt.show()

def generate_key() -> List[int]:
    """
    Generate a random permutation of integers from 0 to 255 for encryption.
    """
    logging.info("Generating encryption key")
    start_time = time.time()
    key = list(range(256))
    random.shuffle(key)
    logging.info(f"Key generated in {time.time() - start_time:.2f} seconds")
    return key

def save_key_to_file(key: List[int], file_path: str):
    """
    Save the key to a text file.
    """
    logging.info(f"Saving key to {file_path}")
    try:
        start_time = time.time()
        key_string = ', '.join(map(str, key))
        with open(file_path, 'w') as file:
            file.write(key_string)
        logging.info(f"Key saved successfully in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logging.error(f"Failed to save key: {e}")
        raise

def encrypt_image(img: np.ndarray, key: List[int]) -> np.ndarray:
    """
    Encrypt the image using the given key.
    """
    logging.info("Starting image encryption")
    start_time = time.time()
    
    try:
        rows, cols = img.shape[:2]
        logging.info(f"Image dimensions: {rows}x{cols}")
        
        img1 = np.zeros((rows, cols, 3), dtype=int)
        for i in range(rows):
            for j in range(cols):
                for k in range(3):
                    img1[i][j][k] = key[img[i][j][k]]
        
        logging.info(f"Image encryption completed in {time.time() - start_time:.2f} seconds")
        return img1
    except Exception as e:
        logging.error(f"Error during encryption: {e}")
        raise

def save_image_to_csv(img: np.ndarray, filename: str, rows: int, cols: int):
    """
    Save the image data to a CSV file with dimensions.
    """
    logging.info(f"Saving image to CSV: {filename}")
    try:
        start_time = time.time()
        img_flat = img.reshape(-1, img.shape[-1])
        with open(filename, 'w') as file:
            file.write(f"{rows},{cols}\n")
            np.savetxt(file, img_flat, delimiter=',', fmt='%d')
        logging.info(f"Image saved to CSV in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logging.error(f"Failed to save image to CSV: {e}")
        raise

def save_image_as_png(img: np.ndarray, png_path: str):
    """
    Save the image data as a PNG file.
    """
    logging.info(f"Saving image to PNG: {png_path}")
    try:
        start_time = time.time()
        img_to_save = np.clip(img, 0, 255).astype(np.uint8)
        plt.imsave(png_path, img_to_save)
        logging.info(f"Image saved to PNG in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logging.error(f"Failed to save image as PNG: {e}")
        raise

def select_file(title, filetypes):
    """
    Open a dialog to select a file.
    """
    root = tk.Tk()
    root.attributes('-topmost', True)  # Make sure dialog appears on top
    root.withdraw()  # Hide the main window
    
    # Force focus on the dialog
    root.focus_force()
    
    # Use a callback to ensure the dialog is shown
    def open_dialog():
        file_path = filedialog.askopenfilename(title=title, filetypes=filetypes, parent=root)
        root.file_path = file_path
        root.quit()
    
    # Schedule the dialog to open after the main loop starts
    root.after(100, open_dialog)
    
    # Start the main loop
    root.mainloop()
    
    # Get the selected file path
    file_path = getattr(root, 'file_path', '')
    
    # Destroy the root window
    root.destroy()
    
    return file_path

def select_directory(title):
    """
    Open a dialog to select a directory.
    """
    root = tk.Tk()
    root.attributes('-topmost', True)  # Make sure dialog appears on top
    root.withdraw()  # Hide the main window
    
    # Force focus on the dialog
    root.focus_force()
    
    # Use a callback to ensure the dialog is shown
    def open_dialog():
        directory = filedialog.askdirectory(title=title, parent=root)
        root.directory = directory
        root.quit()
    
    # Schedule the dialog to open after the main loop starts
    root.after(100, open_dialog)
    
    # Start the main loop
    root.mainloop()
    
    # Get the selected directory
    directory = getattr(root, 'directory', '')
    
    # Destroy the root window
    root.destroy()
    
    return directory

def main():
    try:
        # Initialize Tkinter root
        logging.info("Starting image encryption process")
        
        # Open file dialog for selecting an image file
        print("Select an image to encrypt...")
        img_path = select_file("Select Image File", [("Image Files", "*.jpg *.jpeg *.png")])
        if not img_path:
            logging.error("No image file selected")
            print("No image file selected.")
            exit(1)
        logging.info(f"Selected image: {img_path}")
        
        # Ensure the path is absolute
        img_path = os.path.abspath(img_path)
        
        # Get the directory where to save key and image
        print("Select a directory to save the key and encrypted image...")
        output_dir = select_directory("Select Output Directory")
        if not output_dir:
            logging.error("No output directory selected")
            print("No directory selected.")
            exit(1)
        logging.info(f"Selected output directory: {output_dir}")
        
        # Ensure the path is absolute
        output_dir = os.path.abspath(output_dir)  

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            logging.info(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir)

        # Define paths for saving files
        key_file_path = os.path.join(output_dir, "key.txt")
        encrypted_csv_path = os.path.join(output_dir, "encrypted_image.csv")
        encrypted_png_path = os.path.join(output_dir, "encrypted_image.png")

        # Load and display the original image
        try:
            img = load_image(img_path)
        except Exception as e:
            logging.error(f"Failed to load image: {e}")
            print(f"Error loading image: {e}")
            exit(1)

        # Generate and save the key
        try:
            key = generate_key()
            save_key_to_file(key, key_file_path)
        except Exception as e:
            logging.error(f"Failed to generate or save key: {e}")
            print(f"Error with key: {e}")
            exit(1)

        print("Processing...")

        # Encrypt the image
        try:
            encrypted_img = encrypt_image(img, key)
        except Exception as e:
            logging.error(f"Failed to encrypt image: {e}")
            print(f"Error encrypting image: {e}")
            exit(1)

        # Save the encrypted image to CSV
        try:
            rows, cols = img.shape[:2]
            save_image_to_csv(encrypted_img, encrypted_csv_path, rows, cols)
        except Exception as e:
            logging.error(f"Failed to save encrypted image to CSV: {e}")
            print(f"Error saving encrypted image to CSV: {e}")
            exit(1)

        # Save the encrypted image as a PNG
        try:
            save_image_as_png(encrypted_img, encrypted_png_path)
        except Exception as e:
            logging.error(f"Failed to save encrypted image as PNG: {e}")
            print(f"Error saving encrypted image as PNG: {e}")
            exit(1)

        # Display the encrypted image
        print("Encrypted!")
        logging.info("Encryption process completed successfully")
        display_image(encrypted_img, "Encrypted Image")
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
