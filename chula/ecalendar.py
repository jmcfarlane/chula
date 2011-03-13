"""
Simple module to aid in working with calendars
"""

import calendar
import datetime

class Calendar(list):
    """
    Calendar object consisting of a list of :class:`datetime.datetime`
    objects.

    >>> from chula import ecalendar
    >>>
    >>> # Calendar for this month
    >>> c = ecalendar.Calendar()
    >>>
    >>> # Calendar for a specific year/month
    >>> c = ecalendar.Calendar(year=2010, month=2)
    >>>
    >>> # Print out the last two weeks of the month
    >>> for i, week in list(enumerate(c))[-2:]:
    ...     print 'Week', i + 1
    ...     for day in week:
    ...         print day.strftime('%Y/%m/%d')
    Week 3
    2010/02/15
    2010/02/16
    2010/02/17
    2010/02/18
    2010/02/19
    2010/02/20
    2010/02/21
    Week 4
    2010/02/22
    2010/02/23
    2010/02/24
    2010/02/25
    2010/02/26
    2010/02/27
    2010/02/28
    """

    def __init__(self, year=None, month=None):
        """
        Creates a calendar.

        :param year: Calendar year
        :type year: :class:`int`
        :param month: Calendar month
        :type month: :class:`int`
        :rtype: :class:`list`
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
