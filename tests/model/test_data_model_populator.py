from plainvoice.model.data.data_model import DataModel
from plainvoice.model.data.data_model_populator import DataModelPopulator

from datetime import datetime


def test_data_model_replacements():
    # create a data model
    data_model = DataModel()

    # create all available fields
    data_model.define_fixed_field_type('str', str, str)
    data_model.add_field_descriptor('title', 'str', '')
    data_model.add_field_descriptor('comment', 'str', '')
    data_model.add_field_descriptor('code', 'str', '')
    data_model.add_field_descriptor('date_str', 'str', '')
    data_model.add_field_descriptor('for_render', 'str', '')

    # fill the fields with placeholders
    data_model.set_fixed('title', 'title is: "{{ this.get("code") }}"')
    data_model.set_fixed(
        'comment', 'code in title "{{ this.get("title") }}" is "{{ this.get("code") }}"'
    )
    data_model.set_fixed('code', '{{ now.strftime("%Y%m%d") }}')
    data_model.set_fixed(
        'date_str',
        # this tries to make the string gets replaced to
        # "{{ now.strftime("%Y%m%d") }}", which will lead
        # to itself being replaced finally only in another
        # populating run. this way I could technically
        # have replacement string-"presets", or maybe
        # content which will only be populated on
        # rendering or for the script execution
        '{% raw %}{{ now.strftime("%Y%m%d") }}{% endraw %}',
    )
    data_model.set_fixed(
        'for_render',
        '{% raw %}title on rendering is: {{ this.get("title") }}{% endraw %}',
    )

    # also set an additional field, which will access an
    # optional extra transfered veriable for the populator
    data_model.set_additional('additional', '{{ extra }}')

    # now prepare the populator
    additional = 'extra variable'
    populator = DataModelPopulator(extra=additional)

    # populate the data model
    populator.populate(data_model)

    # check if fields got populated correctly
    # for that first prepare the strings manually

    # since I am using the today date, create a dynamic string
    # which will be used in the asserting later and which will
    # always be the same as in the populating output. otherwise
    # if this would be hard coded, the test would not be true,
    # if ran on another day then ... on the time writing it!
    code = datetime.now().strftime('%Y%m%d')

    # now the other strings ...
    title = f'title is: "{code}"'
    comment = f'code in title "{title}" is "{code}"'
    date_str = '{{ now.strftime("%Y%m%d") }}'
    for_render = 'title on rendering is: {{ this.get("title") }}'

    assert data_model.get('title', True) == title
    assert data_model.get('comment', True) == comment
    assert data_model.get('code', True) == code
    assert data_model.get('date_str', True) == date_str
    assert data_model.get('for_render', True) == for_render
    assert data_model.get('additional', True) == additional
