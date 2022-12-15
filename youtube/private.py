from datetime import datetime

import pytz

from pyrfc3339 import generate
from youtube import constants


def get_headers():
    return {'Content-Type': 'application/json'}


def get_datetime_in_rfc3339(year=0, month=0, day=0, hour=0, minute=0, second=0):
    if year and month and day:
        return generate(
            datetime(year, month, day, hour, minute, second).replace(tzinfo=pytz.utc)
        )
    return generate(datetime.utcnow().replace(tzinfo=pytz.utc))


def get_params(
    key=constants.API_KEY,
    type='video',
    order='date',
    published_after=get_datetime_in_rfc3339(),
    search_query=constants.PREDEFINED_SEARCH_QUERY,
    max_results=5,
    part='snippet'
):
    return {
        constants.AUTH_KEY: key,
        constants.TYPE_KEY: type,
        constants.ORDER_KEY: order,
        constants.PUBLISHED_AFTER_KEY: published_after,
        constants.SEARCH_KEY: search_query,
        constants.MAX_RESULTS_KEY: max_results,
        constants.PART_KEY: part
    }
