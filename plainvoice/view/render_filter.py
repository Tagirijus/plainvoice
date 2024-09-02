'''
RenderFilter class

This class can extend the given Jinja Environment with filters.
'''

from datetime import datetime, timedelta

from jinja2 import Environment

import calendar


class RenderFilter:
    '''
    Extend Jinja Environmemnt with filters.
    '''

    @staticmethod
    def add_days(date: datetime, days: int) -> datetime:
        '''
        Add days to a given datetime object.

        Args:
            date (datetime): The datetime object.
            days (int): The days to add to the datetime.

        Returns:
            datetime: Returns the new datetime with the added days.
        '''
        return date + timedelta(days=days)

    @staticmethod
    def add_months(date: datetime, months: int) -> datetime:
        '''
        Add months to a given datetime object.

        Args:
            date (datetime): The datetime object.
            months (int): The months to add to the datetime.

        Returns:
            datetime: Returns the new datetime with the added months.
        '''
        month = date.month - 1 + months
        year = date.year + month // 12
        month = month % 12 + 1
        # set day to last day of month, if necessary
        day = min(date.day, calendar.monthrange(year, month)[1])
        return date.replace(year=year, month=month, day=day)

    @staticmethod
    def add_years(date: datetime, years: int) -> datetime:
        '''
        Add years to a given datetime object.

        Args:
            date (datetime): The datetime object.
            years (int): The years to add to the datetime.

        Returns:
            datetime: Returns the new datetime with the added years.
        '''
        try:
            return date.replace(year=date.year + years)
        except ValueError:
            # original date is probably 29th of February (leap year)
            # so set it to the 1st of March
            return date.replace(year=date.year + years, month=3, day=1)

    def extend_jinja_filter(self, env: Environment) -> None:
        '''
        Extend the given Jinja Environment with the filter methods
        of this class.

        Args:
            env (Environmant): The Jinja Environment object.
        '''
        env.filters['add_days'] = self.add_days
        env.filters['add_months'] = self.add_months
        env.filters['add_years'] = self.add_years
