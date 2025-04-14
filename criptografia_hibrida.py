
#Generate a random text
import random
import string
def generate_random_text(length):
 #AES Encrypts and decrypts data in 128-bit blocks (16 bytes)
  if length%16!=0:
    raise ValueError("AES text must be a multiple of 16 bytes")
  else:
    return ''.join(random.choices(string.ascii_letters, k=length))

generate_random_text(16)

#Message encryption
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

aes_key=get_random_bytes(16)
nonce = get_random_bytes(12)         # nonce with 12 bytes
plain_text=generate_random_text(16)
print("Plain text:",plain_text) #string

#Creating an AES object in GCM mode
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))

print("Ciphertext:", ciphertext.hex())
print("Tag:", tag.hex())

#Symmetric key encryption using the receiver's public key using the RSA algorithm
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#RSA key generation:
key_pair = RSA.generate(2048)
private_key = key_pair
public_key = key_pair.publickey()

#Sender encrypts symmetric key with public key:

rsa_cipher = PKCS1_OAEP.new(public_key) #Padding OAEP (Optimal Asymmetric Encryption Padding)
aes_key_encrypted = rsa_cipher.encrypt(aes_key)

import json, base64

with open("payload.json", "w") as f:

    json.dump({
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "aes_key_encrypted": base64.b64encode(aes_key_encrypted).decode()
    }, f)

try:
    with open("payload.json", "r") as file:

        payload = json.load(file)  # Parse JSON into a Python dictionary
except FileNotFoundError:
    print("File not found. Please check the path or filename.")
except json.JSONDecodeError:
    print("Invalid JSON format. Please check the file content.")

# Proceed with decoding if payload was successfully loaded
try:
    ciphertext = base64.b64decode(payload["ciphertext"])
    tag = base64.b64decode(payload["tag"])
    nonce = base64.b64decode(payload["nonce"])
    aes_key_encrypted = base64.b64decode(payload["aes_key_encrypted"])
except KeyError as e:
    print(f"Missing expected field in JSON payload: {e}")

#The receiver uses their RSA private key to decrypt the symmetric key
rsa_dec_cipher = PKCS1_OAEP.new(private_key)
aes_key_decrypted = rsa_dec_cipher.decrypt(aes_key_encrypted)

# Then, the decrypted AES key is used to create a new AES cipher object
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
try:
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    print("Decryption successful. Message is authentic.")
except ValueError:
    print("Decryption failed or message has been tampered with.")

print("Plaintext:", plaintext.decode('utf-8'))
print("Tag:", tag.hex())