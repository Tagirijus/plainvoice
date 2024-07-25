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


def datetime_from_dict_key(
    dic: dict[str, object],
    key: str,
    default: str = ''
) -> datetime | None:
    '''
    This method tries to get a datetime from the value
    of the dict with the given key. If there is no
    value behind that key, a new datetime will be
    created instead and returned, if "default" is set
    to "now". Otherwise None gets returned.

    Well, if there is a datetime behind that dicts key,
    this will get returned, of course.

    Args:
        dic (dict): \
            The dict to use this method on.
        key (str): \
            The key containing the datetime.
        default (str): \
            If the default is "now", the datetime,
            when not possible to get, will be
            today. (default: `''`)

    Returns:
        datetime | None: Returns the datetime or None.
    '''
    date_tmp = dic.get(
        key,
        datetime.now() if default == 'now' else None
    )
    if not isinstance(date_tmp, datetime) and date_tmp is not None:
        return datetime.strptime(str(date_tmp), '%Y-%m-%d')
    else:
        return date_tmp
