from view import printing as p

import click


def print_if_verbose(err: Exception) -> None:
    """
    This function checks if "verbose" is enabled and then
    prints out error messages with traceback on level 2
    of verbosity.

    Args:
        err (str): The error message to display.
    """
    ctx = click.get_current_context()
    verbose = ctx.obj.get('verbose', 0)
    if verbose >= 1:
        p.print_warning(str(err))
    if verbose >= 2:
        import traceback
        p.print_formatted(traceback.format_exc())
