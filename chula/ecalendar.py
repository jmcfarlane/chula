"""
Simple module to aid in working with calendars
"""

import calendar
import datetime

class Calendar(list):
    def __init__(self, year=None, month=None):
        """
        Creates calendar
        @param year: Calendar year
        @type year: int
        @param month: Calendar month
        @type month: int
        @return: list
        """
        
        w = 0
        cal = []
        if year is None or month is None:
            today = datetime.datetime.now()
            year = today.year
            month = today.month

        weeks = calendar.monthcalendar(year, month)
        for week in weeks:
            self.append([])
            for day in week:
                if day > 0:
                    day = datetime.datetime(year, month, day).date()
                    self[w].append(day)
                else:
                    self[w].append(None)

            w += 1

