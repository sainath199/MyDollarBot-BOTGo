import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add 'code' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import budget_max  # Assuming 'budget_max.py' is in the 'code' directory
from telebot import types

class TestBudgetMax(unittest.TestCase):

    def setUp(self):
        self.chat_id = 12345
        self.bot = MagicMock()
        self.message = MagicMock()
        self.message.chat.id = self.chat_id

    @patch('budget_max.helper')
    def test_run_with_existing_limit(self, mock_helper):
        """Test the 'run' function when a max limit exists."""
        # Mock helper methods
        mock_helper.isMaxTransactionLimitAvailable.return_value = True
        mock_helper.getMaxTransactionLimit.return_value = 100

        # Call the function
        budget_max.run(self.message, self.bot)

        # Expected message
        expected_msg = 'Current Limit is $100\n\nHow much is your new Max limit per transaction? \n(Enter numeric values only)'

        # Assert that bot.send_message was called with the expected message
        self.bot.send_message.assert_called_with(self.chat_id, expected_msg)

        # Assert that bot.register_next_step_handler was called
        self.bot.register_next_step_handler.assert_called_once_with(
            self.bot.send_message.return_value, budget_max.post_max_budget, self.bot
        )

    @patch('budget_max.helper')
    def test_run_without_existing_limit(self, mock_helper):
        """Test the 'run' function when no max limit exists."""
        # Mock helper methods
        mock_helper.isMaxTransactionLimitAvailable.return_value = False

        # Call the function
        budget_max.run(self.message, self.bot)

        # Expected message
        expected_msg = 'How much is your new Max limit per transaction? \n(Enter numeric values only)'

        # Assert that bot.send_message was called with the expected message
        self.bot.send_message.assert_called_with(self.chat_id, expected_msg)

        # Assert that bot.register_next_step_handler was called
        self.bot.register_next_step_handler.assert_called_once_with(
            self.bot.send_message.return_value, budget_max.post_max_budget, self.bot
        )

    @patch('budget_max.helper')
    def test_post_max_budget_with_valid_amount(self, mock_helper):
        """Test 'post_max_budget' with a valid amount."""
        # Set up
        self.message.text = '50'

        # Mock helper methods
        mock_helper.validate_entered_amount.return_value = 50
        mock_helper.read_json.return_value = {}
        mock_helper.createNewUserRecord.return_value = {'budget': {}}
        mock_helper.write_json.return_value = True

        # Call the function
        user_list = budget_max.post_max_budget(self.message, self.bot)

        # Assert that bot.send_message was called with 'Max Limit Updated!'
        self.bot.send_message.assert_called_with(self.chat_id, 'Max Limit Updated!')

        # Check that the user_list was updated correctly
        self.assertIn(str(self.chat_id), user_list)
        self.assertEqual(user_list[str(self.chat_id)]['budget']['max_per_txn_spend'], 50)

        # Assert that helper.write_json was called with the updated user_list
        mock_helper.write_json.assert_called_once_with(user_list)

    @patch('budget_max.helper')
    def test_post_max_budget_with_invalid_amount(self, mock_helper):
        """Test 'post_max_budget' with an invalid amount."""
        # Set up
        self.message.text = 'invalid_amount'

        # Mock helper methods
        mock_helper.validate_entered_amount.return_value = 0  # Invalid amount

        # Patch logging to suppress output during tests
        with patch('budget_max.logging'):
            # Call the function
            budget_max.post_max_budget(self.message, self.bot)

            # Assert that helper.throw_exception was called
            mock_helper.throw_exception.assert_called_once()

            # Assert that bot.send_message was not called with 'Max Limit Updated!'
            self.bot.send_message.assert_not_called()

    @patch('budget_max.helper')
    def test_post_max_budget_with_exception(self, mock_helper):
        """Test 'post_max_budget' when an exception occurs."""
        # Set up
        self.message.text = '50'

        # Mock helper methods to raise an exception
        mock_helper.validate_entered_amount.side_effect = Exception('Test Exception')

        # Patch logging to suppress output during tests
        with patch('budget_max.logging'):
            # Call the function
            budget_max.post_max_budget(self.message, self.bot)

            # Assert that helper.throw_exception was called
            mock_helper.throw_exception.assert_called_once()

            # Assert that bot.send_message was not called with 'Max Limit Updated!'
            self.bot.send_message.assert_not_called()

if __name__ == '__main__':
    unittest.main()
