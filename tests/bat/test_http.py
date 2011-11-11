from chula.test import bat

HTML = 'Hello <a href="home/foo">world</a>'

class Test_http(bat.Bat):
    def test_get(self):
        retval = self.get('')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)

    def test_get_args_in_form_get(self):
        retval = self.get('/http/render_form?a=b&foo=bar')
        self.assertTrue('a==b' in retval.data, retval.data)
        self.assertTrue('foo==bar' in retval.data, retval.data)
        self.assertEquals(retval.status, 200)

    def test_get_args_in_form(self):
        retval = self.get('/http/render_form_get?a=b&foo=bar')
        self.assertTrue('a==b' in retval.data,  retval.data)
        self.assertTrue('foo==bar' in retval.data, retval.data)
        self.assertEquals(retval.status, 200)

    def test_get_args_multiple(self):
        retval = self.get('/http/render_form_get?a=b&a=c')
        self.assertTrue("a==['b', 'c']" in retval.data,  retval.data)
        self.assertEquals(retval.status, 200)

    def test_post(self):
        retval = self.post('', dict(a='a', b='b'))
        self.assertEquals(retval.data, HTML)

    def test_post_args_in_form_post(self):
        data = dict(a='b', foo='bar')
        retval = self.post('/http/render_form_post', data)
        self.assertTrue('a==b' in retval.data,  retval)
        self.assertTrue('foo==bar' in retval.data, retval.data)
        self.assertEquals(retval.status, 200)

    def test_post_args_in_form(self):
        data = dict(a='b', foo='bar')
        retval = self.post('/http/render_form', data)
        self.assertTrue('a==b' in retval.data,  retval)
        self.assertTrue('foo==bar' in retval.data, retval.data)
        self.assertEquals(retval.status, 200)

    def test_post_and_get_args(self):
        data = dict(a='b', foo='bar')
        retval = self.post('/http/render_form?x=y&car=red', data)
        self.assertTrue('a==b' in retval.data,  retval)
        self.assertTrue('foo==bar' in retval.data, retval.data)
        self.assertTrue('x==y' in retval.data,  retval)
        self.assertTrue('car==red' in retval.data,  retval)
        self.assertEquals(retval.status, 200)

    def test_post_and_get_args_that_overlap(self):
        data = dict(a='A', foo='bar')
        retval = self.post('/http/render_form?a=b', data)
        self.assertTrue('a==A' in retval.data,  retval)
        self.assertTrue('foo==bar' in retval.data, retval.data)
        self.assertEquals(retval.status, 200)

    def test_post_args_isolated_from_get(self):
        data = dict(a='A', foo='bar')
        retval = self.post('/http/render_form_post?a=b', data)
        self.assertTrue('a==A' in retval.data,  retval)
        self.assertTrue('foo==bar' in retval.data, retval.data)
        self.assertEquals(retval.status, 200)

    def test_get_args_isolated_from_post(self):
        data = dict(a='A', foo='bar')
        retval = self.post('/http/render_form_get?a=b', data)
        self.assertTrue('a==b' in retval.data,  retval)
        self.assertTrue('foo==bar' not in retval.data, retval.data)
        self.assertEquals(retval.status, 200)

    def test_put(self):
        retval = self.put('', 'this is plain text')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)
        self.assertEquals(retval.status, 200)

    def test_delete(self):
        retval = self.put('', '<delete>me</delete>')
        self.assertEquals(retval.data, HTML)
        self.assertEquals(retval.status, 200)
        self.assertEquals(retval.status, 200)
