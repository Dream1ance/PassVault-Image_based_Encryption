# Passvault 🔐

Passvault is a unique, command-line password manager that uses **any image file as a master key** to encrypt and secure your sensitive passwords. Instead of remembering a complex master password, you just need to have the right image.

## How It Works

The core idea behind Passvault is to treat an image file as a physical key. The security isn't based on the image's filename or metadata, but on its actual pixel data.

1.  **Image as a Seed**: When you provide an image (by uploading, screenshot, or web fetch), the program takes the entire binary data of that image.
2.  **Deterministic Hashing**: The image data is hashed using SHA-256 to create a unique and fixed-size "fingerprint".
3.  **Randomized Key Slicing**: This hash is then used to seed a random number generator. This makes the process *deterministic* (the same image will always produce the same key) but ensures the key is selected from a *non-obvious* part of the image data.
4.  **In-Memory Key**: A 32-byte slice is taken from the image's Base64 representation to serve as the AES-256 encryption key. This key **only exists in memory** while the program is running and is never stored on disk.
5.  **Secure Encryption**: All your passwords are encrypted using this key with the AES-256-CBC algorithm and stored securely in a MongoDB database.

## ✨ Features

* **Secure Encryption:** Uses AES-256, a robust, industry-trusted encryption standard.
* **Unique Key Generation:** Your key is derived from an image, making it something you *have* (the file) rather than something you just *know* (a password).
* **Advanced Key Derivation:** Instead of using a predictable part of the image, the key is derived from a randomized-yet-deterministic slice of the image data, making it resilient to simple analysis.
* **Flexible Image Input:** Choose your key on the fly:
    * ⬆️ **Upload** a local file.
    * 📸 **Take** an instant screenshot.
    * 🌐 **Fetch** a new image from the web using a search prompt.
* **Database Storage:** Securely stores encrypted credentials in a MongoDB database.

## 💻 Tech Stack

* **Language:** Python 3
* **Database:** MongoDB
* **Core Libraries:**
    * `cryptography` for AES encryption
    * `pymongo` for database interaction
    * `Pillow` & `mss` for screenshot handling
    * `requests` for fetching web images
    * `tkinter` for the file upload dialog

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

* Python 3.8 or higher
* A running instance of MongoDB on your local machine (`mongodb://localhost:27017`).

### Installation

1.  **Clone the repository**
    ```sh
    git clone [https://github.com/Dream1ance/PassVault-Image_based_Encryption](https://github.com/Dream1ance/PassVault-Image_based_Encryption/passvault_v2.git)
    cd passvault_v2
    ```

2.  **Install the required packages**
    ```sh
    pip install pymongo "cryptography>=3.4" mss Pillow requests
    ```

### Usage

Run the main application from your terminal:

```sh
python passvault_v2.py
```

The application will start and present you with a menu to choose your key source, and then you can choose to store or retrieve passwords.

## ⚠️ Security Disclaimer

The entire security of this password vault rests on the **secrecy and integrity of the source image file**.

* Anyone who gains access to the exact image file can generate the master key and decrypt your passwords.
* If the image file is modified in any way (even by a single bit), a different key will be generated, and you will lose access to your stored passwords. **Always keep a secure backup of your original key image!**

## 🧑‍💻 Authors

This project was created with passion by:

* Harish - [GitHub Profile](https://github.com/Dream1ance)
* Janarthanan - [GitHub Profile](https://github.com/jana-4)
* Arshad - [GitHub Profile](https://github.com/teammate2-username)
* Jaffer - [GitHub Profile](https://github.com/teammate2-username)

## 📄 License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
