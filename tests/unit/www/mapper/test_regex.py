import unittest

from chula import config
from chula.www.adapters.mod_python import fakerequest
from chula.www.mapper import regex

mapper = (
    # Home controller
    (r'^/$', 'home.index'),
    (r'^/home/?$', 'home.index'),
    (r'^/home/index/?$', 'home.index'),

    # Sample controller
    (r'^/sample/?$', 'sample.index'),
    (r'^/sample/page/?$', 'sample.page'),
)

class Test_regex(unittest.TestCase):
    doctest = regex

    def setUp(self):
        req = fakerequest.FakeRequest()
        cfg = config.Config()
        cfg.classpath = 'package'
        cfg.error_controller = 'error'
        self.mapper = regex.RegexMapper(cfg, req, mapper)

    def test_homepage(self):
        self.mapper.uri = '/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'home')
        self.assertEquals(self.mapper.route.class_name, 'Home')
        self.assertEquals(self.mapper.route.method, 'index')

    def test_regex_match(self):
        self.mapper.uri = '/sample'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'sample')
        self.assertEquals(self.mapper.route.class_name, 'Sample')
        self.assertEquals(self.mapper.route.method, 'index')

    def test_regex_match_with_optional_slash(self):
        self.mapper.uri = '/sample/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'sample')
        self.assertEquals(self.mapper.route.class_name, 'Sample')
        self.assertEquals(self.mapper.route.method, 'index')

    def test_uri_without_any_match(self):
        self.mapper.uri = '/foo/bar/bla/'
        self.mapper.default_route()
        self.mapper.parse()
        self.assertEquals(self.mapper.route.package, 'package')
        self.assertEquals(self.mapper.route.module, 'error')
        self.assertEquals(self.mapper.route.class_name, 'Error')
        self.assertEquals(self.mapper.route.method, 'e404')
