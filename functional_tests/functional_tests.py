from os import remove
from subprocess import Popen, PIPE
from unittest import TestCase


def unescape(bytestream):
    return str(bytestream).replace('\\n', '\n')


class FunctionalTest(TestCase):

    def assert_process_succeeds(self, cmdline):
        process = Popen(
            cmdline,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, stderr = process.communicate()
        self.assertEqual(process.returncode, 0, unescape(stderr))
        self.assertEqual(stderr, b'')
        return stdout


    def test_output_should_be_accepted_by_dot(self):
        self.assert_process_succeeds(
            'deps2dot functional_tests/test_data/esperanto.deps >test.dot',
        )
        self.assert_process_succeeds(
            'dot -Tsvg test.dot >test.svg',
        )
        remove('test.dot')
        remove('test.svg')

