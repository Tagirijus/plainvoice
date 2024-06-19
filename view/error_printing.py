from view import printing as p

import click


def print_if_verbose(err):
    ctx = click.get_current_context()
    verbose = ctx.obj.get('verbose', 0)
    if verbose >= 1:
        p.print_warning(err)
    if verbose >= 2:
        import traceback
        p.print_formatted(traceback.format_exc())
