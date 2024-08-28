from plainvoice.model.template.template_repository import TemplateRepository

import os


def test_create_default_template(
    test_data_folder,
    test_data_file
):
    # set the test data folder
    test_folder = test_data_folder('render_tests')
    templates_folder = test_folder + '/templates'
    test_file = test_data_file('render_tests/templates/new_template.jinja')

    # create a TemplateRepository instance
    template_repo = TemplateRepository(templates_folder)

    # create a new template from scratch
    template_repo.create_template('new_template')

    # this file should now exist in the templates folder
    assert os.path.exists(test_file) is True
    # remove the file again
    os.unlink(test_file)


def test_get_template_names(test_data_folder):
    # set the test data folder
    test_folder = test_data_folder('render_tests')
    templates_folder = test_folder + '/templates'

    # create a TemplateRepository instance
    template_repo = TemplateRepository(templates_folder)

    # now get the template names as a list. in the test setting
    # this is just one file
    template_names = template_repo.get_template_names()

    # 'invoice' should be in this list
    assert 'invoice' in template_names
