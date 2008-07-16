"""Functions to make working with databases easier"""

import re

from chula import data, error

def cbool(input_):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.

    @param input_: String to be cleaned
    @type input_: String
    @return: String I{TRUE/FALSE}, or 'NULL'
    
    >>> print 'SET active = %s;' % cbool(True)
    SET active = TRUE;
    """
    
    if input_ in [None, '']:
        return 'NULL'
    
    input_ = str(input_).lower()
    if input_ in data.TRUE:
        return 'TRUE'

    elif input_ in data.FALSE:
        return 'FALSE'

    else:
        raise error.TypeConversionError(input_, 'sql boolean')

def cdate(input_, doquote=True, isfunction=False):
    """
    Returns a formatted string safe for use in SQL. If None or an empty
    string is passed, it will return 'NULL' so as to insert a NULL value
    into the database.
    
    B{Todo:}
    I{This function needs to be able to receive datetime.datetime types too.}
    
    @param input_: Date to be cleaned
    @type input_: String
    @return: String, or 'NULL'
    
    >>> print 'SET updated = %s;' % cdate('1/1/2005')
    SET updated = '1/1/2005';
    
    >>> print 'SET updated = %s;' % cdate('now()', isfunction=True)
    SET updated = now();
    """
    
    if input_ in [None, '', 'NULL']:
        return 'NULL'

    elif isfunction:
        return input_

    else:
        input_ = str(input_)
        if data.isdate(input_):
            if doquote:
                input_ = data.wrap(input_, "'")
        else:
            raise error.TypeConversionError(input_, 'sql date')

    return input_

def cfloat(input_):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    
    @param input_: Float to be cleaned
    @type input_: Anything
    @return: Float, or 'NULL'
    
    >>> print 'WHERE field = %s;' % cfloat("45")
    WHERE field = 45.0;
    """
    
    # Check if the data passed is a NULL value
    if input_ is None or str(input_).lower() == 'null' or input_ == '':
        return 'NULL'

    elif isinstance(input_, float):
        return input_

    try:
        return float(input_)
    except:
        raise error.TypeConversionError(input_, 'sql float')

def cint(input_):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    
    @param input_: Integer to be cleaned
    @type input_: Anything
    @return: Integer, or 'NULL'
    
    >>> print 'WHERE field = %s;' % cint("45")
    WHERE field = 45;
    """
    
    # Check if the data passed is a NULL value
    if input_ is None or str(input_).lower() == 'null' or input_ == '':
        return 'NULL'

    elif isinstance(input_, int):
        return input_

    try:
        return int(input_)
    except:
        raise error.TypeConversionError(input_, 'sql float')

def cregex(input_, doquote=True):
    """
    Returns a regular expression safe for use in SQL.  If None is
    passed if will raise an exception as None is not a valid regular
    expression.  The intented use is with regex based SQL expressions.


    @param input_: Value to evaluate
    @type input_: str
    @param doquote: I{OPTIONAL}: Wrapped in single quotes, defaults to B{True}
    @type doquote: bool
    @return: str
    """

    if data.isregex(input_):
        if doquote:
            return data.wrap(input_, "'")
        else:
            return input_
    else:
        raise error.TypeConversionError(input_, 'sql regex')

def cstr(input_, doquote=True, doescape=True):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return 'NULL' so as to insert a NULL value into the database.
    Single quotes will be escaped.
    
    @param input_: String to be cleaned
    @type input_: String
    @param doquote: I{OPTIONAL}: Wrapped in single quotes, defaults to B{True}
    @type doquote: bool
    @param doescape: I{OPTIONAL}: Escape single quotes, defaults to B{True}
    @type doescape: bool
    @return: String, or 'NULL'
    
    >>> print 'SET description = %s;' % cstr("I don't")
    SET description = 'I don''t';
    >>> print 'SET now = %s;' % cstr("CURRENT_TIME", doquote=False)
    SET now = CURRENT_TIME;
    """
    
    if input_ is None:
        return 'NULL'
    
    input_ = str(input_) 
    if doescape:
        escape = {"'":"''", "\\":"\\\\"}
        input_ = data.replace_all(escape, input_)

    if doquote:
        return data.wrap(input_, "'")
    else:
        return input_

def ctags(input_):
    """
    Returns a string safe for use in a sql statement

    @param: input_
    @type input_: Anything
    @return: 'NULL', or input_ string
    
    >>> print ctags('')
    NULL
    >>> print ctags('linux git foo')
    'foo git linux'
    """

    if input_ in [None, '']:
        return 'NULL'
    
    if isinstance(input_, list):
        input_ = ' '.join(input_)

    tags = data.tags2str(data.str2tags(input_))
    return "'%s'" % tags.lower()

def empty2null(input_):
    """
    Returns NULL if an empty string or None is passed, else returns the
    input_ string.

    @param: input_
    @type input_: Anything
    @return: 'NULL', or input_ string
    
    >>> print empty2null('')
    NULL
    """

    if input_ in [None, '']:
        return 'NULL'
    else:
        return input_

def unquote(input_):
    """
    Return string not padded with single quotes.  This is useful to
    clean something changed by cstr()

    @param: input_
    @type input_: str
    @return: str, or input unchanged
    """

    if isinstance(input_, str):
        if input_.startswith("'") and input_.endswith("'"):
            input_ = input_[1:-1]

    return input_
