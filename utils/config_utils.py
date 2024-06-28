import os
import subprocess
from model.file import File
from model.settings import Settings
from view import printing as p
import yaml


def open_in_editor(filename):
    S = Settings()

    p.print_formatted(
        f'Opening "{filename}"'
        + f' with "{S.EDITOR}" ...'
    )

    subprocess.run([S.EDITOR, filename])


def edit_config():
    S = Settings()

    # probably for the first time, create the config file
    if not os.path.exists(S.CONFIGFILE):
        p.print_formatted(f'Creating default "config" at "{S.DATADIR}/" ...')
    # then save it, yet also save it eveytime to fill new attributes, which
    # were added later in the development
    FileYAML().save(S.get_config_as_dict(), S.CONFIGFILE)
    # now load it
    open_in_editor(S.CONFIGFILE)
