# passvault_v2.py

import pymongo
from getpass import getpass # For securely typing passwords
from imagenc_v2 import generate_key_from_image, encrypt_password, decrypt_password
from image_handler import get_image_from_upload, get_image_from_screenshot, get_image_from_web

# --- Database Connection ---
try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    # The ismaster command is cheap and does not require auth.
    myclient.admin.command('ismaster')
    db = myclient["vault"]
    col = db["keys"]
    print("✅ Successfully connected to MongoDB.")
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(f"❌ Could not connect to MongoDB: {err}")
    exit()


def get_key():
    """
    Guides user to select an image source and generates a key.
    """
    print("\n--- Key Generation ---")
    print("Choose an image source to generate the key:")
    print("1. Upload an image from your computer")
    print("2. Take a screenshot")
    print("3. Fetch a random image from the web")
    
    choice = input("Enter your choice (1/2/3): ")
    
    image_data = None
    if choice == '1':
        image_data = get_image_from_upload()
    elif choice == '2':
        image_data = get_image_from_screenshot()
        print("✅ Screenshot captured.")
    elif choice == '3':
        prompt = input("What do you want an image of? (e.g., 'nature', 'cats'): ")
        image_data = get_image_from_web(prompt)
    else:
        print("Invalid choice.")
        return None

    if image_data:
        print("🔑 Image loaded, generating key...")
        return generate_key_from_image(image_data)
    else:
        print("❌ Key generation failed: No image data.")
        return None

def insert(key):
    """Function to insert encrypted password into MongoDB"""
    name = input("Username: ")
    src = input("Service/Website (e.g., Google, Facebook): ")
    passw = getpass("Password: ")

    encrypted_password = encrypt_password(passw, key)
    data = {"name": name, "src": src, "pass": encrypted_password}

    col.insert_one(data)
    print("\n✅ Password Encrypted & Stored Successfully!")

def retrieve(key):
    """Function to retrieve and decrypt password"""
    name = input("Username: ")
    src = input("Service/Website: ")
    
    query = {"name": name, "src": src}
    res = col.find_one(query)
    
    if res:
        encrypted_password = res["pass"]
        decrypted_password = decrypt_password(encrypted_password, key)
        print("="*20)
        print("🔓 Decrypted Password:", decrypted_password)
        print("="*20)

    else:
        print("❌ No matching record found!")

def main():
    # This key is derived from the image and only stored in memory
    encryption_key = get_key()
    
    if not encryption_key:
        return # Exit if key generation failed

    # Note: In a real app, you would add a master password here to encrypt/decrypt
    # the 'encryption_key' itself for another layer of security.

    while True:
        print("\n--- Password Vault Menu ---")
        print("1. Store a new password")
        print("2. Retrieve a password")
        print("3. Exit")
        
        action = input("Choose an action (1/2/3): ")
        
        if action == '1':
            insert(encryption_key)
        elif action == '2':
            retrieve(encryption_key)
        elif action == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()