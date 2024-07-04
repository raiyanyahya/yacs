# yacs
Yet another credential store 🔐


## Encryption and Decryption

`yacs` securely encrypts and decrypts your secrets using AES encryption with a key derived from your master password. When you initialize the credential store, a strong encryption key is generated from your master password using PBKDF2 (Password-Based Key Derivation Function 2) with a unique salt. This key, combined with a randomly generated Initialization Vector (IV), encrypts your secrets, ensuring each encryption is unique and secure. The encrypted data is then encoded in base64 format for safe storage. For added security, the tool prompts you to re-enter your master password after initialization to verify that the data can be successfully decrypted, ensuring the integrity and accessibility of your secrets.