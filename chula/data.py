"""
Functions to make working with data easier.
"""

import datetime
import time
import re
from types import *
import string
from chula import regex

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
    
    @param unit: Unit of measure (B{s}econds/B{m}inutes/B{h}ours/B{d}ays/B{w}eeks).
    @type unit: String
    @param delta: Offset, amount to adjust the date by.
    @type delta: Integer
    @param date: Date to be added/subtracted to/from
    @type date: datetime.datetime
    @return: datetime.datetime object
    
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

def datetime_diff(start, stop, unit='seconds'):
    """
    Calculates the difference between two dates.
    
    @param start: Start time
    @type start: datetime.datetime
    @param stop: Stop time
    @type stop: datetime.datetime
    @param unit: Unit of measure B{s}econds/B{m}inutes/B{h}ours/B{d}ays/B{w}eeks
    @type unit: String
    @return: Integer (defaults to seconds, if unit not passed)
    
        >>> start = str2datetime('1/1/2005')
        >>> stop = str2datetime('1/5/2005')
        >>> print datetime_diff(start, stop)
        345600.0
        >>> print datetime_diff(start, stop, 'd')
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

def datetime_within_range(time, offset, now=False):
    """
    The idea is to provide shorthand for "is foobar time within 02:00 + 30 min".
    This can be usefull for things that look for time periods when different
    logic applies, like from 2am and the next 30 minutes expect the network
    to be slow, as backups are taking place. Anything in the past is considered
    out of range.
    
    @param time: Representation of hours:minutes
    @type time: String representation of time
    @param offset: The size of the range or window
    @type offset: Integer
    @param now: I{Optional} argument to specify time range/window start.
    @type now: datetime.datetime
    @return: Boolean
    
        >>> print datetime_within_range('11:00', 30, str2datetime('1/1/2005 11:25'))
        True
        >>> print datetime_within_range('11:00', 30, str2datetime('1/1/2005 11:35'))
        False
    
    """
    
    arrTime = time.split(':')
    if not now:
        now = datetime.datetime.now()
    
    # Calculate the begin time based on today
    begin = datetime.datetime(now.year,
                                   now.month,
                                   now.day,
                                   int(arrTime[0]),
                                   int(arrTime[1])
                                  )
    diff = now - begin
    #print begin, now, '(' + str(offset) + ')', ' -->', diff.seconds / 60
    
    # Determine if now() is beyond the begin time (positive number of days)
    if diff.days >= 0:
        minutes = diff.seconds / 60
        if minutes <= offset:
            return True
        else:
            return False
    else:
        return False

def fmt_phone(input):
    """
    Format a string into a properly formatted telephone number.  Accepts a few
    common styles of input.
    
    @param input: Telephone number to format
    @type input: String
    @return: String formatted as: (area) exchange.number
    
        >>> print fmt_phone('555-123-1234')
        (555) 123.1234
    
    """
    
    if input is None or input == '':
        return input
    else:
        input = str(input)
        x = len(input)
        if x == 12:
            b = '(%s) %s.%s' % (input[0:3], 
                                input[4:7], 
                                input[8:12])
        elif x == 10:
            b = '(%s) %s.%s' % (input[0:3], 
                                input[3:6], 
                                input[6:10])
        elif x == 7:
            b = '%s.%s' % (input[0:3], 
                           input[3:7])
        else:
            b = input #TODO: need to raise error here
        return b

def fmt_money(currency):
    """
    Format U.S. currency (two decimal paces)
    
    @param currency: Currency
    @type currency: Float
    @return: String
    
        >>> print fmt_money(15000)
        15,000.00
    
    
    """
    if not isint(currency, isstrict=False):
        raise Exception, "Sorry, the value passed cannot be converted to currency"
        return
    if currency == -0:
        currency = 0
    currency = '%.2f' % (currency)
    return commaify(currency)

def isarray(input):
    """
    B{NOTE:} This function is depricated and will raise an exception if used.
    Determines if the value passed is an array.  An array is considered one of
    the following:
        1. Tuple
        2. List
        3. Dict
        
    @param input: Value to evaluate
    @type input: Anything
    @return: True/False
    
    """
    raise StandardError(\
        """This function has been depricated
        Please use the following as appropriate:
            1. istuple()
            2. islist()
            3. isdict()
        """)
    if istuple(input) or islist(input) or isdict(input):
        return True
    else:
        return False

def isboolean(input, isstrict=True):
    """
    Determines if the value passes is a boolean.

    @param input: Value to evaluate
    @type input: Anything
    @return: True/False

        >>> isboolean(True)
        True
        >>> isboolean('true', isstrict=False)
        True
    """

    strict = [True, False]
    loose = [0, 1, 'true', 'false', 'yes', 'no', 'on', 'off']
    
    
    if input in strict:
        return True
    else:
        if not isstrict:
            if isstr(input): input = input.lower()
            if input in loose:
                return True
            else:
                return False
        else:
            return False

def isdate(input):
    """
    Determines if the value passed is a date.
            
    @param input: Value to evaluate
    @type input: Anything
    @return: True/False
    
        >>> print isdate('1/1/2005')
        True
        >>> print isdate('1/41/2005')
        False
    
    """
    try:
        str2datetime(input)
        return True
    except ValueError:
        return False

def isdict(input):
    """
    Determines if the value passed is a dictionary.
            
    @param input: Value to evaluate
    @type input: Anything
    @return: True/False
    
        >>> print isdict({'key':'value'})
        True
        >>> print isdict('1/1/2005')
        False
    
    """
    
    a = type(input).__name__
    if a == 'dict':
        return True
    else:
        return False
    
def isint(input, isstrict=True):
    """
    Determines if the value passed is an integer.
            
    @param input: Value to evaluate
    @type input: Anything
    @param isstrict: Return True if can safely convert to integer
    @type isstrict: Boolean
    @return: True/False
    
        >>> print isint(1)
        True
        >>> print isint('1')
        False
        >>> print isint('1', isstrict=False)
        True
    
    """
    
    if type(input) == IntType:
        return True
    else:
        if not isstrict:
            try:
                return isint(int(input))
            except:
                return False
        else:
            return False

def islist(input):
    """
    Determines if the value passed is a list.
            
    @param input: Value to evaluate
    @type input: Anything
    @return: True/False
    
        >>> print islist([1, 2])
        True
        >>> print islist('1')
        False
        >>> print islist((1, 2))
        False
    
    """
    
    a = type(input).__name__
    if a == 'list':
        return True
    else:
        return False

def istag(input):
    """
    Determines if the value passed is a tag.
            
    @param input: Value to evaluate
    @type input: Anything
    @return: True/False
    
        >>> print istag(('foo'))
        True
        >>> print istag('foo!!')
        False
    
    """
    
    import re
    if isstr(input) is False:
        return False
    
    if not re.search(regex.TAG, input) is None:
        return True
    else:
        return False

def isstr(input, isstrict=True):
    """
    Determines if the value passed is a string.
            
    @param input: Value to evaluate
    @type input: Anything
    @param isstrict: Return True if can safely convert to string
    @type isstrict: Boolean
    @return: True/False
    
        >>> print isstr('1')
        True
        >>> print isstr(1)
        False
    
    """
    if input is None: return False
    
    otype = type(input)
    if otype == StringType:
        return True
    # check for mod_python.util.StringField
    elif otype.__name__ == 'StringField':
        return True
    elif otype == unicode:
        return True
    else:
        if isstrict is False:
            try:
                input = str(input)
                return True
            except:
                pass
            
        return False
   
def istuple(input):
    """
    Determines if the value passed is a tuple.
            
    @param input: Value to evaluate
    @type input: Anything
    @return: True/False
    
        >>> print istuple((1,))
        True
        >>> print istuple([1])
        False
    
    """
    
    a = type(input).__name__
    if a == 'tuple':
        return True
    else:
        return False

def list2unique(input):
    """
    Returns the list passed, with duplicates removed
    
    @param input: List to be evaluated
    @type input: List
    @return: List, only containing nique values
    """
    unique = {}
    for value in input:
        unique[value] = 1
        
    input = unique.keys()
    input.sort()
    return input
    
def none2empty(input):
    """
    If the value passed is of NoneType, convert it to an empty string.
            
    @param input: Value to evaluate
    @type input: Anything
    @return: "", or the value passed
    
        >>> print none2empty([1])
        [1]
        >>> if none2empty(None) == '': print True
        True
            
    """
    
    if input is None: input = ''
    return input

def replace_all(subs, input):
    """
    Simple text replacement, using an input dictionary against a string.
    
    @param subs: Dictionary of find/replace values.
    @type subs: Dictionary
    @param input: String to update
    @return: Return string with replacements made per the passed dictionary.
    
        >>> print replace_all({'l':'1', 'o':'0'}, "Hello world")
        He110 w0r1d
    
    """ 
    
    if not input is None and input != '':
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape,
                                                 subs.keys())))
        # Recursively for each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: subs[mo.string[mo.start():mo.end()]],
                         input)
    else:
        return input

def str2datetime(x):
    """
    Conversion from string to datetime object.
    
    @param x: Datetime in string format
    @type x: String
    @return: datetime.datetime
    
        >>> print str2datetime("10/4/2005 21:45")
        2005-10-04 21:45:00

    """
    
    #TODO: Woah this function needs some lovin, really!!
    if istuple(x):
        pass
    else:
        if x is None or isint(x) or len(x) < 6:
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
    
        >>> print str2tags('linux good ms annoying')
        ['annoying', 'good', 'linux', 'ms']
    
    """
    
    import re
    error = "Value passed must be alpha numeric only"
    if isstr(input) is False:
        raise ValueError, error + ': ' + str(input)
    else:
        # Replace commas with spaces, and remove extra spaces
        input = re.sub(r'[ ,+]+', ' ', input)
    
    if input == '':
        return []
    
    if not re.search(regex.TAGS, input) is None:
        input = input.lower()
        tags = list2unique(input.split(' '))
        
        return tags
    else:
        raise ValueError, error + ': ' + str(input)

def wrap(input, wrap):
    """
    Wrap a string with something.
    
    @param input: String to wrap
    @type input: String
    @param wrap: String to wrap with
    @type wrap: String
    @return: String wrapped by value passed
    
        >>> print wrap('sql', "'")
        'sql'
    
    """
    
    return wrap + input + wrap

def tags2str(input):
    """
    Convert a list of tags into a tsearch2 compliant string. Note that this
    string is not single quote padded for use with an sql insert statement.
    For that, pass the returened value to:  db.ctags()
    
    @param input: List of valid tags
    @type input: List
    @return: List
    
        >>> print tags2str(['annoying', 'good', 'linux', 'ms'])
        annoying good linux ms
    
    """

    if islist(input) is False:
        error = "The list of tags passed is not a list"
        raise ValueError, error + ': ' + str(input)
    
    for tag in input:
        if istag(tag) is False:
            error = "Value is not a tag, according to data.istag()"
            raise ValueError, error + ': ' + str(tag)
    
    input.sort()
    return ' '.join(input)

def txt2js_string(text, replace=string.replace):
    """
    Convert text that includes lines breaks and quotes into a safe JavaScript
    string. I{Uses string.replace to be fast as possible}
    
    @param text: Text to be converted
    @type: text: String
    @return: String
    """

    #TODO: unit test and docstring test this
    text = replace(text, "'", r"\'")
    text = replace(text, '"', r'\"')
    text = replace(text, "\r\n", ' ')
    return text
