from cryptography.fernet import Fernet
import base64

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(plaintext)
    with open(file_path + ".encrypted", 'wb') as f:
        f.write(encrypted)

# Key
key = base64.urlsafe_b64encode(b'Testisstudent1234567890987654321')

encrypt_file("c2_client.py", key)
print("File is encrypted!.")
