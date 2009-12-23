"""Module for working with unit tests"""

import doctest
import imp
import os
import re
import sys
import unittest

RE_TEST_MODULE = re.compile(r'.*test_[a-zA-Z]+[-a-zA-Z0-9_]+\.py$')
RE_TEST_CLASS = re.compile(r'Test_[a-zA-Z_]+')
DOCTEST = 'doctest'

class TestFinder(set):
    """
    Class to find and run unit tests.  When looking for tests it uses
    the following regular expressions to match modules with the
    pattern I{Test_class} and it will load doctests if
    I{Test_class.doctest} exists and is set to a module.

    Example usage:

    >>> from chula import testutils
    >>> tests = testutils.TestFinder('/path/to/project')
    >>> tests.run()
    """

    def __init__(self, location):
        """
        @param location: A filesystem path, or collection of paths
        @type location: str, list, or tuple
        @return: set
        """

        super(TestFinder, self).__init__()
        self.search(location)
        self.build_suite()

    def search(self, location):
        """
        Search the passed path(s) and fill the set with the path to
        each test module.

        @param location: A filesystem path, or collection of paths
        @type location: str, list, or tuple
        @return: None
        """

        if isinstance(location, (list, tuple)):
            for node in location:
                self.search_node(node)
        else:
            self.search_node(location)

    def search_node(self, node):
        """
        Process a file or directory and import tests

        @param node: A filesystem directory or file
        @type node: str
        @return: None
        """

        if os.path.exists(node):
            if os.path.isdir(node):
                self.search_directory(node)
            else:
                self.add_file(node)

    def search_directory(self, directory):
        """
        Import all of the tests in a directory

        @param directory: A directory on the filesystem
        @type directory: str
        @return: None
        """

        for root, dirs, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                self.add_file(path)

    def add_file(self, file):
        """
        Add a file to the unique list (set) of files that contain
        tests.

        @param file: A file on the filesystem
        @type file: str
        @return: None
        """

        if not RE_TEST_MODULE.match(file) is None:
            self.add(file)

    def build_suite(self):
        """
        Combine all the tests into a single unittest suite
        """

        cwd = os.getcwd()
        self.suite = unittest.TestSuite()
        sys.path.insert(0, None)
        for test in self:
            dir_name = os.path.dirname(test)
            module_name = os.path.basename(test)[:-3]

            # Add the module to the front of the python path
            sys.path[0] = dir_name

            # Generate a fully unique [module] name, but try to avoid
            # including duplicate long strings on the front.  For
            # example, we don't want: # _home_username_path_to_repo_tests
            if dir_name.startswith(cwd):
                dir_name = dir_name.rsplit(cwd)[1]

            # Don't start with a slash either
            if dir_name.startswith(os.sep):
                dir_name = dir_name[1:]

            # Finally generate the uniq [module] name
            u_name = os.path.join(dir_name, module_name).replace(os.sep, '_')

            try:
                # Import the module using imp rather than __import__
                # as imp allows us to specify the name of the module.
                # This allows us to have tests with the same name in
                # different directories - and avoid namespace clashes.
                f, filename, descr = imp.find_module(module_name)
                module = imp.load_module(u_name, f, filename, descr)
            except ImportError, ex:
                print 'Unable to import', test
                raise

            for tests in self.extract_tests(module):
                self.suite.addTests(tests)
                
        sys.path.pop(0)

    def extract_tests(self, module):
        """
        Import all of the tests in a file by looking for classes that
        match a Test_abc pattern.  If the test class has a I{doctest}
        attribute that holds a module, the corresponding doctests wil
        be added as well.

        @param module: Module containing unit tests
        @type module: module
        @return: iterator
        """

        for obj in dir(module):
            if not RE_TEST_CLASS.match(obj) is None:
                # Load the class as a test suite
                unbound_class = getattr(module, obj)
                tests = unittest.makeSuite(unbound_class)

                # Add doctest testing if the test suite supports it
                doctests = getattr(unbound_class, DOCTEST, None)
                if not doctests is None:
                    tests.addTest(doctest.DocTestSuite(doctests))

                yield tests

    def run(self, verbosity=2):
        """
        Run the unit tests found, with a default verbosity of 2.
        """
        
        return unittest.TextTestRunner(verbosity=verbosity).run(self.suite)
