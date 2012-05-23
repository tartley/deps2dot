from unittest import TestCase

from mock import call, patch

from deps2dot.main import main


class MainTest(TestCase):

    @patch('deps2dot.main.sys.argv', [1, 2, 3])
    @patch('deps2dot.main.get_parser')
    @patch('deps2dot.main.parse_args')
    @patch('deps2dot.main.validate')
    @patch('deps2dot.main.generate')
    def test_main(
        self, mock_generate, mock_validate, mock_parse_args, mock_get_parser
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
            mock_generate.call_args,
            call(mock_validate.return_value)
        )

