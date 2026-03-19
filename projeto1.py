
import random
import string

def generate_random_file(length):
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation + '') for _ in range (length))

def save_text_to_file(text, filename):
    with open(filename, 'w', encoding = 'utf-8') as f:
        f.write(text)

save_text_to_file(generate_random_file(2), 'size2.txt')
save_text_to_file(generate_random_file(4), 'size4.txt')
save_text_to_file(generate_random_file(8), 'size8.txt')
save_text_to_file(generate_random_file(16), 'size16.txt')
save_text_to_file(generate_random_file(32), 'size32.txt')
save_text_to_file(generate_random_file(64), 'size64.txt')
save_text_to_file(generate_random_file(128), 'size128.txt')
save_text_to_file(generate_random_file(512), 'size512.txt')
save_text_to_file(generate_random_file(4096), 'size4096.txt')
save_text_to_file(generate_random_file(32768), 'size32768.txt')
save_text_to_file(generate_random_file(262144), 'size262144.txt')
save_text_to_file(generate_random_file(2097152), 'size2097152.txt')


import time

def measure_time(func, *args, total=100):
    times = []
    for _ in range(total):
        start = time.perf_counter()
        func(*args)  
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / total


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def cipher(key, iv):
    return Cipher(algorithms.AES(key), modes.CFB(iv), backend = default_backend())

def encrypt_aes(plaintext, key, iv):
    encryptor = cipher(key,iv).encryptor()
    encrypted = encryptor.update(plaintext) + encryptor.finalize()
    return encrypted

def decrypt_aes(encrypted, key, iv):
    decryptor = cipher(key, iv).decryptor()
    decrypted = decryptor.update(encrypted) + decryptor.finalize()
    return decrypted

def encrypt_decrypt_aes(file_size):
    key = os.urandom(32)
    iv = os.urandom(16)

    with open(f'size{file_size}.txt', 'rb') as f:
        plaintext = f.read()
    encrypted = encrypt_aes(plaintext, key, iv)
    encryption_time = measure_time(encrypt_aes, plaintext, key, iv, total = 100)
    decryption_time = measure_time(decrypt_aes, plaintext, key, iv, total = 100)

    return encryption_time, decryption_time
    
def create_lists():
    file_sizes_aes = [8, 64, 512, 4096, 32768, 262144, 2097152]

    aes_encryption_times = []
    aes_decryption_times = []

    for file_size in file_sizes_aes:
        encryption_time, decryption_time = encrypt_decrypt_aes(file_size)

        aes_encryption_times.append(encryption_time * 1000000)
        aes_decryption_times.append(decryption_time * 1000000)
    
    return aes_encryption_times, aes_decryption_times



from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import timeit
import os


def generate_rsa_key():
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048,
        backend = default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

private_key, public_key = generate_rsa_key()

def encrypt_rsa(plaintext, public_key):
    encrypted = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )
    return encrypted


def decrypt_rsa(encrypted, private_key):
    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted


def encrypt_decrypt_rsa(file_size):

    with open(f'size{file_size}.txt', 'rb') as f:
        plaintext = f.read()

    encrypted = encrypt_rsa(plaintext, public_key)
    encryption_time = measure_time(encrypt_rsa, plaintext, public_key, total = 100)
    decryption_time = measure_time(decrypt_rsa, encrypted, private_key, total = 100)

    return encryption_time, decryption_time

def rsa_lists():
    file_sizes_rsa = [2, 4, 8, 16, 32, 64, 128]

    rsa_encryption_times = []
    rsa_decryption_times = []

    for file_size in file_sizes_rsa:
        encryption_time, decryption_time = encrypt_decrypt_rsa(file_size)
        rsa_encryption_times.append(encryption_time * 1000000)
        rsa_decryption_times.append(decryption_time * 1000000)

    return rsa_encryption_times, rsa_decryption_times


from cryptography.hazmat.primitives import hashes
import timeit
import random
import string

def generate_random_text(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def save_text_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

def sha256(plaintext):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(bytes(plaintext, "utf-8"))
    return digest.finalize()
    
def sha_list():
    sha_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]
    sha_hash_generation_time = []
    
    for file_size in sha_sizes:
        save_text_to_file(generate_random_text(file_size), f'size{file_size}.txt')
        
        with open(f'size{file_size}.txt', 'r') as f:
            plaintext = f.read()
            execution_time = measure_time(sha256, plaintext, total = 100)
        sha_hash_generation_time.append(execution_time * 1000000)  # Convert to microseconds
    return sha_hash_generation_time


import pandas as pd

aes_encryption_times, aes_decryption_times = create_lists()
rsa_encryption_times, rsa_decryption_times = rsa_lists()
sha_hash_generation_time = sha_list()

file_sizes_aes = [8, 64, 512, 4096, 32768, 262144, 2097152]
file_sizes_rsa = [2, 4, 8, 16, 32, 64, 128]
file_sizes_sha = [8, 64, 512, 4096, 32768, 262144, 2097152]

all_file_sizes = sorted(set(file_sizes_aes + file_sizes_rsa + file_sizes_sha))

df = pd.DataFrame(columns=["File Size (bytes)", "AES Encryption Time (µs)", "AES Decryption Time (µs)", "RSA Encryption Time (µs)", "RSA Decryption Time (µs)", "SHA-256 Digest Time (µs)"])

data = []

for file_size in all_file_sizes:
    # AES
    aes_encryption_time = aes_encryption_times[file_sizes_aes.index(file_size)] if file_size in file_sizes_aes else None
    aes_decryption_time = aes_decryption_times[file_sizes_aes.index(file_size)] if file_size in file_sizes_aes else None

    # RSA
    rsa_encryption_time = rsa_encryption_times[file_sizes_rsa.index(file_size)] if file_size in file_sizes_rsa else None
    rsa_decryption_time = rsa_decryption_times[file_sizes_rsa.index(file_size)] if file_size in file_sizes_rsa else None

    # SHA
    sha_time = sha_hash_generation_time[file_sizes_sha.index(file_size)] if file_size in file_sizes_sha else None

    data.append({
        "File Size (bytes)": file_size,
        "AES Encryption Time (µs)": round(aes_encryption_time, 3) if aes_encryption_time is not None else "/",
        "AES Decryption Time (µs)": round(aes_decryption_time, 3) if aes_decryption_time is not None else "/",
        "RSA Encryption Time (µs)": round(rsa_encryption_time, 3) if rsa_encryption_time is not None else "/",
        "RSA Decryption Time (µs)": round(rsa_decryption_time, 3) if rsa_decryption_time is not None else "/",
        "SHA-256 Digest Time (µs)": round(sha_time, 3) if sha_time is not None else "/"
    })

df = pd.DataFrame(data)

df.to_csv("tabela.csv", index=False)
print(df)


import matplotlib.pyplot as plt
import numpy as np

aes_encryption_times_us = np.array(aes_encryption_times) 
aes_decryption_times_us = np.array(aes_decryption_times) 

rsa_encryption_times_us = np.array(rsa_encryption_times)
rsa_decryption_times_us = np.array(rsa_decryption_times) 

sha_digest_times_us = np.array(sha_hash_generation_time) 


file_labels_aes = [f"Size {s}" for s in file_sizes_aes]
file_labels_rsa = [f"Size {s}" for s in file_sizes_rsa]
file_labels_sha = [f"Size {s}" for s in file_sizes_sha]

# Gráfico AES - encryption / decryption
plt.figure(figsize = (10, 6))
plt.plot(file_labels_aes, aes_encryption_times_us, label = 'Mean Values (Encryption time)', marker = 'o', color = 'b')
plt.plot(file_labels_aes, aes_decryption_times_us, label = 'Mean Values (Decryption time)', marker = 'o', color = 'r')
plt.xlabel('File size')
plt.ylabel('Time in microsseconds')
plt.title('Mean values of AES encryption / decryption')
plt.legend()
plt.xticks(rotation = 45)
plt.yticks(np.arange(0, 3501, 500)) 
plt.ylim(-100, 3450)
plt.grid(True)
plt.show()


# Gráfico RSA  - encryption / decryption
plt.figure(figsize = (10, 6))
plt.plot(file_labels_rsa, rsa_encryption_times_us, label = 'Mean Values (Encryption time)', marker = 's', color = 'g')
plt.plot(file_labels_rsa, rsa_decryption_times_us, label = 'Mean Values (Decryption time)', marker = 's', color = 'm')
plt.xlabel('File size')
plt.ylabel('Time in microsseconds')
plt.title('Mean values of RSA encryption / decryption')
plt.legend()
plt.xticks(rotation =  45)
plt.yticks(np.arange(0, 1000 , 200))
plt.ylim(-100,1050)
plt.grid(True)
plt.show()


# Gráfico SHA-256 
plt.figure(figsize = (10, 6))
plt.plot(file_labels_sha, sha_digest_times_us, label = 'Mean Values Digest Time', marker = 'd', color = 'orange')
plt.xlabel('File size')
plt.ylabel('Time in microsseconds')
plt.title('Mean values of SHA digest generation time')
plt.legend()
plt.xticks(rotation = 45)
plt.yticks(np.arange(0, 3001, 500))  
plt.ylim(-200,3000)
plt.grid(True)
plt.show()