'''
Some functions for handling data.
'''

from datetime import datetime

import re
import yaml


def is_valid_date(date: str) -> str:
    '''
    Check if the given string is a valid date. If it is,
    return the date string as YYYY-MM-DD.

    Args:
        date (str): The date string input.

    Returns:
        str: Returns a date string, otherwise an empty one.
    '''
    formats = ['%Y-%m-%d', '%d.%m.%Y', '%d.%m.%y']

    for fmt in formats:
        try:
            return datetime.strptime(date, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue

    return ''


def represent_multiline_str(dumper, data):
    '''
    Define a custom represent function for multiline strings.
    This way multiline strings will get dumped by YAML with
    the pipe newline style.
    '''
    if '\n' in data:
        return dumper.represent_scalar(
            'tag:yaml.org,2002:str', data, style='|'
        )
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, represent_multiline_str)


def to_yaml_string(data: dict) -> str:
    '''
    Convert a dict to a YAML string as it would be saved. This
    method exists in this class, due to the YAML representer
    being changed here.

    Args:
        data (dict): The dict, which should be converted to a YAML string.

    Returns:
        str: Returns the YAML string.
    '''
    if data:
        return yaml.dump(
            data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )
    else:
        return ''
