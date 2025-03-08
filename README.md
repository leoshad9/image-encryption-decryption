# Image Encryption and Decryption

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

This project provides a solution for encrypting and decrypting images using a randomly generated key. The encrypted images are stored in CSV format, and the key is saved in a text file for later decryption.

<p align="center">
  <img src="screenshots/app_screenshot.png" alt="Application Screenshot" width="600">
</p>

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Security Considerations](#security-considerations)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## Author

Mohammad Shadman Khan

## Features

- **Image Encryption**: Encrypts images using a randomly generated key and saves the encrypted image in CSV format.
- **Image Decryption**: Decrypts images using the key file to restore the original image.
- **Graphical User Interface (GUI)**: Uses Tkinter to provide a user-friendly interface for selecting files and directories.
- **Security**: Implements a substitution cipher to protect image data.
- **Logging**: Comprehensive logging for debugging and auditing purposes.

## Requirements

- Python 3.x
- Required Python packages:
  - `numpy`
  - `matplotlib`
  - `tkinter` (usually included with Python)
  - `pillow` (PIL fork, used by matplotlib for image processing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/leoshad9/image-encryption-decryption.git
   cd image-encryption-decryption
   ```

2. Install the required packages:
   ```bash
   pip install numpy matplotlib pillow
   ```

3. Verify installation:
   ```bash
   python -c "import numpy; import matplotlib; import PIL; print('All dependencies installed successfully!')"
   ```

## Usage

### Encrypting an Image

1. Run the `img_encrypt.py` script:
   ```bash
   python img_encrypt.py
   ```

2. Follow the prompts to:
   - Select an image file to encrypt (supports `.jpg`, `.jpeg`, `.png`).
   - Choose a directory to save the encrypted image and key.

3. The encrypted image will be saved as `encrypted_image.csv` and `encrypted_image.png` in the selected directory, and the key will be saved as `key.txt`.

### Decrypting an Image

1. Run the `img_decrypt.py` script:
   ```bash
   python img_decrypt.py
   ```

2. Follow the prompts to:
   - Select the key file (`key.txt`).
   - Choose the directory containing the `encrypted_image.csv`.
   - Select a directory to save the decrypted image.

3. The decrypted image will be displayed and saved as `decrypted_image.png` in the selected directory.

## How It Works

The encryption process uses a substitution cipher with a randomly generated key to transform each pixel value in the image:

1. A random key is generated as a permutation of integers from 0 to 255
2. Each pixel value in each color channel (R,G,B) is replaced with its corresponding value in the key
3. The result is saved as CSV for perfect reconstruction
4. The decryption process applies the inverse key mapping to recover the original image

### Technical Details

```
Encryption: Encrypted_pixel = key[Original_pixel]
Decryption: Original_pixel = inverse_key[Encrypted_pixel]
```

The substitution cipher uses a key that is a random permutation of values from 0 to 255. During decryption, we create an inverse mapping (a dictionary) where:

```python
inverse_key = {v: i for i, v in enumerate(key)}
```

This allows us to look up the original pixel value when given the encrypted value.

## Security Considerations

- **Key Management**: Keep your key file (`key.txt`) secure. Anyone with access to this file can decrypt your images.
- **Educational Purpose**: This implementation is for educational purposes and may not be suitable for highly sensitive data.
- **Cryptographic Strength**: The substitution cipher used here is vulnerable to frequency analysis if applied to text but is more resistant when used on image data due to the complex distribution of pixel values.
- **Production Use**: Consider using established cryptographic libraries like PyCryptodome or cryptography for production applications.
- **Key Storage**: The key is stored in plaintext, which is a security vulnerability. For higher security, consider encrypting the key itself.

## Performance Considerations

- **Encryption Speed**: The encryption uses nested loops for processing each pixel, which may be slow for very large images.
- **Decryption Optimization**: The decryption uses NumPy's vectorized operations which is faster than the pixel-by-pixel approach used in encryption.
- **Memory Usage**: The entire image is loaded into memory, which could be problematic for extremely large images.
- **Improvements**: For better performance with large images, consider:
  - Implementing chunked processing
  - Using NumPy's vectorized operations for encryption as well
  - Parallelizing the encryption/decryption process with multiprocessing

## Troubleshooting

### Common Issues

- **FileNotFoundError**: Ensure all paths are correctly specified
- **Key mismatch**: Make sure you're using the correct key file for decryption
- **Image display issues**: Try reinstalling matplotlib if decrypted images don't display correctly
- **Memory errors**: For very large images, try processing them in smaller chunks
- **Tkinter dialog not appearing**: Make sure your system has Tkinter properly installed and configured

For additional help, please open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## Contact

For questions or feedback, please contact Mohammad Shadman Khan.

Project repository: [https://github.com/leoshad9/image-encryption-decryption](https://github.com/leoshad9/image-encryption-decryption)