'''
Some functions for handling data.
'''

import yaml


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
