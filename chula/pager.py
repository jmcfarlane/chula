"""
Generic paging class designed to aid in drawing next/previous widgets
"""

class Pager(list):
    def __init__(self, offset, recordcount, limit=8, visiblepages=19):
        """
        Create a new pager

        @param offset: 0 based representation of what to offset/skip by
        @type offset: Integer
        @param recordcount: 1 based representation of records available
        @type recordcount: Integer
        @param limit: 1 based representation of records to show per page
        @type limit: Integer
        @param visiblepages: 1 based representation of pages to show at a time
        @type visiblepages: Integer
        @return: List of dictionaries

        >>> from chula import pager
        >>> p = pager.Pager(0, 50)
        >>> p[0]['isselected']
        True
        >>> p[0]['offset']
        0
        >>> p = pager.Pager(30, 100, 5, 11)
        >>> p[0]['isselected']
        False
        >>> p[0]['offset']
        5
        """

        super(Pager, self).__init__()

        if (visiblepages % 2) == 0:
            raise ValueError, 'visiblepages cannot be an even number'

        if recordcount < 1:
            return

        if offset < 0:
            raise ValueError, 'offset must be >= 0'
        elif offset >= recordcount:
            raise ValueError, 'offset must be < recordcount'

        currentpage = offset // limit                   # 0 based
        totalpages = ((recordcount - 1) // limit) + 1   # 1 based
        firstvisible = 0                                # 0 based

        # If current page is more than half of total visiblepages, adjust
        # first page to avoid sliding too far to the right
        if currentpage > visiblepages // 2:
            firstvisible = currentpage - visiblepages // 2

        # Initially set last page to first + visible
        lastvisible = firstvisible + visiblepages  - 1

        # If previous calculation made last page too high, calculate
        # first page by subtracting from the last
        if lastvisible > totalpages - 1:
            lastvisible = totalpages - 1
            firstvisible = totalpages - visiblepages

        if totalpages <= visiblepages:
            firstvisible = 0
            lastvisible = totalpages - 1

        self.currentpage = currentpage

        for page in xrange(firstvisible, lastvisible + 1):
            self.append({'offset':page * limit,
                         'isselected':(page == currentpage),
                         'number':page * limit / limit + 1})

    def render(self):
        return self

