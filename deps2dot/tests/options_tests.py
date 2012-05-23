from unittest import TestCase

from mock import Mock, patch

from deps2dot import __version__
from deps2dot.options import get_parser, validate


class OptionsTest(TestCase):

    @patch('sys.stderr')
    def assert_get_parser_error(self, args, expected, mock_stderr):
        parser = get_parser('prog')
        with self.assertRaises(SystemExit):
            parser.parse_args(args)
        self.assertIn(expected, mock_stderr.write.call_args[0][0])


    def test_get_parser_version(self):
        self.assert_get_parser_error(['--version'], 'v%s' % (__version__,))

    def test_get_parser_filename(self):
        parser = get_parser('prog')
        options = parser.parse_args(['filename'])

        self.assertEqual(options.input, 'filename')


    def test_validate(self):
        options = Mock()
        options.command = [0]
        response = validate(options)
        self.assertIs(response, options)

