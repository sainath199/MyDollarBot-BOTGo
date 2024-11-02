import unittest
from unittest.mock import patch, MagicMock
import os

class TestEmailFunctions(unittest.TestCase):

    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        # Set up mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the function
        send_email('testuser@example.com', 'Test Subject', 'Test Message', 'test_attachment.txt')

        # Assertions
        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('dollarbot123@gmail.com', 'tsvueizeuvzivtjo')
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

    @patch('os.path.isfile')
    @patch('extract.run')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="test data")
    @patch('smtplib.SMTP')
    def test_process_email_input_with_existing_file(self, mock_smtp, mock_open, mock_extract_run, mock_isfile):
        # Mock file check to return True
        mock_isfile.return_value = True

        # Mock bot and message
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123
        message.text = 'testuser@example.com'

        # Call the function
        process_email_input(message, bot)

        # Assertions
        mock_smtp.assert_called()
        mock_open.assert_called_with('code/data.csv', 'rb')
        bot.send_message.assert_called_with(123, 'Email sent successfully!')

    @patch('os.path.isfile')
    @patch('extract.run')
    @patch('smtplib.SMTP')
    def test_process_email_input_without_existing_file(self, mock_smtp, mock_extract_run, mock_isfile):
        # Mock file check to return False
        mock_isfile.return_value = False
        mock_extract_run.return_value = 'code/data.csv'

        # Mock bot and message
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123
        message.text = 'testuser@example.com'

        # Call the function
        process_email_input(message, bot)

        # Assertions
        mock_extract_run.assert_called_once_with(message, bot)
        mock_smtp.assert_called()
        bot.send_message.assert_called_with(123, 'Email sent successfully!')

    @patch('logging.error')
    def test_run_with_exception(self, mock_log_error):
        # Mock bot and message
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123

        # Force an exception
        bot.send_message.side_effect = Exception('Test exception')

        # Call the function
        run(message, bot)

        # Assertions
        mock_log_error.assert_called_once_with('Test exception')

if __name__ == '__main__':
    unittest.main()
