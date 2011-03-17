"""Functions to make working with databases easier"""

import re

from chula import data, error

def cbool(string):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return ``NULL`` so as to insert a NULL value into the database.

    :param string: String to be cleaned
    :type string: :class:`str`
    :rtype: :class:`str` ``TRUE``, ``FALSE``, or ``NULL``

    >>> from chula.db import functions
    >>> print 'SET active = %s;' % functions.cbool(True)
    SET active = TRUE;
    >>>
    >>> print 'SET active = %s;' % functions.cbool(False)
    SET active = FALSE;
    >>>
    >>> print 'SET active = %s;' % functions.cbool(None)
    SET active = NULL;
    """

    if string in [None, '']:
        return 'NULL'

    string = str(string).lower()
    if string in data.TRUE:
        return 'TRUE'

    elif string in data.FALSE:
        return 'FALSE'

    else:
        raise error.TypeConversionError(string, 'sql boolean')

def cdate(string, doquote=True, isfunction=False):
    """
    Returns a formatted string safe for use in SQL. If :class:`None` or an empty
    string is passed, it will return ``NULL`` so as to insert a NULL value
    into the database.

    .. note::

       Todo: This function needs to be able to receive
       datetime.datetime types too.

    :param string: Date to be cleaned
    :type string: :class:`str`
    :rtype: :class:`str`, or ``NULL``

    >>> from chula.db import functions
    >>> print 'SET updated = %s;' % functions.cdate('1/1/2005')
    SET updated = '1/1/2005';

    >>> print 'SET updated = %s;' % functions.cdate('now()', isfunction=True)
    SET updated = now();
    """

    if string in [None, '', 'NULL']:
        return 'NULL'

    elif isfunction:
        return string

    else:
        string = str(string)
        if data.isdate(string):
            if doquote:
                string = data.wrap(string, "'")
        else:
            raise error.TypeConversionError(string, 'sql date')

    return string

def cfloat(flt):
    """
    Returns a formatted string safe for use in SQL. If None is passed, it
    will return ``NULL`` so as to insert a NULL value into the database.

    :param flt: Float to be cleaned
    :type flt: Anything
    :rtype: :class:`float`, or ``NULL``

    >>> from chula.db import functions
    >>> print 'WHERE field = %s;' % functions.cfloat("45")
    WHERE field = 45.0;
    >>>
    >>> print 'WHERE field = %s;' % functions.cfloat(None)
    WHERE field = NULL;
    """

    # Check if the data passed is a NULL value
    if flt is None or str(flt).lower() == 'null' or flt == '':
        return 'NULL'

    elif isinstance(flt, float):
        return flt

    try:
        return float(flt)
    except:
        raise error.TypeConversionError(flt, 'sql float')

def cint(integer):
    """
    Returns a formatted string safe for use in SQL. If :class:`None`
    is passed, it will return ``NULL`` so as to insert a NULL value
    into the database.

    :param integer: Integer to be cleaned
    :type integer: Anything
    :rtype: :class:`int`, or ``NULL``

    >>> from chula.db import functions
    >>> print 'WHERE field = %s;' % functions.cint("45")
    WHERE field = 45;
    """

    # Check if the data passed is a NULL value
    if integer is None or str(integer).lower() == 'null' or integer == '':
        return 'NULL'

    elif isinstance(integer, int):
        return integer

    try:
        return int(integer)
    except:
        raise error.TypeConversionError(integer, 'sql float')

def cregex(string, doquote=True):
    """
    Returns a regular expression safe for use in SQL.  If
    :class:`None` is passed if will raise an exception as None is not
    a valid regular expression.  The intented use is with regex based
    SQL expressions.


    :param string: Value to evaluate
    :type string: :class:`str`
    :param doquote: optionally wrap in single quotes, default is :class:`True`
    :type doquote: :class:`bool`
    :rtype: :class:`str`
    """

    if data.isregex(string):
        if doquote:
            return data.wrap(string, "'")
        else:
            return string
    else:
        raise error.TypeConversionError(string, 'sql regex')

def cstr(string, doquote=True, doescape=True):
    """
    Returns a formatted string safe for use in SQL. If :class:`None`
    is passed, it will return ``NULL`` so as to insert a NULL value
    into the database.  Single quotes will be escaped.

    :param string: String to be cleaned
    :type string: :class:`str`
    :param doquote: Optionally wrap in single quotes, default is :class:`True`
    :type doquote: bool
    :param doescape: Optionally escape single quotes, default is :class:`True`
    :type doescape: :class:`bool`
    :rtype: :class:`str`, or ``NULL``

    >>> from chula.db import functions
    >>> print 'SET description = %s;' % functions.cstr("I don't")
    SET description = 'I don''t';
    >>>
    >>> print 'SET now = %s;' % functions.cstr("CURRENT_TIME", doquote=False)
    SET now = CURRENT_TIME;
    """

    if string is None:
        return 'NULL'

    string = str(string)
    if doescape:
        escape = {"'":"''", "\\":"\\\\"}
        string = data.replace_all(escape, string)

    if doquote:
        return data.wrap(string, "'")
    else:
        return string

def ctags(string):
    """
    Returns a string safe for use in a sql statement

    :param: string
    :type string: Anything
    :rtype: ``NULL``, or :class:`str`

    >>> from chula.db import functions
    >>> print functions.ctags('')
    NULL
    >>> print functions.ctags('linux git foo')
    'foo git linux'
    """

    if string in [None, '']:
        return 'NULL'

    if isinstance(string, list):
        string = ' '.join(string)

    tags = data.tags2str(data.str2tags(string))
    return "'%s'" % tags.lower()

def empty2null(string):
    """
    Returns ``NULL`` if an empty string or :class:`None` is passed,
    else returns the string string.

    :param: string
    :type string: Anything
    :rtype: ``NULL``, or :class:`str`

    >>> from chula.db import functions
    >>> print functions.empty2null('')
    NULL
    """

    if string in [None, '']:
        return 'NULL'
    else:
        return string

def unquote(string):
    """
    Return string not padded with single quotes.  This is useful to
    clean something changed by cstr()

    :param: string
    :type string: :class:`str`
    :rtype: :class:`str`, or input unchanged
    """

    if isinstance(string, str):
        if string.startswith("'") and string.endswith("'"):
            string = string[1:-1]

    return string
