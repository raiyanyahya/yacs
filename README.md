# yacs
Yet another credential store 🔐

`yacs` is a command-line tool that allows you to securely store, manage, and retrieve secrets locally in an encrypted JSON file. This tool uses AES encryption with a master password to ensure your secrets are kept safe.

## Features

Initialization: Set up a new credential store with a master password and a hint.
Adding Secrets: Add secrets with descriptions, supporting both string and binary types.
Retrieving Secrets: Retrieve secrets by their key.
Viewing Keys and Descriptions: List all keys and their descriptions.
Resetting: Delete the credential store and start from scratch.


## Encryption and Decryption

`yacs` securely encrypts and decrypts your secrets using AES encryption with a key derived from your master password. When you initialize the credential store, a strong encryption key is generated from your master password using PBKDF2 (Password-Based Key Derivation Function 2) with a unique salt. This key, combined with a randomly generated Initialization Vector (IV), encrypts your secrets, ensuring each encryption is unique and secure. The encrypted data is then encoded in base64 format for safe storage. For added security, the tool prompts you to re-enter your master password after initialization to verify that the data can be successfully decrypted, ensuring the integrity and accessibility of your secrets.

## Security
The Local Secrets Manager uses AES encryption with a key derived from your master password using PBKDF2 (Password-Based Key Derivation Function 2) with a unique salt. This ensures that your secrets are securely encrypted and can only be decrypted with the correct master password.


## Usage
Install the command line interface via the cli.

    ```
    pip install yacs-cli
    ```

After installing you should be able to see the below when you run `yacs`.
    ```
    @raiyanyahya ➜ /workspaces/yacs (master) $ yacs
    Usage: yacs [OPTIONS] COMMAND [ARGS]...

    A cli to provision and manage local developer environments.

    Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

    Commands:
    get    Get a secret from the credential store.
    init   Initialize an empty local credstore.
    put    Add a secret to the credential store.
    reset  Delete the credstore and start from scratch.
    view   View all keys and their descriptions.
    ```
### Initialize the store

    ```
    yacs init
    ```

### Add a secret

    ```
    yacs put /mykey "description" mysecretstring
    ```

### Get a secret

    ```
    yacs get /mykey
    ```
### View all keyand descriptions

    ```
    yacs view
    ```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
