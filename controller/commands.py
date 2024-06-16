import click
from model.settings import Settings
from controller import utils


@click.group(
    context_settings=dict(help_option_names=['-h', '--help'])
)
@click.pass_context
# @click.option('-v', '--verbose', is_flag=True, help='Enable verbose mode')
def cli(ctx):
    """
    Creating invoices and quotes with a plaintext mindset.
    """
    pass
    # ctx.obj = OBJECT()


@cli.command()
def config():
    """Open the config in the defined editor. By default this is vi."""
    utils.edit_config()
