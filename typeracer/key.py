import base64
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password_provided = "lmaolmaolmao"
password = password_provided.encode()

salt = b'o\xce\x9e\xbd\xce\xf8\xcb\x05\xaf\x9f\x11\xeaQ\xf7\xa8q'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
global encrypted


def encrypt():
    with open('creds.txt', 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    main()


def decrypt():
    with encrypted as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)

    with open('creds.txt.decrypted', 'wb') as f:
        f.write(encrypted)
    main()


def main():
    choice = int(input("Encrypt(1) or Decrypt(2)?"))

    if choice == 1:
        encrypt()
    elif choice == 2:
        decrypt()
    elif choice != 1 or 2:
        print("Invalid argument, please try again.")
        time.sleep(2)
        main()


main()
