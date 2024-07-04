import click
from yacs import inititialize, reset
@click.group()
@click.version_option()
def cli() -> None:
    """A cli to provision and manage local developer environments."""



cli.add_command(inititialize.initialize)
cli.add_command(reset.reset)