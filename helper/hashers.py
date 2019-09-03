from cryptography.fernet import Fernet
import base64
import hashlib
from django.conf import settings
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64decode


def generating_key(passphrase=None):
    key_pair = RSA.generate(4096)
    private_key = open("file_down/private_key.pem", "wb")
    private_key.write(key_pair.exportKey(passphrase=passphrase, pkcs=1))
    private_key.close()

    public_key = open("file_down/public_key.pem", "wb")
    public_key.write(key_pair.publickey().exportKey(passphrase=passphrase, pkcs=1))
    public_key.close()

    password = open("file_down/passpharse.pem", "wb")
    password.write(passphrase.encode('utf-8'))
    password.close()


def encrypt_base64(txt):
    try:
        # # convert integer etc to string first
        # txt = str(txt)
        # # get the key from settings
        # cipher_suite = Fernet(ENCRYPT_KEY)  # key should be byte
        # # #input should be byte, so convert the text to byte
        # encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # # encode to urlsafe base64 format
        # encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        # return encrypted_text

        txt = str(txt)
        enc = txt.encode('ascii')
        encrypted_text = base64.urlsafe_b64encode(enc).decode("ascii")
        return encrypted_text
    except Exception as e:
        # log the error if any
        print('Error: %s' % e)
        return None


def decrypt_base64(txt):
    try:
        # # base64 decode
        # txt = base64.urlsafe_b64decode(txt)
        # cipher_suite = Fernet(ENCRYPT_KEY)
        # decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        # return decoded_text

        decoded_text = base64.urlsafe_b64decode(txt).decode("ascii")
        return decoded_text
    except Exception as e:
        # log the error
        print('Error: %s' % e)
        return None


def encrypt(txt):
    try:
        message = str(txt)
        message = message.encode('ascii')
        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        encrypted = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted
    except Exception as e:
        print('Error: %s' % e)
        return None


def decrypt(encrypted_data):
    try:
        # Read passpharse
        passphrase = open('file_down/passpharse.pem', 'rb')
        # Open key file
        f = open('file_down/private_key.pem', 'rb')
        key = RSA.importKey(f.read(), passphrase=passphrase.read())
        # Decode base64 data
        decoded_data = b64decode(encrypted_data)
        # Decrypt data
        cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        result = cipher.decrypt(decoded_data)
        return result
    except Exception as e:
        print('Error: %s' % e)
        return False
