from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        # Mock __getitem__ connection handler function to return always true
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True

            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # we can also use a patch decorator to mock time.sleep
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
