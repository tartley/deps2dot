from unittest import TestCase

from mock import call, Mock, patch

from deps2dot.main import main


class MainTest(TestCase):

    @patch('deps2dot.main.sys.argv', [1, 2, 3])
    @patch('deps2dot.main.get_parser')
    @patch('deps2dot.main.parse_args')
    @patch('deps2dot.main.validate')
    @patch('deps2dot.main.read_deps')
    @patch('deps2dot.main.deps_to_dot')
    @patch('deps2dot.main.print_output')
    @patch('sys.stdout', Mock())
    def test_main(
        self, mock_print, mock_deps_to_dot, mock_read, mock_validate,
        mock_parse_args, mock_get_parser
    ):

        main()

        self.assertEqual(
            mock_get_parser.call_args,
            call('deps2dot')
        )
        self.assertEqual(
            mock_parse_args.call_args,
            call(mock_get_parser.return_value, [2, 3])
        )
        self.assertEqual(
            mock_validate.call_args,
            call(mock_parse_args.return_value)
        )
        self.assertEqual(
            mock_read.call_args,
            call(mock_validate.return_value)
        )
        self.assertEqual(
            mock_deps_to_dot.call_args,
            call(mock_read.return_value)
        )

