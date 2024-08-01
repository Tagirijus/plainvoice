from plainvoice.model.client.client import Client


def test_client_fixed_fields():
    # first I create a new Client instance
    # with a specific id
    client = Client('tagi')

    # now I check if the id was set correctly
    assert client.get_client_id() == 'tagi'

    # and then I check if some default fiexed
    # fields where set correctly
    assert client.get_fixed('attention') == 'Attn.'
    assert client.get_fixed('salutation') == 'Mr.'
