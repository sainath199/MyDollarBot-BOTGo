import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust sys.path to include the directory where 'extract.py' is located
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import extract  # Assuming 'extract.py' is in the 'code' directory
from telebot import types

def create_message(chat_id=12345):
    """Helper function to create a dummy message object"""
    chat = types.Chat(chat_id, 'private')
    from_user = types.User(chat_id, False, 'test_user')
    message = types.Message(
        message_id=1,
        from_user=from_user,
        date=None,
        chat=chat,
        content_type='text',
        options={},
        json_string=""
    )
    return message

class TestExtractModule(unittest.TestCase):

    def setUp(self):
        self.chat_id = 12345
        self.bot = MagicMock()
        self.message = create_message(chat_id=self.chat_id)

    @patch('extract.helper')
    def test_csv_extraction_with_no_data(self, mock_helper):
        """Test the 'run' function when user has no data."""
        # Mock user history data as empty list
        mock_helper.getUserHistory.return_value = []

        # Call the function
        extract.run(self.message, self.bot)

        # Assert that bot.send_message was called with the appropriate message
        self.bot.send_message.assert_called_once_with(
            self.chat_id, "no data to generate csv"
        )

        # Assert that bot.send_document was not called
        self.bot.send_document.assert_not_called()

    @patch('extract.helper')
    @patch('extract.logging')
    def test_run_exception_handling(self, mock_logging, mock_helper):
        """Test exception handling in 'run' function."""
        # Mock getUserHistory to raise an exception
        mock_helper.getUserHistory.side_effect = Exception('Test Exception')

        # Call the function
        extract.run(self.message, self.bot)

        # Assert that logging.error was called
        mock_logging.error.assert_called_once_with('Test Exception')

        # Assert that bot.send_message and bot.send_document were not called
        self.bot.send_message.assert_not_called()
        self.bot.send_document.assert_not_called()

if __name__ == '__main__':
    unittest.main()
