import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust sys.path to include the directory where 'history.py' is located
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import history  # Assuming 'history.py' is in the 'code' directory
from telebot import types

def create_message(text, chat_id=12345):
    params = {'messagebody': text}
    chat = types.User(chat_id, False, 'test')
    message = types.Message(1, None, None, chat, 'text', params, "")
    message.text = text
    return message

class TestHistoryModule(unittest.TestCase):

    def setUp(self):
        self.chat_id = 12345
        self.bot = MagicMock()
        self.message = create_message("Test message", chat_id=self.chat_id)

    @patch('history.helper')
    @patch('history.plt')
    def test_run_with_data(self, mock_plt, mock_helper):
        """Test 'run' function when the user has spending data."""
        # Mock user history data
        mock_helper.getUserHistory.return_value = [
            '01-Jan-2021,Food,100,USD',
            '15-Feb-2021,Transport,50,USD',
            '20-Mar-2021,Entertainment,75,USD'
        ]

        # Mock user's preferred currency
        mock_helper.get_user_preferred_currency.return_value = 'USD'

        # Mock convert_currency to return the same amount (assuming USD to USD conversion)
        mock_helper.convert_currency.side_effect = lambda amount, from_currency, to_currency: amount

        # Call the function
        history.run(self.message, self.bot)

        # Assert that bot.send_message was called with the spending history
        expected_message = (
            'Here is your spending history (converted to USD): \n'
            'DATE, CATEGORY, AMOUNT\n'
            '----------------------\n'
            '01-Jan-2021,Food,100,USD\n'
            '15-Feb-2021,Transport,50,USD\n'
            '20-Mar-2021,Entertainment,75,USD\n'
        )
        self.bot.send_message.assert_called_with(self.chat_id, expected_message)

        # Assert that matplotlib functions were called to generate the plot
        mock_plt.clf.assert_called_once()
        mock_plt.bar.assert_called_once()
        mock_plt.savefig.assert_called_once_with('histo.png')

        # Assert that bot.send_photo was called to send the histogram
        self.bot.send_photo.assert_called_once()

    @patch('history.helper')
    @patch('history.logging')
    def test_run_no_user_history(self, mock_logging, mock_helper):
        """Test 'run' function when getUserHistory returns None."""
        # Mock getUserHistory to return None
        mock_helper.getUserHistory.return_value = None

        # Call the function
        history.run(self.message, self.bot)

        # Assert that bot.reply_to was called with the error message
        self.bot.reply_to.assert_called_with(
            self.message,
            'Oops!Sorry! No spending records found!'
        )

        # Assert that bot.send_message was not called
        self.bot.send_message.assert_not_called()

        # Assert that bot.send_photo was not called
        self.bot.send_photo.assert_not_called()

        # Assert that logging.exception was called
        mock_logging.exception.assert_called_once()

    @patch('history.helper')
    @patch('history.plt')
    def test_run_with_currency_conversion(self, mock_plt, mock_helper):
        """Test 'run' function when currency conversion is required."""
        # Mock user history data with different currencies
        mock_helper.getUserHistory.return_value = [
            '01-Jan-2021,Food,100,EUR',
            '15-Feb-2021,Transport,50,USD',
            '20-Mar-2021,Entertainment,75,GBP'
        ]

        # Mock user's preferred currency
        mock_helper.get_user_preferred_currency.return_value = 'USD'

        # Mock convert_currency to simulate conversion rates
        def mock_convert(amount, from_currency, to_currency):
            rates = {
                ('EUR', 'USD'): 1.2,
                ('GBP', 'USD'): 1.4,
                ('USD', 'USD'): 1.0
            }
            rate = rates.get((from_currency, to_currency), 1.0)
            return amount * rate

        mock_helper.convert_currency.side_effect = mock_convert

        # Call the function
        history.run(self.message, self.bot)

        # Assert that bot.send_message was called with the spending history
        expected_message = (
            'Here is your spending history (converted to USD): \n'
            'DATE, CATEGORY, AMOUNT\n'
            '----------------------\n'
            '01-Jan-2021,Food,100,EUR\n'
            '15-Feb-2021,Transport,50,USD\n'
            '20-Mar-2021,Entertainment,75,GBP\n'
        )
        self.bot.send_message.assert_called_with(self.chat_id, expected_message)

        # Assert that convert_currency was called correctly
        mock_helper.convert_currency.assert_any_call(100.0, 'EUR', 'USD')
        mock_helper.convert_currency.assert_any_call(50.0, 'USD', 'USD')
        mock_helper.convert_currency.assert_any_call(75.0, 'GBP', 'USD')

        # Assert that matplotlib functions were called to generate the plot
        mock_plt.clf.assert_called_once()
        mock_plt.bar.assert_called_once()
        mock_plt.savefig.assert_called_once_with('histo.png')

        # Assert that bot.send_photo was called to send the histogram
        self.bot.send_photo.assert_called_once()

    @patch('history.helper')
    @patch('history.plt')
    def test_run_with_missing_currency_info(self, mock_plt, mock_helper):
        """Test 'run' function when some records lack currency info."""
        # Mock user history data with missing currency
        mock_helper.getUserHistory.return_value = [
            '01-Jan-2021,Food,100',  # Missing currency, should default to USD
            '15-Feb-2021,Transport,50,USD',
            '20-Mar-2021,Entertainment,75,EUR'
        ]

        # Mock user's preferred currency
        mock_helper.get_user_preferred_currency.return_value = 'USD'

        # Mock convert_currency
        def mock_convert(amount, from_currency, to_currency):
            rates = {
                ('USD', 'USD'): 1.0,
                ('EUR', 'USD'): 1.2,
            }
            rate = rates.get((from_currency, to_currency), 1.0)
            return amount * rate

        mock_helper.convert_currency.side_effect = mock_convert

        # Call the function
        history.run(self.message, self.bot)

        # Assert that bot.send_message was called with the spending history
        expected_message = (
            'Here is your spending history (converted to USD): \n'
            'DATE, CATEGORY, AMOUNT\n'
            '----------------------\n'
            '01-Jan-2021,Food,100\n'
            '15-Feb-2021,Transport,50,USD\n'
            '20-Mar-2021,Entertainment,75,EUR\n'
        )
        self.bot.send_message.assert_called_with(self.chat_id, expected_message)

        # Assert that convert_currency was called correctly
        mock_helper.convert_currency.assert_any_call(100.0, 'USD', 'USD')  # Default currency
        mock_helper.convert_currency.assert_any_call(50.0, 'USD', 'USD')
        mock_helper.convert_currency.assert_any_call(75.0, 'EUR', 'USD')

        # Assert that matplotlib functions were called
        mock_plt.clf.assert_called_once()
        mock_plt.bar.assert_called_once()
        mock_plt.savefig.assert_called_once_with('histo.png')

        # Assert that bot.send_photo was called
        self.bot.send_photo.assert_called_once()

if __name__ == '__main__':
    unittest.main()
