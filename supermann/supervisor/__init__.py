"""Supervisor interface for Supermann"""

from __future__ import absolute_import, unicode_literals, print_function

import os
import sys

import supervisor.childutils

import supermann.utils

class EventListener(object):
    """A simple Supervisor event listener"""

    def __init__(self, stdin=sys.stdin, stdout=sys.stdout,
                 reserve_stdin=True, reserve_stdout=True):
        self.log = supermann.utils.getLogger(self)

        # STDIN and STDOUT are referenced by the object, so that they are easy
        # to test, and so the references in sys can be removed (see below)
        self.stdin = stdin
        self.stdout = stdout

        # As stdin/stdout are used to communicate with Supervisor,
        # reserve them by replacing the sys attributes with None
        if reserve_stdin:
            sys.stdin = None
            self.log.debug("Supervisor listener has reserved STDIN")
        if reserve_stdout:
            sys.stdout = None
            self.log.debug("Supervisor listener has reserved STDOUT")

    def parse(self, line):
        """Parses a Supervisor header or payload"""
        return dict([pair.split(':') for pair in line.split()])

    def ready(self):
        """Writes and flushes the READY symbol to stdout"""
        self.stdout.write('READY\n')
        self.stdout.flush()

    def result(self, result):
        """Writes and flushes a result message to stdout"""
        self.stdout.write('RESULT {0}\n{1}'.format(len(result), result))
        self.stdout.flush()

    def ok(self):
        self.result('OK')

    def fail(self):
        self.result('FAIL')

    def wait(self):
        """Waits for an event from Supervisor, then reads and returns it"""
        headers = self.parse(self.stdin.readline())
        payload = self.parse(self.stdin.read(int(headers.pop('len'))))
        self.log.debug("Received %s from supervisor", headers['eventname'])
        return headers, payload

class Supervisor(object):
    def __init__(self):
        self.listener = EventListener()
        self.interface = supervisor.childutils.getRPCInterface(os.environ)

    def run_forever(self):
        while True:
            self.listener.ready()
            yield self.listener.wait()
            self.listener.ok()
