import click
import json
from os import urandom, remove
from rich.console import Console
from rich.prompt import Prompt
import base64

from yacs.util import decrypt_message, derive_key, encrypt_message, get_credstore_path

console = Console()





def initialize_credstore(filename, password=None):
    console.print("Initializing Credential Store", style="bold green")

    credstore_path = get_credstore_path(filename)

    if credstore_path.exists():
        console.print(f"[bold red]Error:[/bold red] {credstore_path} already exists.", style="bold red")
        return

    if not password:
        password = Prompt.ask("Enter master password", password=True)

    salt = urandom(16)
    key = derive_key(password, salt)
    credstore = {
        "secrets": {},
        "salt": base64.urlsafe_b64encode(salt).decode('utf-8')
    }

    encrypted_data = encrypt_message(key, json.dumps(credstore))

    with open(credstore_path, 'w') as file:
        json.dump({"data": encrypted_data, "salt": base64.urlsafe_b64encode(salt).decode('utf-8')}, file)

    console.print(f"[bold green]Credential store initialized successfully.[/bold green] File created: {credstore_path}")

    # Verification step
    verify_password = Prompt.ask("Re-enter master password to verify", password=True)
    verify_key = derive_key(verify_password, salt)
    with open(credstore_path, 'r') as file:
        stored_data = json.load(file)
    try:
        decrypted_data = decrypt_message(verify_key, stored_data["data"])
        if decrypted_data:
            console.print("[bold green]Password verified successfully.[/bold green] Data decrypted correctly.")
    except UnicodeDecodeError:
        console.print("[bold red]Password verification failed.[/bold red]")
        remove(credstore_path)
        return
    except Exception:
        console.print("[bold red]Password verification failed.[/bold red]")
        remove(credstore_path)
        return
    
        


@click.command("init")
@click.option('--filename', default='credstore.json', help='The name of the credential store file.')
@click.option('--password', help='The master password for the credential store.')
def initialize(filename, password) -> None:
    """Initialize an empty local credstore."""
    initialize_credstore(filename, password)

