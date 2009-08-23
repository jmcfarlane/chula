"""
Simple utility class to send emails
"""

import smtplib
import socket

from chula import data, regex

class Mail(object):
    def __init__(self, server):
        """
        Set the required attributes
        """

        self.body = None
        self.from_addy = None
        self.reply_to_addy = None
        self.server = server
        self.subject = None
        self.to_addy = None

    def _validate_encoding(self):
        self.body = data.str2unicode(self.body)
        self.from_addy = data.str2unicode(self.from_addy)
        self.reply_to_addy = data.str2unicode(self.reply_to_addy)
        self.server = data.str2unicode(self.server)
        self.subject = data.str2unicode(self.subject)
        self.to_addy = data.str2unicode(self.to_addy)

    def send(self):
        """
        Send the requested mail using smtplib
        """

        if not regex.match(regex.EMAIL, str(self.reply_to_addy)):
            self.reply_to_addy = self.from_addy

        self._validate_encoding()

        headers = []
        headers.append('From: %s' % self.from_addy)
        headers.append('Reply-To: %s' % self.reply_to_addy)
        headers.append('To: %s' % ','.join(self.to_addy.split()))
        headers.append('Subject: %s' % self.subject)
        headers.append('\n')

        try:
            server = smtplib.SMTP(self.server)
            server.set_debuglevel(0)
            server.sendmail(self.from_addy,
                            self.to_addy.split(),
                            '\n'.join(headers) + self.body)
            server.quit()
        except socket.gaierror:
            raise
