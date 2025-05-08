
import click
import json
import base64
from rich.console import Console
from rich.prompt import Prompt
from yacs.util import derive_key, encrypt_message, decrypt_message, get_credstore_path

console = Console()


def put_secret(filename, key, description, secret, secret_type):
    credstore_path = get_credstore_path(filename)

    if not credstore_path.exists():
        console.print(f"[bold red]Error:[/bold red] {credstore_path} does not exist. Initialize a new store.", style="bold red")
        return

    password = Prompt.ask("Enter master password", password=True)

    with open(credstore_path, 'r') as file:
        stored_data = json.load(file)
        salt = base64.urlsafe_b64decode(stored_data["salt"].encode('utf-8'))
        encryption_key = derive_key(password, salt)
        
        try:
            decrypted_data = json.loads(decrypt_message(encryption_key, stored_data["data"]))
        except UnicodeDecodeError:
            console.print("[bold red]Password verification failed.Try again.[/bold red]")
            return
        except Exception:
            console.print("[bold red]Password verification failed.Try again.[/bold red]")
            return

    secrets = decrypted_data["secrets"]
    if secret_type == "binary":
        secret = base64.urlsafe_b64encode(secret.encode()).decode('utf-8')
    secrets[key] = {"description": description, "secret": secret, "type": secret_type}

    decrypted_data["secrets"] = secrets
    updated_encrypted_data = encrypt_message(encryption_key, json.dumps(decrypted_data))

    with open(credstore_path, 'w') as file:
        json.dump({"data": updated_encrypted_data, "salt": stored_data["salt"]}, file)

    console.print(f"[bold green]Secret for key '{key}' added successfully.[/bold green]")


@click.command("put")
@click.option('--filename', default='credstore.json', help='The name of the credential store file.')
@click.argument('key')
@click.argument('description')
@click.option('--type', 'secret_type', type=click.Choice(['string', 'binary']), default='string', help='The type of the secret: string or binary.')
def put(filename, key, description, secret_type):
    """Add a secret to the credential store."""
    secret = Prompt.ask("Enter the secret", password=True)
    put_secret(filename, key, description, secret, secret_type)