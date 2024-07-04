import click
from os import remove
from rich.console import Console
from rich.prompt import Confirm, Prompt
import base64
import json
from yacs.util import decrypt_message, derive_key, get_credstore_path

console = Console()


def reset_credstore(filename):
    credstore_path = get_credstore_path(filename)

    if not credstore_path.exists():
        console.print(f"[bold red]Error:[/bold red] {credstore_path} does not exist.", style="bold red")
        return

    password = Prompt.ask("Enter master password to confirm reset", password=True)

    with open(credstore_path, 'r') as file:
        stored_data = json.load(file)
        salt = base64.urlsafe_b64decode(stored_data["salt"].encode('utf-8'))
        key = derive_key(password, salt)

        try:
            decrypt_message(key, stored_data["data"])
        except UnicodeDecodeError:
            console.print("[bold red]Password verification failed.[/bold red]")
            return
        except Exception:
            console.print("[bold red]Password verification failed.[/bold red]")
            return

    confirm = Confirm.ask("Are you sure you want to delete the credential store and all its contents?", default=False)
    if confirm:
        remove(credstore_path)
        console.print(f"[bold green]Credential store {credstore_path} deleted successfully.[/bold green]")
    else:
        console.print("[bold yellow]Reset operation cancelled.[/bold yellow]")


@click.command("reset")
@click.option('--filename', default='credstore.json', help='The name of the credential store file.')
def reset(filename):
    """Delete the credstore and start from scratch."""
    reset_credstore(filename)