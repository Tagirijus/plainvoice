from datetime import datetime


def datetime2str(value: datetime) -> str:
    '''
    Simply convert a datetime to an ISO 8601 formatted string.

    Args:
        value (datetime): Must be a datetime to get the date from.

    Returns:
        str: The ISO 8601 date string.
    '''
    return (
        value.strftime('%Y-%m-%d')
    )
