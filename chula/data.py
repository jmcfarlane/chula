"""
Functions to make working with data easier.
"""

import datetime
import time
import re
from types import *
import string
from chula import chulaException, regex

def commaify(input):
    """
    Generate a number with commas for pretty printing
    
    @param input: Data to be commaified
    @type input: Number or string
    @return: String
    
    >>> print commaify('45000000000')
    45,000,000,000
    """
    
    parts = str(input).split('.')
    formatted = re.sub(r'(\d{3})', r'\1,', parts[0][::-1])
    try:
        output = formatted[::-1] + '.' + parts[1]
    except:
        output = formatted[::-1]

    return output.replace('-,', '-')

def date_add(unit, delta, date):
    """
    Add or subtract from the date passed.
    
    @param unit: Unit of measure (B{S}ec/B{M}in/B{H}r/B{d}ays/B{w}eeks)
    @type unit: String
    @param delta: Offset, amount to adjust the date by
    @type delta: Integer
    @param date: Date to be added/subtracted to/from
    @type date: datetime.datetime
    @return: datetime.datetime
    
    >>> start = str2datetime('1/1/2005 11:35')
    >>> print date_add('days', -5, start)
    2004-12-27 11:35:00
    """
    
    initial = date
    if unit == 'seconds' or unit == 's':
        delta = datetime.timedelta(seconds=delta)
    elif unit == 'minutes' or unit == 'm':
        delta = datetime.timedelta(minutes=delta)
    elif unit == 'hours' or unit == 'h':
        delta = datetime.timedelta(hours=delta)
    elif unit == 'days' or unit == 'd':
        delta = datetime.timedelta(days=delta)
    elif unit == 'weeks' or unit == 'w':
        delta = datetime.timedelta(months=delta)
    else:
        return False
        
    return initial + delta

def date_diff(start, stop, unit='seconds'):
    """
    Calculates the difference between two dates.
    
    @param start: Start time
    @type start: datetime.datetime
    @param stop: Stop time
    @type stop: datetime.datetime
    @param unit: Unit of measure (B{S}ec/B{M}in/B{H}r/B{d}ays/B{w}eeks)
    @type unit: String
    @return: Integer (defaults to seconds, if unit not passed)
    
    >>> start = str2datetime('1/1/2005')
    >>> stop = str2datetime('1/5/2005')
    >>> print date_diff(start, stop)
    345600.0
    >>> print date_diff(start, stop, 'd')
    4.0
    """
    
    if start > stop:
        start, stop = stop, start
        issign = -1
    else:
        issign = 1
    
    diff = stop - start
    days = diff.days
    minutes, seconds = divmod(diff.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    seconds += round((days * 86400) + (hours * 3600) + (minutes * 60))
    minutes += round((days * 1440) + (hours * 60))
    hours += round(days * 24)
    days = round(days)
    weeks = round(days * 7)
    
    if unit == 'minutes' or unit == 'm':
        return minutes * issign 
    elif unit == 'hours' or unit == 'h':
        return hours * issign 
    elif unit == 'days' or unit == 'd':
        return days * issign
    elif unit == 'weeks' or unit == 'w':
        return weeks * issign
    else:
        return seconds * issign

def date_within_range(time, offset, now=None):
    """
    The idea is to provide shorthand for "is foobar time within 02:00 + 30
    min".  This can be usefull for things that look for time periods when
    different logic applies, like from 2am and the next 30 minutes expect
    the network to be slow, as backups are taking place. Anything in the
    past is considered out of range.
    
    @param time: Representation of hours:minutes
    @type time: String representation of time
    @param offset: The size of the range or window
    @type offset: Integer
    @param now: I{Optional} argument to specify time range/window start.
    @type now: datetime.datetime
    @return: Boolean
    
    >>> print date_within_range('11:00', 30, str2datetime('1/1/2005 11:25'))
    True
    >>> print date_within_range('11:00', 30, str2datetime('1/1/2005 11:35'))
    False
    """
    
    range = time.split(':')
    if now is None:
        now = datetime.datetime.now()
    
    # Calculate the begin time based on today
    begin = datetime.datetime(now.year,
                              now.month,
                              now.day,
                              int(range[0]),
                              int(range[1]))
    diff = now - begin
    
    # Determine if now() is beyond the begin time (positive number of days)
    if diff.days >= 0:
        minutes = diff.seconds / 60
        if minutes <= offset:
            return True
        else:
            return False
    else:
        return False

def format_phone(input):
    """
    Format a string into a properly formatted telephone number.  Accepts a
    few common styles of input.
    
    @param input: Telephone number to format
    @type input: String
    @return: String formatted as: (area) exchange-number
    
    >>> print format_phone('555-123-1234')
    (555) 123-1234
    """
    
    m = re.match(r'(?P<area>\d{3})?'
                 r'(\D)*'
                 r'(?P<exchange>\d{3})'
                 r'(\D)*'
                 r'(?P<number>\d{4})', input)

    if not m is None:
        area = m.group('area')
        if not area is None:
            area = '(%s) ' % area
        else:
            area = ''
        phone = '%s-%s' % (m.group('exchange'), m.group('number'))
        return area + phone
    else:
        return input

def format_money(amount):
    """
    Format a numeric value into commaified dollars and cents (two digits)
    
    @param amount: Money to be converted
    @type currency: Float
    @return: String
    
    >>> print format_money(15000)
    15,000.00
    >>> print format_money(15000.100030)
    15,000.10
    """

    try:
        amount = float(amount)
    except Exception:
        msg = 'The money passed must be castable as float'
        raise chulaException.TypeConversionError(amount, 'float', append=msg)

    return commaify('%.2f' % (amount))

def isdate(input):
    """
    Determines if the value passed is a date.
            
    @param input: Value to evaluate
    @type input: Anything
    @return: Boolean
    
    >>> print isdate('1/1/2005')
    True
    >>> print isdate('1/41/2005')
    False
    """
    try:
        str2datetime(input)
        return True
    except:
        return False

def istag(input, regexp=None):
    """
    Determines if the value passed is a tag.
            
    @param input: Value to evaluate
    @type input: Anything
    @param regexp: Alternate regex to chula.regex.TAG
    @type regexp: Valid regular expression (string)
    @return: Boolean
    
    >>> print istag('foo')
    True
    >>> print istag('foo!!')
    False
    """
    
    if isinstance(input, str) is False:
        return False

    if regexp is None:
        regexp = regex.TAG
    
    if re.search(regexp, input) is None:
        return False
    else:
        return True

def istags(input, regexp=None):
    """
    Determines if the value passed is a collection of tag.
            
    @param input: Value to evaluate
    @type input: Anything
    @param regexp: Alternate regex to chula.regex.TAGS
    @type regexp: Valid regular expression (string)
    @return: Boolean
    
    >>> print istags('foo bar')
    True
    >>> print istags('foo, bar')
    True
    >>> print istags('foo!! bar')
    False
    """
    
    if isinstance(input, str) is False:
        return False

    if regexp is None:
        regexp = regex.TAGS

    if re.search(regexp, input) is None:
        return False
    else:
        return True

def none2empty(input):
    """
    Convert none to an empty string.
            
    @param input: Value to evaluate
    @type input: Anything
    @return: Empty string ('') or value passed
    
    >>> print none2empty([1])
    [1]
    >>> if none2empty(None) == '':
    ...     print True
    True
    """
    
    if input is None:
        return ''
    else:
        return input

def replace_all(subs, input):
    """
    Simple text replacement, using an input dictionary against a string.
    
    @param subs: Dictionary of find/replace values
    @type subs: Dictionary
    @param input: String to update
    @type input: String
    @return: String
    
    >>> print replace_all({'l':'1', 'o':'0'}, "Hello world")
    He110 w0r1d
    """ 
    
    if not input is None and input != '':
        # Generate a regular expression using the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, subs.keys())))

        # Recursively for each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: subs[mo.string[mo.start():mo.end()]],
                         input)
    else:
        return input

def str2bool(input):
    """
    Determine if the string passed is either True or False

    @param input: Value to evaluate
    @type input: Anything
    @return: Boolean

    >>> str2bool(True)
    True
    >>> str2bool('on')
    True
    """

    true = ['1', 'true', 'yes', 'y', 'on']
    false = ['0', 'false', 'no', 'n', 'off']
    
    if input in [True, False]:
        return input

    input = str(input).lower()
    if input in true:
        return True
    elif input in false:
        return False
    else:
        raise chulaException.TypeConversionError(input, 'boolean')

def str2datetime(x):
    """
    Conversion from string to datetime object.
    
    @param x: Datetime in string format
    @type x: String
    @return: datetime.datetime
    
        >>> print str2datetime("10/4/2005 21:45")
        2005-10-04 21:45:00

    """
    
    if isinstance(x, tuple):
        pass
    else:
        if x is None or isinstance(x, int) or len(x) < 6:
            msg = "Value passed cannot be converted to a date/datetime."
            raise ValueError, msg

        t = {}
        x = x.replace('-', '/')

        if x.find(' ') > 0:
            try:
                time = x.split(' ')[1].split(':')
                if len(time) >= 2:
                    t['hour'] = time[0]
                    t['minute'] = time[1]
                if len(time) >= 3:
                    t['second'] = time[2]
                    if t['second'].find('.') > 0:
                        t['second'] = t['second'].split('.')[0]
                else:
                    t['second'] = 0
                
                x = x.split(' ')[0]
            except:
                raise ValueError, "Value passed is not formatted properly."

        try:
            x = x.split('/')
            x.extend(time)
        except:
            pass

        try:
            # Support for yyyymmdd
            if len(x[0]) == 8:
                t['year'] = x[0][0:4]
                t['month'] = x[0][4:6]
                t['day'] = x[0][6:8]
            elif len(x[0]) == 4:
                t['year'] = x[0]
                t['month'] = x[1]
                t['day'] = x[2]
            else:
                t['year'] = x[2]
                t['month'] = x[0]
                t['day'] = x[1]
                
        except:
            raise ValueError, "Value passed is not formatted properly."

    if len(t) == 6:
        date = datetime.datetime(int(t['year']), 
                                 int(t['month']), 
                                 int(t['day']), 
                                 int(t['hour']), 
                                 int(t['minute']), 
                                 int(t['second']))
    else:
        date = datetime.datetime(int(t['year']), 
                                 int(t['month']), 
                                 int(t['day']))
    return date

def str2tags(input):
    """
    Convert a string of tags into a sorted list of tags.
    
    @param input: String
    @type input: String
    @return: List
    
    >>> print str2tags('linux good ms annoying linux good')
    ['annoying', 'good', 'linux', 'ms']
    """
    
    if istags(input) is True:
        input = input.lower()
        input = input.replace(',', ' ')
        tags = list(frozenset(input.split()))
        if '' in tags:
            tags.remove('')
        tags.sort()
        return tags

    elif input == '':
        return []
    
    raise chulaException.TypeConversionError(input, 'list of tags')

def wrap(input, wrap):
    """
    Wrap a string with something.
    
    @param input: String to wrap
    @type input: String
    @param wrap: String to wrap with
    @type wrap: String
    @return: String
    
    >>> print wrap('sql', "'")
    'sql'
    """
    
    return '%s%s%s' % (wrap, input, wrap)

def tags2str(tags):
    """
    Convert a list of tags into a tsearch2 compliant string. Note that this
    string is not single quote padded for use with an sql insert statement.
    For that, pass the returened value to:  db.ctags()
    
    @param tags: List of valid tags
    @type tags: List
    @return: List
    
    >>> print tags2str(['annoying', 'good', 'linux', 'ms'])
    annoying good linux ms
    """

    if isinstance(tags, list) is False:
        msg = "The list of tags passed is not a list"
        raise ValueError, msg 

    for tag in tags:
        if istag(tag) is False:
            raise chulaException.TypeConversionError(tag, 'tag')
    
    tags.sort()

    return ' '.join(tags)
