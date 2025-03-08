"""
Image Decryption Tool

This script decrypts images that were encrypted using the img_encrypt.py tool.
It uses a key file to reverse the encryption process and restore the original image.

Author: Mohammad Shadman Khan
"""

import getpass
import numpy as np
import matplotlib.pyplot as plt
import os
import logging
import time
import tkinter as tk
from tkinter import filedialog

# Configure logging with more details
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to display image
def display_image(img: np.ndarray, title: str):
    """
    Display an image with a given title.
    """
    plt.title(title)
    plt.imshow(img)
    plt.show()

# Function to validate key
def validate_key(key):
    """
    Validate that the key is a permutation of integers from 0 to 255.
    """
    logging.info("Validating key...")
    if len(key) != 256:
        raise ValueError(f"Key length is {len(key)}, expected 256")
    
    sorted_key = sorted(key)
    expected_range = list(range(256))
    if sorted_key != expected_range:
        # Find differences for better error reporting
        missing = set(expected_range) - set(sorted_key)
        duplicates = [x for x in sorted_key if sorted_key.count(x) > 1]
        if missing:
            raise ValueError(f"Key is missing values: {missing}")
        if duplicates:
            raise ValueError(f"Key has duplicate values: {set(duplicates)}")
        raise ValueError("Key is not a valid permutation of integers from 0 to 255")
    
    logging.info("Key validation successful")

# Function to load key from file
def load_key_from_file(filename):
    """
    Load the key from a text file.
    """
    logging.info(f"Loading key from {filename}")
    try:
        with open(filename, 'r') as file:
            key_string = file.read().strip()
            key = [int(s.strip()) for s in key_string.split(',')]
            logging.info(f"Key loaded, length: {len(key)}")
            return key
    except Exception as e:
        logging.error(f"Error loading key: {e}")
        raise

# Function to load image from CSV file
def load_image_from_csv(filename):
    """
    Load an image from a CSV file.
    """
    logging.info(f"Loading image from {filename}")
    if not os.path.exists(filename):
        logging.error(f"File not found at {filename}")
        return None, None, None
    try:
        start_time = time.time()
        with open(filename, 'r') as file:
            # Read dimensions from the first line
            line = file.readline().strip()
            rows, cols = map(int, line.split(','))
            logging.info(f"Image dimensions: {rows}x{cols}")

            # Load the flattened image data
            logging.info("Loading image data...")
            img_flat = np.loadtxt(file, delimiter=',', dtype=int)
            logging.info(f"Image data loaded in {time.time() - start_time:.2f} seconds")

            # Reshape to original dimensions
            img = img_flat.reshape((rows, cols, 3))
            logging.info("Image reshaped successfully")

        return img, rows, cols
    except Exception as e:
        logging.error(f"Error loading image: {e}")
        return None, None, None

# Function to validate image
def validate_image(img):
    """
    Validate that the image has 3 channels and pixel values are in the range [0, 255].
    """
    logging.info("Validating image...")
    if not isinstance(img, np.ndarray):
        raise ValueError(f"Image is not a numpy array, got {type(img)}")
    
    if img.ndim != 3:
        raise ValueError(f"Image has {img.ndim} dimensions, expected 3")
    
    if img.shape[-1] != 3:
        raise ValueError(f"Image has {img.shape[-1]} channels, expected 3")
    
    min_val = np.min(img)
    max_val = np.max(img)
    if min_val < 0 or max_val > 255:
        raise ValueError(f"Image data values out of range. Min: {min_val}, Max: {max_val}")
    
    logging.info("Image validation successful")

# Function to decrypt image
def decrypt_image(img, key):
    """
    Decrypt the image using the provided key.
    """
    logging.info("Starting image decryption...")
    start_time = time.time()
    
    try:
        # Create inverse key mapping
        inverse_key = {v: i for i, v in enumerate(key)}
        logging.info("Inverse key mapping created")
        
        # Apply decryption
        img1_loaded = np.vectorize(inverse_key.get)(img)
        logging.info(f"Image decryption completed in {time.time() - start_time:.2f} seconds")
        
        return img1_loaded
    except Exception as e:
        logging.error(f"Error during decryption: {e}")
        raise

def save_image_as_png(img: np.ndarray, png_path: str):
    """
    Save the image data as a PNG file.
    """
    logging.info(f"Saving image to {png_path}")
    try:
        start_time = time.time()
        img_to_save = np.clip(img, 0, 255).astype(np.uint8)
        plt.imsave(png_path, img_to_save)
        logging.info(f"Image saved successfully in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logging.error(f"Failed to save image as PNG: {e}")
        raise

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

def main():
    try:
        # Open a GUI to select the key file
        logging.info("Opening file dialog for key file selection")
        print("Select the key file...")
        key_file = select_file("Select Key File", [("Text Files", "*.txt"), ("All Files", "*.*")])
        if not key_file:
            logging.error("No key file selected")
            print("No key file selected.")
            exit(1)
        logging.info(f"Selected key file: {key_file}")
        
        print("Processing...")
        
        # Load and validate the key
        try:
            key = load_key_from_file(key_file)
            validate_key(key)
        except Exception as e:
            logging.error(f"Key error: {e}")
            print(f"Key Error: {e}")
            exit(1)

        # Open a GUI to select the image directory
        logging.info("Opening file dialog for image directory selection")
        print("Select the directory containing the encrypted image...")
        img_dir = select_directory("Select Image Directory")
        if not img_dir:
            logging.error("No image directory selected")
            print("No image directory selected.")
            exit(1)
        logging.info(f"Selected directory: {img_dir}")

        # Load the encrypted image
        csv_path = os.path.join(img_dir, "encrypted_image.csv")
        img1_loaded, _, _ = load_image_from_csv(csv_path)
        if img1_loaded is None:
            logging.error("Failed to load image")
            print("Failed to load image.")
            exit(1)

        # Decrypt the image
        try:
            logging.info("Starting decryption process")
            img3 = decrypt_image(img1_loaded, key)
            validate_image(img3)
        except (ValueError, KeyError) as e:
            logging.error(f"Decryption error: {e}")
            print(f"Error: {e}")
            exit(1)

        # Display the decrypted image
        logging.info("Decryption completed successfully")
        print("Decrypted!")
        display_image(img3, "Decrypted Image")

        # Open a GUI to select the output directory for saving the decrypted image
        logging.info("Opening file dialog for output directory selection")
        print("Select where to save the decrypted image...")
        output_dir = select_directory("Select Output Directory")
        if not output_dir:
            logging.error("No output directory selected")
            print("No output directory selected.")
            exit(1)
        logging.info(f"Selected output directory: {output_dir}")

        # Save the decrypted image
        decrypted_png_path = os.path.join(output_dir, "decrypted_image.png")
        save_image_as_png(img3, decrypted_png_path)
        print(f"Image saved to {decrypted_png_path}")
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
