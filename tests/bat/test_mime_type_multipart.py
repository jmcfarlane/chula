# Python imports
from subprocess import Popen, PIPE
import hashlib

# Project imports
from chula.test import bat

HANDLER = '/http/render_form_post'
HTML = 'Hello <a href="home/foo">world</a>'

def shell(cmd):
    output = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    return output.communicate()

class Test_mime_type_multipart(bat.Bat):
    def _post_and_validate_checksum(self, b, a):
        cmd = 'curl -v -F file=@%s %s' % (b, self.url(HANDLER))
        stdout, stderr = shell(cmd)
        open(a, 'w').write(stdout[len('file=='):])
        before = hashlib.sha1(open(b).read()).hexdigest()
        after = hashlib.sha1(open(a).read()).hexdigest()
        self.assertEquals(before, after, stderr)

    def test_text_file(self):
        sample = 'SAMPLE TEXT FILE'
        open('/tmp/test.txt', 'w').write(sample)
        cmd = 'curl -v -F file=@/tmp/test.txt %s' % self.url(HANDLER)
        stdout, stderr = shell(cmd)
        self.assertEquals(stdout, 'file==%s' % sample, stderr)

    def test_text_file_without_extension(self):
        self._post_and_validate_checksum('/etc/services', '/tmp/services')

    def test_binary_file_without_extension(self):
        self._post_and_validate_checksum('/bin/echo', '/tmp/echo')
