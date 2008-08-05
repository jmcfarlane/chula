"""
Simple utility class to send emails
"""

import smtplib
import socket

from chula import regex

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

    def send(self):
        """
        Send the requested mail using smtplib
        """

        if not regex.match(regex.EMAIL, str(self.reply_to_addy)):
            self.reply_to_addy = self.from_addy

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
