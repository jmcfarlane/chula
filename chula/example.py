"""
Example python module for use with illustrating the example unit test(s)
"""

class Example(object):
    def __init__(self):
        """
        Example constructor
        """

        self.name = 'Example attribute'

    def sum(self, a, b):
        """
        Sum two values

        @param a: Value to be summed with b
        @type a: integer
        @param b: Vale to be summed with a
        @type b: integer
        @return: integer
        """

        try:
            return a + b
        except ValueError:
            raise

    def awesome(self):
        """
        Describe the nature of all things related to Gentoo Linux

        @return: boolean

        >>> from chula import example
        >>> gentoo = example.Example()
        >>> if gentoo.awesome():
        ...     print 'Gentoo is awesome!'
        Gentoo is awesome!
        >>> git = example.Example()
        >>> if git.awesome():
        ...     print 'Git is also awesome!'
        Git is also awesome!
        >>> distro = example.Example()
        >>> 'Fedora' is distro.awesome()
        False
        """

        return True

def something():
    return []
