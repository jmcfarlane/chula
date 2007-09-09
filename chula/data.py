"""
Functions to make working with data easier.
"""

import datetime
import time
import re
from types import *
import string
from chula import regex

def chart_scale(num_input):
    """
    Formats a numeric value to a clean rounded number usefull for
    drawing charts.  This can be used to generate the scale by which
    all data points in a graph represent a percentage of.
    
    @param num_input: Data to be rounded to new value
    @type num_input: Int, Long, Float
    @return: Long
    
        >>> print chart_scale(300)
        330.0
    """
    import math
    try:
        num_input = float(num_input)
    except:
        raise ValueError, 'Value passed is not numeric'
    
    return math.ceil((num_input * 1.1) / 10) * 10

def commaify(str_input):
    """
    Formats a string representation of a number so it looks nice.
    This is handy for presentation of currency for example.
    
    @param str_input: Data to have commas added every third place.
    @type str_input: String
    @return: String
    
        >>> print commaify('45000000000')
        45,000,000,000
    """
    
    if not isstr(str_input):
        raise ValueError, 'Value passed is not a string.'
    
    #TODO: learn from and improve this:
    #if num > 1000:  return '%s,%03d' % (commaify(num/1000), num % 1000)
    #else:           return str(num)
    if str_input[0] == '-':
        str_sign = '-'
        str_input = str_input[1:]
    else:
        str_sign = ''
        
    list_input = str_input.split('.')
    str_whole = list_input[0]
    if len(str_whole) > 3:
        #str_whole = commaify(str_whole[:-3]) + ',' + str_whole[:3]
        #str_whole = str_whole[:-3] + ',' + str_whole[-3:]
        str_whole = commaify(str_whole[:-3]) + ',' + str_whole[-3:]
        #str_whole = commaify(str_whole[-3:]) + ',' + str_whole[:3]
    
    if len(list_input) > 1:
        str_input = str_whole + '.' + list_input[1]
        pass
    else:
        str_input = str_whole
        
    return str_sign + str_input

def csv2list(str_input):
    """
    Make it easy to loop over "CSV" files.
    
    @param str_input: Data to be processed
    @type str_input: String
    @return: List of dictionaries
    
        >>> # Simulate the return of open('foo.csv').readlines()[:]
        >>> csv = []
        >>> csv.append('name;age;sex')
        >>> csv.append('Sam;45;Male')
        >>> csv.append('Nancy;27;Female')
        >>> csv.append('Kirby;13;Female')
        >>> csv = '\\n'.join(csv)
        >>> for record in csv2list(csv):
        ...     print record['name'], record['age']
        ...
        Sam 45
        Nancy 27
        Kirby 13

    """
    from operator import itemgetter
    
    # Get a list of the data
    list_input = str_input.split('\n')
    
    # Determine the most likely delimiter
    dict_delim = {'\t':list_input[0].count('\t'),
                  ',':list_input[0].count(','),
                  ';':list_input[0].count(';')}
    delim = sorted(dict_delim.items(), key=itemgetter(1), reverse=True)[0][0]

    # Begin to generate the list of dictionaries
    irow = 0
    list_output = []
    LIST_COLS = []
    for row in list_input:
        list_cols = row.split(delim)
        if irow == 0:
            icol = 0
            for col in list_cols:
                if col is None or col == '':
                    col = 'column-%s' % icol
                LIST_COLS.append(col)
                icol += 1
        else:
            dict_row = {}
            icol = 0
            for col in list_cols:
                try:
                    dict_row[LIST_COLS[icol]] = col
                except IndexError:
                    #print "column[%s] missing head: %s" % (icol, col)
                    pass
                icol += 1
            list_output.append(dict_row)
        irow += 1
    
    return list_output

def date_add(str_unit, int_delta, obj_date):
    """
    Add or subtract from the date passed.
    
    @param str_unit: Unit of measure (B{s}econds/B{m}inutes/B{h}ours/B{d}ays/B{w}eeks).
    @type str_unit: String
    @param int_delta: Offset, amount to adjust the date by.
    @type int_delta: Integer
    @param obj_date: Date to be added/subtracted to/from
    @type obj_date: datetime.datetime
    @return: datetime.datetime object
    
        >>> start = str2datetime('1/1/2005 11:35')
        >>> print date_add('days', -5, start)
        2004-12-27 11:35:00
    
    """
    
    date_initial = obj_date
    if str_unit == 'seconds' or str_unit == 's':
        obj_delta = datetime.timedelta(seconds=int_delta)
    elif str_unit == 'minutes' or str_unit == 'm':
        obj_delta = datetime.timedelta(minutes=int_delta)
    elif str_unit == 'hours' or str_unit == 'h':
        obj_delta = datetime.timedelta(hours=int_delta)
    elif str_unit == 'days' or str_unit == 'd':
        obj_delta = datetime.timedelta(days=int_delta)
    elif str_unit == 'weeks' or str_unit == 'w':
        obj_delta = datetime.timedelta(months=int_delta)
    else:
        return False
        
    return date_initial + obj_delta

def datetime_diff(obj_start, obj_stop, str_unit='seconds'):
    """
    Calculates the difference between two dates.
    
    @param obj_start: Start time
    @type obj_start: datetime.datetime
    @param obj_stop: Stop time
    @type obj_stop: datetime.datetime
    @param str_unit: Unit of measure (B{s}econds/B{m}inutes/B{h}ours/B{d}ays/B{w}eeks).
    @type str_unit: String
    @return: Integer (defaults to seconds, if str_unit not passed)
    
        >>> start = str2datetime('1/1/2005')
        >>> stop = str2datetime('1/5/2005')
        >>> print datetime_diff(start, stop)
        345600.0
        >>> print datetime_diff(start, stop, 'd')
        4.0

    """
    
    if obj_start > obj_stop:
        obj_start, obj_stop = obj_stop, obj_start
        bool_sign = -1
    else:
        bool_sign = 1
    
    obj_diff = obj_stop - obj_start
    days = obj_diff.days
    minutes, seconds = divmod(obj_diff.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    seconds += round((days * 86400) + (hours * 3600) + (minutes * 60))
    minutes += round((days * 1440) + (hours * 60))
    hours += round(days * 24)
    days = round(days)
    weeks = round(days * 7)
    
    if str_unit == 'minutes' or str_unit == 'm':
        return minutes * bool_sign 
    elif str_unit == 'hours' or str_unit == 'h':
        return hours * bool_sign 
    elif str_unit == 'days' or str_unit == 'd':
        return days * bool_sign
    elif str_unit == 'weeks' or str_unit == 'w':
        return weeks * bool_sign
    else:
        return seconds * bool_sign

def datetime_within_range(str_time, int_offset, time_now=False):
    """
    The idea is to provide shorthand for "is foobar time within 02:00 + 30 min".
    This can be usefull for things that look for time periods when different
    logic applies, like from 2am and the next 30 minutes expect the network
    to be slow, as backups are taking place. Anything in the past is considered
    out of range.
    
    @param str_time: Representation of hours:minutes
    @type str_time: String representation of time
    @param int_offset: The size of the range or window
    @type int_offset: Integer
    @param time_now: I{Optional} argument to specify time range/window start.
    @type time_now: datetime.datetime
    @return: Boolean
    
        >>> print datetime_within_range('11:00', 30, str2datetime('1/1/2005 11:25'))
        True
        >>> print datetime_within_range('11:00', 30, str2datetime('1/1/2005 11:35'))
        False
    
    """
    
    arrTime = str_time.split(':')
    if not time_now:
        time_now = datetime.datetime.now()
    
    # Calculate the begin time based on today
    time_begin = datetime.datetime(time_now.year,
                                   time_now.month,
                                   time_now.day,
                                   int(arrTime[0]),
                                   int(arrTime[1])
                                  )
    time_diff = time_now - time_begin
    #print time_begin, time_now, '(' + str(int_offset) + ')', ' -->', time_diff.seconds / 60
    
    # Determine if now() is beyond the begin time (positive number of days)
    if time_diff.days >= 0:
        int_minutes = time_diff.seconds / 60
        if int_minutes <= int_offset:
            return True
        else:
            return False
    else:
        return False

def fmt_phone(str_input):
    """
    Format a string into a properly formatted telephone number.  Accepts a few
    common styles of input.
    
    @param str_input: Telephone number to format
    @type str_input: String
    @return: String formatted as: (area) exchange.number
    
        >>> print fmt_phone('555-123-1234')
        (555) 123.1234
    
    """
    
    if str_input is None or str_input == '':
        return str_input
    else:
        str_input = str(str_input)
        x = len(str_input)
        if x == 12:
            b = '(%s) %s.%s' % (str_input[0:3], 
                                str_input[4:7], 
                                str_input[8:12])
        elif x == 10:
            b = '(%s) %s.%s' % (str_input[0:3], 
                                str_input[3:6], 
                                str_input[6:10])
        elif x == 7:
            b = '%s.%s' % (str_input[0:3], 
                           str_input[3:7])
        else:
            b = str_input #TODO: need to raise error here
        return b

def fmt_money(flt_currency):
    """
    Format U.S. currency (two decimal paces)
    
    @param flt_currency: Currency
    @type flt_currency: Float
    @return: String
    
        >>> print fmt_money(15000)
        15,000.00
    
    
    """
    if not isint(flt_currency, bool_strict=False):
        raise Exception, "Sorry, the value passed cannot be converted to currency"
        return
    if flt_currency == -0:
        flt_currency = 0
    flt_currency = '%.2f' % (flt_currency)
    return commaify(flt_currency)

def isarray(str_input):
    """
    B{NOTE:} This function is depricated and will raise an exception if used.
    Determines if the value passed is an array.  An array is considered one of
    the following:
        1. Tuple
        2. List
        3. Dict
        
    @param str_input: Value to evaluate
    @type str_input: Anything
    @return: True/False
    
    """
    raise StandardError(\
        """This function has been depricated
        Please use the following as appropriate:
            1. istuple()
            2. islist()
            3. isdict()
        """)
    if istuple(str_input) or islist(str_input) or isdict(str_input):
        return True
    else:
        return False

def isboolean(str_input, bool_strict=True):
    """
    Determines if the value passes is a boolean.

    @param str_input: Value to evaluate
    @type str_input: Anything
    @return: True/False

        >>> isboolean(True)
        True
        >>> isboolean('true', bool_strict=False)
        True
    """

    list_strict = [True, False]
    list_loose = [0, 1, 'true', 'false', 'yes', 'no', 'on', 'off']
    
    
    if str_input in list_strict:
        return True
    else:
        if not bool_strict:
            if isstr(str_input): str_input = str_input.lower()
            if str_input in list_loose:
                return True
            else:
                return False
        else:
            return False

def isdate(str_input):
    """
    Determines if the value passed is a date.
            
    @param str_input: Value to evaluate
    @type str_input: Anything
    @return: True/False
    
        >>> print isdate('1/1/2005')
        True
        >>> print isdate('1/41/2005')
        False
    
    """
    try:
        str2datetime(str_input)
        return True
    except ValueError:
        return False

def isdict(str_input):
    """
    Determines if the value passed is a dictionary.
            
    @param str_input: Value to evaluate
    @type str_input: Anything
    @return: True/False
    
        >>> print isdict({'key':'value'})
        True
        >>> print isdict('1/1/2005')
        False
    
    """
    
    a = type(str_input).__name__
    if a == 'dict':
        return True
    else:
        return False
    
def isint(str_input, bool_strict=True):
    """
    Determines if the value passed is an integer.
            
    @param str_input: Value to evaluate
    @type str_input: Anything
    @param bool_strict: Return True if can safely convert to integer
    @type bool_strict: Boolean
    @return: True/False
    
        >>> print isint(1)
        True
        >>> print isint('1')
        False
        >>> print isint('1', bool_strict=False)
        True
    
    """
    
    if type(str_input) == IntType:
        return True
    else:
        if not bool_strict:
            try:
                return isint(int(str_input))
            except:
                return False
        else:
            return False

def islist(str_input):
    """
    Determines if the value passed is a list.
            
    @param str_input: Value to evaluate
    @type str_input: Anything
    @return: True/False
    
        >>> print islist([1, 2])
        True
        >>> print islist('1')
        False
        >>> print islist((1, 2))
        False
    
    """
    
    a = type(str_input).__name__
    if a == 'list':
        return True
    else:
        return False

def istag(str_input):
    """
    Determines if the value passed is a tag.
            
    @param str_input: Value to evaluate
    @type str_input: Anything
    @return: True/False
    
        >>> print istag(('foo'))
        True
        >>> print istag('foo!!')
        False
    
    """
    
    import re
    if isstr(str_input) is False:
        return False
    
    if not re.search(regex.TAG, str_input) is None:
        return True
    else:
        return False

def isstr(str_input, bool_strict=True):
    """
    Determines if the value passed is a string.
            
    @param str_input: Value to evaluate
    @type str_input: Anything
    @param bool_strict: Return True if can safely convert to string
    @type bool_strict: Boolean
    @return: True/False
    
        >>> print isstr('1')
        True
        >>> print isstr(1)
        False
    
    """
    if str_input is None: return False
    
    obj_type = type(str_input)
    if obj_type == StringType:
        return True
    # check for mod_python.util.StringField
    elif obj_type.__name__ == 'StringField':
        return True
    elif obj_type == unicode:
        return True
    else:
        if bool_strict is False:
            try:
                str_input = str(str_input)
                return True
            except:
                pass
            
        return False
   
def istuple(str_input):
    """
    Determines if the value passed is a tuple.
            
    @param str_input: Value to evaluate
    @type str_input: Anything
    @return: True/False
    
        >>> print istuple((1,))
        True
        >>> print istuple([1])
        False
    
    """
    
    a = type(str_input).__name__
    if a == 'tuple':
        return True
    else:
        return False

def list2unique(list_input):
    """
    Returns the list passed, with duplicates removed
    
    @param list_input: List to be evaluated
    @type list_input: List
    @return: List, only containing nique values
    """
    list_unique = {}
    for value in list_input:
        list_unique[value] = 1
        
    list_input = list_unique.keys()
    list_input.sort()
    return list_input
    
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

def replace_all(dict_subs, str_input):
    """
    Simple text replacement, using an input dictionary against a string.
    
    @param dict_subs: Dictionary of find/replace values.
    @type dict_subs: Dictionary
    @param str_input: String to update
    @return: Return string with replacements made per the passed dictionary.
    
        >>> print replace_all({'l':'1', 'o':'0'}, "Hello world")
        He110 w0r1d
    
    """ 
    
    if not str_input is None and str_input != '':
        # Create a regular expression  from the dictionary keys
        regex = re.compile("(%s)" % "|".join(map(re.escape,
                                                 dict_subs.keys())))
        # Recursively for each match, look-up corresponding value in dictionary
        return regex.sub(lambda mo: dict_subs[mo.string[mo.start():mo.end()]],
                         str_input)
    else:
        return str_input

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
            raise ValueError, "Value passed cannot be converted to a date/datetime."
    
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
        datetime_tmp = datetime.datetime(int(t['year']), 
                                         int(t['month']), 
                                         int(t['day']), 
                                         int(t['hour']), 
                                         int(t['minute']), 
                                         int(t['second']))
    else:
        datetime_tmp = datetime.datetime(int(t['year']), 
                                         int(t['month']), 
                                         int(t['day']))
    return datetime_tmp

def str2tags(str_input):
    """
    Convert a string of tags into a sorted list of tags.
    
    @param str_input: String
    @type str_input: String
    @return: List
    
        >>> print str2tags('linux good ms annoying')
        ['annoying', 'good', 'linux', 'ms']
    
    """
    
    import re
    str_error = "Value passed must be alpha numeric only"
    if isstr(str_input) is False:
        raise ValueError, str_error + ': ' + str(str_input)
    else:
        # Replace commas with spaces, and remove extra spaces
        str_input = re.sub(r'[ ,+]+', ' ', str_input)
    
    if str_input == '':
        return []
    
    if not re.search(regex.TAGS, str_input) is None:
        str_input = str_input.lower()
        list_tags = list2unique(str_input.split(' '))
        
        return list_tags
    else:
        raise ValueError, str_error + ': ' + str(str_input)

def str_wrap(str_input, str_wrap_with):
    """
    Wrap a string with something.
    
    @param str_input: String to wrap
    @type str_input: String
    @param str_wrap_with: String to wrap with
    @type str_wrap_with: String
    @return: String wrapped by value passed
    
        >>> print str_wrap('sql', "'")
        'sql'
    
    """
    
    return str_wrap_with + str_input + str_wrap_with

def tags2str(list_input):
    """
    Convert a list of tags into a tsearch2 compliant string. Note that this
    string is not single quote padded for use with an sql insert statement.
    For that, pass the returened value to:  db.clean_tags()
    
    @param list_input: List of valid tags
    @type list_input: List
    @return: List
    
        >>> print tags2str(['annoying', 'good', 'linux', 'ms'])
        annoying good linux ms
    
    """
    if islist(list_input) is False:
        str_error = "The list of tags passed is not a list"
        raise ValueError, str_error + ': ' + str(list_input)
    
    for tag in list_input:
        if istag(tag) is False:
            str_error = "Value is not a tag, according to data.istag()"
            raise ValueError, str_error + ': ' + str(tag)
    
    list_input.sort()
    return ' '.join(list_input)

def txt2js_string(text, replace=string.replace):
    """
    Convert text that includes lines breaks and quotes into a save JavaScript
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
   
def uid(int_len):
    """
    Generate a random string. This function is partially based on current time
    and thus cannot be 100% reliable.
    
    B{Note:} I{int_len must be >= 15}
    
    @param int_len: Length of the desired string
    @type int_len: Integer
    @return: String
    
        >>> if uid(35) != uid(35): print True
        True
    
    """
    
    from random import randrange
    objDate = datetime.datetime.now()
    str_uid = objDate.strftime("%Y%m%d%H%M%S")
    for i in xrange(int_len - len(str_uid)):
        # 65=A 91=Z  97=a 122=z
        str_uid += chr(randrange(65, 91))
    if len(str_uid) <= 14:
        raise Exception, 'Length must be >= 15'
    elif len(str_uid) != int_len:
        print len(str_uid)
        raise TFBug
    return str_uid


    
def zerofront(input, int_length):
    """
    Pad the front of a string to a specified length.
    
    B{Note:} I{This function has been depricated and will throw an exception.
    There is no reason to have this function, as zfill() should be used.}
    
    @param input: String to pad
    @type input: String
    @param int_length: Length of string
    @type int_length: Integer
    @return: String padded to length
    
    """
    raise Exception, 'This function is depricated, rather use:  "a".zfill(x)'
    #return str(input).zfill(int_length)
    
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
