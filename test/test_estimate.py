import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the 'code' directory to sys.path to import the estimate module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import estimate  # Assuming your code is saved in 'estimate.py'
from telebot import types

class TestEstimateModule(unittest.TestCase):
    def setUp(self):
        self.chat_id = 12345
        self.message = MagicMock()
        self.message.chat.id = self.chat_id
        self.bot = MagicMock()

    @patch('estimate.helper')
    def test_run_no_history(self, mock_helper):
        """Test the 'run' function when the user has no spending history."""
        # Mock helper.getUserHistory to return None
        mock_helper.getUserHistory.return_value = None

        # Call the function
        estimate.run(self.message, self.bot)

        # Assert that bot.send_message was called with the appropriate message
        self.bot.send_message.assert_called_with(
            self.chat_id, "Oops! Looks like you do not have any spending records!"
        )

        # Assert that bot.reply_to was not called
        self.bot.reply_to.assert_not_called()

        # Assert that bot.register_next_step_handler was not called
        self.bot.register_next_step_handler.assert_not_called()

        # Assert that helper.read_json was called
        mock_helper.read_json.assert_called_once()

    @patch('estimate.helper')
    def test_run_with_history(self, mock_helper):
        """Test the 'run' function when the user has spending history."""
        # Mock helper.getUserHistory to return some history
        mock_helper.getUserHistory.return_value = ['2023-11-01,Food,20.0']

        # Mock helper.getSpendEstimateOptions
        mock_helper.getSpendEstimateOptions.return_value = ['Next day', 'Next month']

        # Call the function
        estimate.run(self.message, self.bot)

        # Assert that bot.reply_to was called with the correct message and markup
        self.bot.reply_to.assert_called_once()
        args, kwargs = self.bot.reply_to.call_args
        self.assertEqual(args[0], self.message)
        self.assertEqual(args[1], 'Please select the period to estimate')
        self.assertIn('reply_markup', kwargs)
        self.assertIsInstance(kwargs['reply_markup'], types.ReplyKeyboardMarkup)

        # Check that the markup contains the options
        markup = kwargs['reply_markup']
        keyboard = markup.keyboard
        expected_options = ['Next day', 'Next month']
        # Flatten the keyboard to get the button texts
        flattened_keyboard = []
        for row in keyboard:
            for button in row:
                if isinstance(button, types.KeyboardButton):
                    flattened_keyboard.append(button.text)
                elif isinstance(button, dict) and 'text' in button:
                    flattened_keyboard.append(button['text'])
                elif isinstance(button, str):
                    flattened_keyboard.append(button)
                else:
                    flattened_keyboard.append(str(button))
        for option in expected_options:
            self.assertIn(option, flattened_keyboard)

        # Assert that bot.register_next_step_handler was called
        self.bot.register_next_step_handler.assert_called_once()
        registered_handler = self.bot.register_next_step_handler.call_args[0][1]
        self.assertEqual(registered_handler, estimate.estimate_total)

        # Assert that helper.read_json was called
        mock_helper.read_json.assert_called_once()

    @patch('estimate.helper')
    def test_estimate_total_valid_option(self, mock_helper):
        """Test 'estimate_total' function with a valid option."""
        # Mock helper.getSpendEstimateOptions
        mock_helper.getSpendEstimateOptions.return_value = ['Next day', 'Next month']

        # Mock helper.getUserHistory
        mock_helper.getUserHistory.return_value = ['2023-11-01,Food,20.0', '2023-11-01,Transport,10.0']

        # Set message.text to a valid option
        self.message.text = 'Next day'

        # Patch time.sleep and calculate_estimate
        with patch('estimate.time.sleep') as mock_sleep, \
             patch('estimate.calculate_estimate') as mock_calculate_estimate:
            mock_calculate_estimate.return_value = 'Food $20.0\nTransport $10.0\n'

            estimate.estimate_total(self.message, self.bot)

            # Assert that bot.send_message was called with 'Hold on! Calculating...'
            self.bot.send_message.assert_any_call(self.chat_id, "Hold on! Calculating...")

            # Assert that bot.send_chat_action was called with 'typing'
            self.bot.send_chat_action.assert_called_with(self.chat_id, 'typing')

            # Assert that time.sleep was called with 0.5
            mock_sleep.assert_called_with(0.5)

            # Check that bot.send_message was called with the expected spending text
            expected_spending_text = (
                "Here are your estimated spendings for the next day"
                ":\nCATEGORIES,AMOUNT \n----------------------\n"
                "Food $20.0\nTransport $10.0\n"
            )

            self.bot.send_message.assert_called_with(self.chat_id, expected_spending_text)

    @patch('estimate.helper')
    def test_estimate_total_invalid_option(self, mock_helper):
        """Test 'estimate_total' function with an invalid option."""
        # Mock helper.getSpendEstimateOptions
        mock_helper.getSpendEstimateOptions.return_value = ['Next day', 'Next month']

        # Set message.text to an invalid option
        self.message.text = 'Invalid option'

        # Call the function
        with patch('logging.exception') as mock_logging_exception:
            estimate.estimate_total(self.message, self.bot)

            # Assert that bot.reply_to was called with the exception message
            self.bot.reply_to.assert_called_with(
                self.message, 'Sorry I can\'t show an estimate for "Invalid option"!'
            )

            # Check that logging.exception was called
            mock_logging_exception.assert_called_once()

    @patch('estimate.helper')
    def test_estimate_total_no_history(self, mock_helper):
        """Test 'estimate_total' function when the user has no history."""
        # Mock helper.getSpendEstimateOptions
        mock_helper.getSpendEstimateOptions.return_value = ['Next day', 'Next month']

        # Set message.text to a valid option
        self.message.text = 'Next day'

        # Mock helper.getUserHistory to return None
        mock_helper.getUserHistory.return_value = None

        # Call the function
        with patch('logging.exception') as mock_logging_exception:
            estimate.estimate_total(self.message, self.bot)

            # Assert that bot.reply_to was called with the exception message
            self.bot.reply_to.assert_called_with(
                self.message, 'Oops! Looks like you do not have any spending records!'
            )

            # Check that logging.exception was called
            mock_logging_exception.assert_called_once()

    def test_calculate_estimate(self):
        """Test 'calculate_estimate' function with sample data."""
        queryResult = [
            '2023-11-01,Food,20.0',
            '2023-11-01,Transport,10.0',
            '2023-11-02,Food,30.0',
        ]
        days_to_estimate = 1

        result = estimate.calculate_estimate(queryResult, days_to_estimate)

        expected_result = 'Food $25.0\nTransport $5.0\n'

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
