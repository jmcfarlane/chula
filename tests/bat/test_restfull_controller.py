# Python imports
import os

# Project imports
from chula.test import bat

class Test_restfull_controller(bat.Bat):
    def test_uri_parsing(self):
        retval = self.request('/blog/jmcfarlane/2010-05-12/comments')

        if 'CHULA_REGEX_MAPPER' in os.environ:
            html = ("blog: "
                    "{'username': 'jmcfarlane', "
                    "'date': '2010-05-12', 'commens': 'comments'}")
            self.assertEquals(retval.data, html)
            self.assertEquals(retval.status, 200)
        else:
            self.assertTrue('404' in retval.data)
            self.assertEquals(retval.status, 404)


