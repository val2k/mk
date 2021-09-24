import re

from datetime import date, datetime, timedelta
from .constants import YEAR_AND_MONTH_REGEX

def get_prev_month_from_cur_date() -> str:
    prev = date.today().replace(day=1) - timedelta(days=1)
    return '{:02}'.format(prev.month)

def check_year_and_month(year_and_month: str) -> str:
    current_year = datetime.now().year
    current_month = datetime.now().month

    if not year_and_month:
        prev_month = get_prev_month_from_cur_date()
        return "{}/{}".format(current_year, prev_month)

    check_regex = re.compile(YEAR_AND_MONTH_REGEX)
    if not check_regex.match(year_and_month):
        raise ValueError("'{}' format must be YYYY-mm.".format(year_and_month))

    year, month = year_and_month.split('/')

    if int(year) > current_year or int(month) >= current_month:
        raise ValueError(
            """
            Given year is in the future must not be in the future.
            Given month must be inferior of the current month.
            """
        )
    
    return year_and_month
