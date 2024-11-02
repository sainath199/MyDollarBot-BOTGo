import unittest
from unittest.mock import patch, Mock
import os
import sys

# Add the 'code' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

from sendEmail import send_email, process_email_input, run

class TestSendEmail(unittest.TestCase):
    @patch('sendEmail.smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        # Set up your mock SMTP server
        mock_server = Mock()
        mock_smtp.return_value = mock_server

        user_email = "example@example.com"
        subject = "Test Subject"
        message = "Test Message"
        attachment_path = 'test_attachment.txt'  # Use the file name

        # Create a dummy test attachment file
        with open('test_attachment.txt', 'w') as dummy_file:
            dummy_file.write("This is a test attachment.")

        try:
            send_email(user_email, subject, message, attachment_path)

            # Check that the SMTP server is called with the correct arguments
            mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("dollarbot123@gmail.com", "tsvueizeuvzivtjo")
            mock_server.sendmail.assert_called_once()
            mock_server.quit.assert_called_once()

        finally:
            # Remove the dummy test attachment file
            os.remove('test_attachment.txt')

class TestProcessEmailInput(unittest.TestCase):
    @patch('sendEmail.send_email')
    def test_process_email_input(self, mock_send_email):
        # Create a mock message with chat.id and text
        message = Mock()
        message.chat.id = 12345
        message.text = 'user@example.com'

        # Create a mock bot
        bot = Mock()

        # Assume 'data.csv' exists
        with patch('sendEmail.os.path.isfile', return_value=True):
            # Call the function
            process_email_input(message, bot)

            # Check that send_email was called with correct parameters
            mock_send_email.assert_called_once_with(
                'user@example.com',
                'DollarBot Budget Report',
                'Hello user@example.com,\n\nPFA the budget report that you requested.',
                'code/data.csv'
            )

            # Check that bot.send_message was called
            bot.send_message.assert_called_with(12345, 'Email sent successfully!')

class TestProcessEmailInputNoDataFile(unittest.TestCase):
    @patch('sendEmail.extract.run')
    @patch('sendEmail.send_email')
    def test_process_email_input_no_data_file(self, mock_send_email, mock_extract_run):
        # Create a mock message with chat.id and text
        message = Mock()
        message.chat.id = 12345
        message.text = 'user@example.com'

        # Create a mock bot
        bot = Mock()

        # Assume 'data.csv' does not exist
        with patch('sendEmail.os.path.isfile', return_value=False):
            # Mock extract.run to return a file path
            mock_extract_run.return_value = 'some_file_path.csv'

            # Call the function
            process_email_input(message, bot)

            # Check that extract.run was called
            mock_extract_run.assert_called_once_with(message, bot)

            # Check that send_email was called with correct parameters
            mock_send_email.assert_called_once_with(
                'user@example.com',
                'DollarBot Budget Report',
                'Hello user@example.com,\n\nPFA the budget report that you requested.',
                'some_file_path.csv'
            )

            # Check that bot.send_message was called
            bot.send_message.assert_called_with(12345, 'Email sent successfully!')

class TestRunFunction(unittest.TestCase):
    def test_run_function(self):
        # Create a mock message with chat.id
        message = Mock()
        message.chat.id = 12345

        # Create a mock bot
        bot = Mock()

        # Mock bot.send_message to return a message
        bot.send_message.return_value = 'message_object'

        # Call the function
        run(message, bot)

        # Check that bot.send_message was called with correct parameters
        bot.send_message.assert_called_with(12345, 'Please enter your email: ')

        # Check that bot.register_next_step_handler was called with correct parameters
        bot.register_next_step_handler.assert_called_with('message_object', process_email_input, bot)

if __name__ == '__main__':
    unittest.main()