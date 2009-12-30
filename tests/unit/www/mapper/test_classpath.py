import unittest

from chula import config
from chula.www.adapters.mod_python import fakerequest
from chula.www.mapper import classpath

class Test_classpath(unittest.TestCase):
    doctest = classpath

    def setUp(self):
        req = fakerequest.FakeRequest()
        cfg = config.Config()
        cfg.classpath = 'package'
        cfg.error_controller = 'e404'
        self.mapper = classpath.ClassPathMapper(cfg, req)

    def tearDown(self):
        pass
        
    def test_homepage(self):
        self.mapper.uri = '/'
        self.mapper.parse()
        self.assertEquals('package', self.mapper.route.package)
        self.assertEquals('home', self.mapper.route.module)
        self.assertEquals('Home', self.mapper.route.class_name)
        self.assertEquals('index', self.mapper.route.method)

    def test_module_with_named_method(self):
        self.mapper.uri = '/module/method/'
        self.mapper.parse()
        self.assertEquals('package', self.mapper.route.package)
        self.assertEquals('module', self.mapper.route.module)
        self.assertEquals('Module', self.mapper.route.class_name)
        self.assertEquals('method', self.mapper.route.method)

    def test_module_with_implied_method(self):
        self.mapper.uri = '/module/'
        self.mapper.parse()
        self.assertEquals('package', self.mapper.route.package)
        self.assertEquals('module', self.mapper.route.module)
        self.assertEquals('Module', self.mapper.route.class_name)
        self.assertEquals('index', self.mapper.route.method)

    def test_package_with_named_method(self):
        self.mapper.uri = '/pkg/module/method/'
        self.mapper.parse()
        self.assertEquals('package.pkg', self.mapper.route.package)
        self.assertEquals('module', self.mapper.route.module)
        self.assertEquals('Module', self.mapper.route.class_name)
        self.assertEquals('method', self.mapper.route.method)
