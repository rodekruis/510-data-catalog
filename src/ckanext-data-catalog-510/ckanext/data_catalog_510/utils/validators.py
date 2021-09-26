import datetime

import ckan.lib.navl.dictization_functions as df
from ckan.common import _

Invalid = df.Invalid


def validate_date_yyyy_mm_dd(value, context):
    ''' Method to validate the Date format string
        for the yyyy-mm-dd
    '''
    if value:
        format = "%Y-%m-%d"
        try:
            datetime.datetime.strptime(value, format)
        except ValueError:
            raise Invalid(_('This is the incorrect date string format.'
                            'It should be YYYY-MM-DD'))
        return value
    return None
