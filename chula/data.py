"""
Functions to make working with data easier.
"""

import datetime
import re
import string
import time

from chula import error, regex

TRUE = ['1', 't', 'true', 'yes', 'y', 'on']
FALSE = ['0', 'f', 'false', 'no', 'n', 'off']

def commaify(input_):
    """
    Generate a number with commas for pretty printing

    @param input_: Data to be commaified
    @type input_: Number or string
    @return: String
    
    >>> print commaify('45000000000')
    45,000,000,000
    """
    
    parts = str(input_).split('.')
    formatted = re.sub(r'(\d{3})', r'\1,', parts[0][::-1])

    # Strip off extra comma on the front (currently end) if it exists
    if formatted.endswith(','):
        formatted = formatted[:-1]

    # Add the decimal back on if it exists
    try:
        output = formatted[::-1] + '.' + parts[1].ljust(2, '0')
    except IndexError:
        output = formatted[::-1]
    except:
        print 'Unable to format number:', input_
        raise

    return output.replace('-,', '-')

def date_add(unit, delta, date):
    """
    Add or subtract from the date passed

    @param unit: Unit of measure (B{S}ec/B{M}in/B{H}r/B{d}ays/B{w}eeks)
    @type unit: String
    @param delta: Offset, amount to adjust the date by
    @type delta: Integer
    @param date: Date to be added/subtracted to/from
    @type date: datetime.datetime
    @return: datetime.datetime
    
    >>> start = str2date('1/1/2005 11:35')
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
        msg = 'Invalid unit, please use: s, m, h, d, or w'
        raise error.UnsupportedUsageError(msg)
        
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
    
    >>> start = str2date('1/1/2005')
    >>> stop = str2date('1/5/2005')
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
    min".  This can be useful for things that look for time periods when
    different logic applies, like from 2am and the next 30 minutes expect
    the network to be slow, as backups are taking place. Anything in the
    past is considered out of range.

    B{Uncertain if this method should stay or be removed}
    
    @param time: Representation of hours:minutes
    @type time: String representation of time
    @param offset: The size of the range or window
    @type offset: Integer
    @param now: I{Optional} argument to specify time range/window start.
    @type now: datetime.datetime
    @return: bool
    
    >>> print date_within_range('11:00', 30, str2date('1/1/2005 11:25'))
    True
    >>> print date_within_range('11:00', 30, str2date('1/1/2005 11:35'))
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

def escape_for_js(input):
    """
    Clean the input for use within javascript

    @param input: String to have illegal js chars escaped
    @type input: str
    @return: str (safe for use in javascript)
    """

    replace = string.replace

    input = replace(input, "'", r"\'")
    input = replace(input, '"', r'\"')
    input = replace(input, "\r\n", ' ')

    return input

def format_phone(input_):
    """
    Format a string into a properly formatted telephone number.  Accepts a
    few common patterns.

    @param input_: Telephone number to format
    @type input_: String
    @return: String formatted as: (area) exchange-number
    
    >>> print format_phone('555-123-1234')
    (555) 123-1234
    """
    
    m = re.match(r'(?P<area>\d{3})?'
                 r'(\D)*'
                 r'(?P<exchange>\d{3})'
                 r'(\D)*'
                 r'(?P<number>\d{4})', input_)

    if not m is None:
        area = m.group('area')
        if not area is None:
            area = '(%s) ' % area
        else:
            area = ''
        phone = '%s-%s' % (m.group('exchange'), m.group('number'))
        return area + phone
    else:
        return input_

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
        raise error.TypeConversionError(amount, 'float', append=msg)

    return commaify('%.2f' % amount)

def isdate(input_):
    """
    Determines if the value passed is a date.

    @param input_: Value to evaluate
    @type input_: Anything
    @return: bool
    
    >>> print isdate('1/1/2005')
    True
    >>> print isdate('1/41/2005')
    False
    """
    try:
        date = str2date(input_)
        if date is None:
            return False
        else:
            return True
    except:
        return False

def isregex(input_):
    """
    Determines if the value passed is a valid regular rexpression

    @param input_: Value to evaluate
    @type input_: str
    @return: bool

    >>> print isregex(r'.*')
    True
    >>> print isregex(r'[')
    False
    """

    try:
        re.compile(input_)
        return True
    except:
        return False


def istag(input_, regexp=None):
    """
    Determines if the value passed is a tag

    @param input_: Value to evaluate
    @type input_: Anything
    @param regexp: Alternate regex to chula.regex.TAG
    @type regexp: Valid regular expression (string)
    @return: bool
    
    >>> print istag('foo')
    True
    >>> print istag('foo!!')
    False
    """
    
    if not isinstance(input_, basestring):
        return False

    if regexp is None:
        regexp = regex.TAG
    
    if re.search(regexp, input_) is None:
        return False
    else:
        return True

def istags(input_, regexp=None):
    """
    Determines if the value passed is a collection of tag.

    @param input_: Value to evaluate
    @type input_: Anything
    @param regexp: Alternate regex to chula.regex.TAGS
    @type regexp: Valid regular expression (string)
    @return: bool
    
    >>> print istags('foo bar')
    True
    >>> print istags('foo, bar')
    True
    >>> print istags('foo!! bar')
    False
    """
    
    if not isinstance(input_, basestring):
        return False

    if regexp is None:
        regexp = regex.TAGS

    if re.search(regexp, input_) is None:
        return False
    else:
        return True

def none2empty(input_):
    """
    Convert none to an empty string.

    @param input_: Value to evaluate
    @type input_: Anything
    @return: Empty string ('') or value passed
    
    >>> print none2empty([1])
    [1]
    >>> if none2empty(None) == '':
    ...     print True
    True
    """
    
    if input_ is None:
        return ''
    else:
        return input_

def replace_all(subs, input_):
    """
    Simple text replacement, using an input_ dictionary against a string.

    @param subs: Dictionary of find/replace values
    @type subs: Dictionary
    @param input_: String to update
    @type input_: String
    @return: String
    
    >>> print replace_all({'l':'1', 'o':'0'}, "Hello world")
    He110 w0r1d
    """ 
    
    if not input_ is None and input_ != '':
        # Generate a regular expression using the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape, subs.keys())))

        # Recursively for each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: subs[mo.string[mo.start():mo.end()]],
                         input_)
    else:
        return input_

def str2bool(input_):
    """
    Determine if the data passed is either True or False

    @param input_: Value to evaluate
    @type input_: String
    @return: bool

    >>> str2bool(True)
    True
    >>> str2bool('on')
    True
    """
    
    if input_ in [True, False]:
        return input_

    input_ = str(input_).lower()
    if input_ in TRUE:
        return True
    elif input_ in FALSE:
        return False
    else:
        raise error.TypeConversionError(input_, 'boolean')

def str2date(input_):
    """
    Conversion from string to datetime object.  Most of the common
    patterns are currently supported.  If None is passed None will be
    returned

    @param input_: Date time (of supported pattern)
    @type input_: String, or None
    @return: datetime.datetime
    
    >>> print str2date("10/4/2005 21:45")
    2005-10-04 21:45:00
    """
    
    if input_ is None:
        return None
    elif not isinstance(input_, basestring):
        msg = 'Value passed must be of type string.'
        raise error.TypeConversionError(input_,
                                                 'datetime.datetime',
                                                 append=msg)

    from time import strptime
    ptime = {'I':'00', 'M':'00', 'S':'00'}
    parts = {'Y':r'(?P<Y>(1|2)\d{3})',
             'm':r'(?P<m>(1[0-2]|0?[1-9]))',
             'd':r'(?P<d>([0-2]?[1-9]|[123][01]))',
             'I':r'(?P<I>([0-5]?[0-9]|60))',
             'M':r'(?P<M>([0-5]?[0-9]|60))',
             'S':r'(?P<S>([0-5]?[0-9]|60))'}

    regs = []
    regs.append('^%(m)s\D%(d)s\D%(Y)s$')
    regs.append('^%(m)s%(d)s%(Y)s$') 
    regs.append('^%(m)s\D%(d)s\D%(Y)s\D%(I)s\D%(M)s$') 
    regs.append('^%(m)s\D%(d)s\D%(Y)s\D%(I)s\D%(M)s\D%(S)s$') 
    regs.append('^%(Y)s\D%(m)s\D%(d)s$') 
    regs.append('^%(Y)s%(m)s%(d)s$') 
    regs.append('^%(Y)s\D%(m)s\D%(d)s\D%(I)s\D%(M)s$') 
    regs.append('^%(Y)s\D%(m)s\D%(d)s\D%(I)s\D%(M)s\D%(S)s$') 

    # 2007-09-25 00:00:00-04:00
    regs.append('^%(Y)s\D%(m)s\D%(d)s\D%(I)s\D%(M)s\D%(S)s[+-]\d{2}:\d{2}$')

    # 2005-10-4 21:01:00.970532-04:00 
    # 2009-04-16 23:16:34.953368+00:00
    exp = r'^%(Y)s\D%(m)s\D%(d)s\D%(I)s\D%(M)s\D%(S)s\.[0-9]+[+-]\d{2}:\d{2}$'
    regs.append(exp)

    for regexp in regs:
        match = re.match(regexp % parts, input_)
        if not match is None:
            ptime.update(match.groupdict())
            break

    if len(ptime.keys()) == 3:
        raise error.TypeConversionError(input_, 'datetime')

    fixed = '%(Y)s-%(m)s-%(d)sT%(I)s:%(M)s:%(S)s' % ptime
    return datetime.datetime(*strptime(fixed, "%Y-%m-%dT%H:%M:%S")[0:6])

def str2tags(input_):
    """
    Convert a string of tags into a sorted list of tags

    @param input_: String
    @type input_: String
    @return: List
    
    >>> print str2tags('linux good ms annoying linux good')
    ['annoying', 'good', 'linux', 'ms']
    """
    
    if istags(input_):
        input_ = input_.lower()
        input_ = input_.replace(',', ' ')
        tags = list(frozenset(input_.split()))
        if '' in tags:
            tags.remove('')
        tags.sort()
        return tags

    elif input_ == '':
        return []
    
    raise error.TypeConversionError(input_, 'list of tags')

def wrap(input_, wrap):
    """
    Wrap a string with something

    @param input_: String to wrap
    @type input_: String
    @param wrap: String to wrap with
    @type wrap: String
    @return: String
    
    >>> print wrap('sql', "'")
    'sql'
    """
    
    return '%s%s%s' % (wrap, input_, wrap)

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

    if not isinstance(tags, list):
        msg = "The list of tags passed is not a list"
        raise ValueError, msg 

    for tag in tags:
        if not istag(tag):
            raise error.TypeConversionError(tag, 'tag')
    
    tags.sort()

    return ' '.join(tags)

