import json
import base64
import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from yacs.util import derive_key, decrypt_message, get_credstore_path

console = Console()

def view_secrets(filename):
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

    if secrets:
        for key, secret_info in secrets.items():
            console.print(f"Key: {key} Description: {secret_info['description']}\n")
    else:
        console.print("[bold yellow]No secrets found.[/bold yellow]")


@click.command("view")
@click.option('--filename', default='credstore.json', help='The name of the credential store file.')
def view(filename):
    """View all keys and their descriptions."""
    view_secrets(filename)