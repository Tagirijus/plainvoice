'''
DataModelPopulator class

This class is for populating fields in DataModel objects. Basically it will
offe rthe feature that in string fields of DataModel objects the user can
enter things like `{{ this.get('title') }}` so that this content will be
replaced with the content of the data models field _title_. The syntax here
is _Jinja_, giving the possibility to also include logic, for example. If a
field should be populated / replaced with a jinja string itself, e.g. for
later use, when deriving from a preset, such should be written:
`{% raw %}{{ this.get('title') }}{% endraw %}`.
This way Jinja will output the content inside the raw-tag like it is, instead
of rendering it.
'''

from plainvoice.model.data.data_model import DataModel

from datetime import datetime
from jinja2 import Template

import re


class DataModelPopulator:
    '''
    Class for replacing fields in data model fields.
    '''

    def __init__(self, **kwargs):
        '''
        Initiate the DataModelPopulator, which can get variables
        under certain keywords, which will be accessible in the
        replacement later. The replacement is based on Jinja
        templates. So if something like {{ var_1 }} should be
        accessed in the template, here in the init() method
        it should be transfered with init(var_1=THE_VARIABLE).

        Args:
            **kwargs (Object): \
                Any variables under certain needed keywords. \
                These are basically additional optional variables, \
                which can be used in the populating later.
        '''
        self.data = self.prepare_main_data(**kwargs)

    def build_dependency_graph(self, data_dict: dict) -> dict:
        '''
        Build a dependency graph based on the placeholders used in each field.
        Means: create a dictionary which have field names as keys and their
        value is a list with fieldnames, they depend on. This represents
        fields (keys), which have other fields (values) as palceholder in
        themself.

        Args:
            data_dict (dict): The data model as a readable dict.
        '''
        graph = {}
        for field, template in data_dict.items():
            if not isinstance(template, str):
                continue
            placeholders = self.find_placeholders(template)
            if field not in graph:
                graph[field] = []
            for ph in placeholders:
                graph[field].append(ph)
        return graph

    def find_placeholders(self, template: str) -> list:
        '''
        Return a list of fieldnames, which are referenced in the given
        template string. The pattern to find a referenced fieldname
        to the data model itself is (human readable): " this.get('FIELDNAME'"

        Args:
            template (str): \
                The template string, which might contain placeholders.

        Returns:
            list: Returns the found referenced fieldnames as a list.
        '''
        return re.findall(r'\sthis\.get\([\'\"](\w+)[\'\"]', template)

    def populate(self, data_model: DataModel) -> None:
        '''
        Populate the given data model.

        Args:
            data_model (DataModel): The date model to populate.
        '''
        data_dict = data_model.to_dict(True)
        graph = self.build_dependency_graph(data_dict)
        fields_order = self.topological_sort(graph)
        for field in fields_order:
            self.populate_field(data_model, field)

    def populate_field(self, data_model: DataModel, fieldname: str) -> None:
        '''
        Populate the field of the given data model.

        Args:
            data_model (DataModel): \
                The data model, which should have the given field.
            fieldname (str): \
                The field name to populate.
        '''
        combined_dict = {**self.data, **{'this': data_model}}
        if data_model.field_exists_additional(fieldname):
            prepared_value = data_model.get_additional(fieldname)
            template = Template(prepared_value)
            populated_value = template.render(**combined_dict)
            data_model.set_additional(fieldname, populated_value)
        elif data_model.field_exists_fixed(fieldname):
            prepared_value = data_model.get_fixed(fieldname, True)
            template = Template(prepared_value)
            populated_value = template.render(**combined_dict)
            data_model.set_fixed(fieldname, populated_value, True)

    def prepare_main_data(self, **kwargs) -> dict:
        '''
        Prepare the internal replacement variables on the self.data
        attribute. There are some basic variables like the datetime
        object for "now" and also additional ones defined by the
        **kwargs.

        Args:
            **kwargs: Multiple optional keywords for the replacement data.

        Returns:
            dict: Returns a dict.
        '''
        output = kwargs
        output = {**output, **{'now': datetime.now()}}
        return output

    def topological_sort(self, graph) -> list:
        '''
        Perform a topological sort to find the right order of evaluation.
        Means: it will output a list of field names, where the first item
        will be processed first and the last, last. This is needed for
        referencing variables inside the same document (its fields) might
        need different order of processing, in case an earlier field in the
        list would need another later field in the list to be processed
        already. Otherwise such a field could e.g. output the placeholder
        itself again without it being populated.

        Args:
            graph (dict): \
                The dictionary containing the dependencies between \
                the data model fields.

        Returns:
            list: \
                Returns the sorted list, how the fields should be processed \
                during the population process.
        '''
        visited = set()
        order = []

        def visit(node):
            if node not in visited:
                visited.add(node)
                for neighbor in graph.get(node, []):
                    visit(neighbor)
                order.append(node)

        for node in list(graph.keys()):
            visit(node)

        return order
