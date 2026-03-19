# Performance-Benchmarking-Cryptography
This project was developed for the Security and Privacy (2nd year course) at the Faculty of Sciences, University of Porto (FCUP). The goal is to measure and analyze the execution time of various cryptographic primitives using Python.


## Project Overview
The analysis focuses on the performance of symmetric encryption, asymmetric encryption, and hash functions across different file sizes to ensure statistically significant results.


## Technical Stack
* [cite_start]**Language:** Python 3.11.7 [cite: 164]
* [cite_start]**Libraries:** `cryptography.hazmat`, `pandas`, and `matplotlib` [cite: 166]
* [cite_start]**Experimental Setup:** macOS-14.3.1-arm64 (Apple Silicon) [cite: 161]


## Implemented Algorithms
**1. AES (Advanced Encryption Standard)**

Configuration: 256-bit key using CFB mode

Testing Range: Files from 8 bytes up to 2,097,152 bytes

Observation: Encryption and decryption times are nearly identical for smaller files, increasing linearly as the file size grows

**2. RSA (Rivest-Shamir-Adleman)**

Configuration: 2048-bit key with OAEP padding

Testing Range: Small files (2 to 128 bytes) due to RSA's architectural limits

Performance: Decryption is significantly slower (~1435 µs) than encryption (~46 µs)

**3. SHA-256 (Secure Hash Algorithm)**

Function: Generation of fixed-size 256-bit hash digests

Efficiency: SHA-256 proved to be the fastest mechanism, often taking half the time required by AES for the same file sizes

## Experimental Results
[cite_start]The following table shows the mean execution time (in microseconds) for each algorithm, based on 100 iterations per file size[cite: 167]:

| File Size (Bytes) | AES Encryption (µs) | AES Decryption (µs) | RSA Encryption (µs) | RSA Decryption (µs) | SHA-256 Digest (µs) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2** | N/A | N/A | 47.538 | 1540.563 | N/A |
| **4** | N/A | N/A | 46.733 | 1419.660 | N/A |
| **8** | 22.603 | 23.418 | 48.114 | 1419.118 | 12.199 |
| **16** | N/A | N/A | 46.399 | 1416.970 | N/A |
| **32** | N/A | N/A | 46.783 | 1419.368 | N/A |
| **64** | 18.188 | 18.992 | 46.599 | 1420.648 | 6.441 |
| **128** | N/A | N/A | 45.355 | 1414.271 | N/A |
| **512** | 19.047 | 20.100 | N/A | N/A | 6.518 |
| **4096** | 25.109 | 24.897 | N/A | N/A | 8.128 |
| **32768** | 72.123 | 68.990 | N/A | N/A | 24.320 |
| **262144** | 467.589 | 417.524 | N/A | N/A | 154.710 |
| **2097152** | 3809.431 | 3405.309 | N/A | N/A | 1338.284 |


[!NOTE]
RSA results for large files are marked as N/A because asymmetric encryption is not designed for bulk data processing.


## How to Run
Install the required dependencies:

pip install cryptography pandas matplotlib

Run the benchmarking script:

python projeto1.py



This project was elaborated by: Filipa Melo Leite & Luana Letra Gibbels.
