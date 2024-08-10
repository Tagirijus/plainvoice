from plainvoice.utils import data_utils


def test_yaml_multiline_string():
    # create a test dict, which should contain
    # a multiline string, which will hopefully
    # be converted correctly in YAML
    the_dict = {
        'multiline': 'line a\nline b\nline c'
    }

    # convert and check the output
    the_yaml_string = data_utils.to_yaml_string(the_dict)
    assert the_yaml_string == 'multiline: |-\n  line a\n  line b\n  line c\n'
