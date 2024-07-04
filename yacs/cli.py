import click
from yacs import inititialize, reset, put, get, view
@click.group()
@click.version_option()
def cli() -> None:
    """A cli to provision and manage local developer environments."""



cli.add_command(inititialize.initialize)
cli.add_command(reset.reset)
cli.add_command(put.put)
cli.add_command(get.get)
cli.add_command(view.view)