import click
import json
import base64
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from yacs.util import derive_key, decrypt_message, get_credstore_path

console = Console()


def get_secret(filename, key):
    credstore_path = get_credstore_path(filename)

    if not credstore_path.exists():
        console.print(f"[bold red]Error:[/bold red] {credstore_path} does not exist.", style="bold red")
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

    if key in secrets:
        secret_info = secrets[key]
        if secret_info["type"] == "binary":
            secret = base64.urlsafe_b64decode(secret_info["secret"].encode()).decode('utf-8')
        else:
            secret = secret_info["secret"]

        console.print(f"{secret}", style="bold green")
    else:
        console.print(f"[bold red]Error:[/bold red] Key '{key}' not found.", style="bold red")


@click.command("get")
@click.option('--filename', default='credstore.json', help='The name of the credential store file.')
@click.argument('key')
def get(filename, key):
    """Get a secret from the credential store."""
    get_secret(filename, key)