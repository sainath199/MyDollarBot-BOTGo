import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the 'code' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import edit
from telebot import types

class TestEditModule(unittest.TestCase):
    def setUp(self):
        # Common setup for tests
        self.chat_id = 12345
        self.mock_bot = MagicMock()
        self.message = MagicMock()
        self.message.chat.id = self.chat_id

    @patch('edit.helper')
    def test_run_with_user_history(self, mock_helper):
        """Test the 'run' function when user has expense history."""
        # Mock user history
        user_history = ['2023-10-31,Food,10.00', '2023-10-30,Transport,5.00']
        mock_helper.getUserHistory.return_value = user_history

        # Call the function
        edit.run(self.message, self.mock_bot)

        # Assert that reply_to was called with expected parameters
        self.assertTrue(self.mock_bot.reply_to.called)
        reply_call_args = self.mock_bot.reply_to.call_args

        # Access args and kwargs from call_args
        args = reply_call_args.args
        kwargs = reply_call_args.kwargs

        self.assertEqual(args[0], self.message)
        self.assertEqual(args[1], "Select expense to be edited:")
        # 'reply_markup' is passed via kwargs
        self.assertIn('reply_markup', kwargs)
        self.assertIsInstance(kwargs['reply_markup'], types.ReplyKeyboardMarkup)

        # Assert that register_next_step_handler was called
        self.assertTrue(self.mock_bot.register_next_step_handler.called)

    @patch('edit.helper')
    def test_select_category_to_be_updated(self, mock_helper):
        """Test 'select_category_to_be_updated' function."""
        # Simulate user message with selected expense
        self.message.text = 'Date=2023-10-31,		Category=Food,		Amount=$10.00'

        # Call the function
        edit.select_category_to_be_updated(self.message, self.mock_bot)

        # Assert that reply_to was called asking what to update
        self.assertTrue(self.mock_bot.reply_to.called)
        reply_call_args = self.mock_bot.reply_to.call_args

        # Access args and kwargs from call_args
        args = reply_call_args.args
        kwargs = reply_call_args.kwargs

        self.assertEqual(args[1], "What do you want to update?")
        self.assertIn('reply_markup', kwargs)
        self.assertIsInstance(kwargs['reply_markup'], types.ReplyKeyboardMarkup)

        # Assert that register_next_step_handler was called
        self.assertTrue(self.mock_bot.register_next_step_handler.called)

    @patch('edit.helper')
    def test_enter_updated_data(self, mock_helper):
        """Test 'enter_updated_data' function."""
        # Mock getSpendCategories
        mock_helper.getSpendCategories.return_value = ['Food', 'Transport', 'Entertainment']

        # Simulate user choosing to update 'Category'
        self.message.text = 'Category'

        # Selected data from previous step
        selected_data = ['Date=2023-10-31', 'Category=Food', 'Amount=$10.00']

        # Call the function
        edit.enter_updated_data(self.message, self.mock_bot, selected_data)

        # Assert that reply_to was called to select new category
        self.assertTrue(self.mock_bot.reply_to.called)
        reply_call_args = self.mock_bot.reply_to.call_args

        # Access args and kwargs from call_args
        args = reply_call_args.args
        kwargs = reply_call_args.kwargs

        self.assertEqual(args[1], "Please select the new category")
        self.assertIn('reply_markup', kwargs)
        self.assertIsInstance(kwargs['reply_markup'], types.ReplyKeyboardMarkup)

        # Assert that register_next_step_handler was called
        self.assertTrue(self.mock_bot.register_next_step_handler.called)

    @patch('edit.helper')
    def test_edit_date_with_valid_date(self, mock_helper):
        """Test 'edit_date' function with valid date input."""
        # Mock data
        mock_helper.read_json.return_value = {
            str(self.chat_id): {'data': ['2023-10-31,Food,10.00']}
        }
        mock_helper.getUserHistory.return_value = ['2023-10-31,Food,10.00']

        # Simulate user entering a valid date
        self.message.text = '01-Nov-2023'

        selected_data = ['Date=2023-10-31', 'Category=Food', 'Amount=$10.00']

        # Call the function
        edit.edit_date(self.message, self.mock_bot, selected_data)

        # Assert that write_json was called
        self.assertTrue(mock_helper.write_json.called)

        # Assert that reply_to was called with 'Date is updated'
        self.mock_bot.reply_to.assert_called_with(self.message, "Date is updated")

    @patch('edit.helper')
    def test_edit_date_with_invalid_date(self, mock_helper):
        """Test 'edit_date' function with invalid date input."""
        # Simulate user entering an invalid date
        self.message.text = 'Invalid-Date'

        selected_data = ['Date=2023-10-31', 'Category=Food', 'Amount=$10.00']

        # Call the function
        edit.edit_date(self.message, self.mock_bot, selected_data)

        # Assert that write_json was not called
        self.assertFalse(mock_helper.write_json.called)

        # Assert that reply_to was called with 'The date is incorrect'
        self.mock_bot.reply_to.assert_called_with(self.message, "The date is incorrect")

    @patch('edit.helper')
    def test_edit_cat(self, mock_helper):
        """Test 'edit_cat' function."""
        # Mock data
        mock_helper.read_json.return_value = {
            str(self.chat_id): {'data': ['2023-10-31,Food,10.00']}
        }
        mock_helper.getUserHistory.return_value = ['2023-10-31,Food,10.00']

        # Simulate user entering a new category
        self.message.text = 'Transport'

        selected_data = ['Date=2023-10-31', 'Category=Food', 'Amount=$10.00']

        # Call the function
        edit.edit_cat(self.message, self.mock_bot, selected_data)

        # Assert that write_json was called
        self.assertTrue(mock_helper.write_json.called)

        # Assert that reply_to was called with 'Category is updated'
        self.mock_bot.reply_to.assert_called_with(self.message, "Category is updated")

    @patch('edit.helper')
    def test_edit_cost_with_valid_amount(self, mock_helper):
        """Test 'edit_cost' function with valid amount."""
        # Mock data
        mock_helper.read_json.return_value = {
            str(self.chat_id): {'data': ['2023-10-31,Food,10.00']}
        }
        mock_helper.getUserHistory.return_value = ['2023-10-31,Food,10.00']
        mock_helper.validate_entered_amount.return_value = 1  # Non-zero indicates valid

        # Simulate user entering a new cost
        self.message.text = '15.00'

        selected_data = ['Date=2023-10-31', 'Category=Food', 'Amount=$10.00']

        # Call the function
        edit.edit_cost(self.message, self.mock_bot, selected_data)

        # Assert that validate_entered_amount was called
        mock_helper.validate_entered_amount.assert_called_with('15.00')

        # Assert that write_json was called
        self.assertTrue(mock_helper.write_json.called)

        # Assert that reply_to was called with 'Expense amount is updated'
        self.mock_bot.reply_to.assert_called_with(self.message, "Expense amount is updated")

    @patch('edit.helper')
    def test_edit_cost_with_invalid_amount(self, mock_helper):
        """Test 'edit_cost' function with invalid amount."""
        # Mock data
        mock_helper.validate_entered_amount.return_value = 0  # Zero indicates invalid

        # Simulate user entering an invalid cost
        self.message.text = 'InvalidAmount'

        selected_data = ['Date=2023-10-31', 'Category=Food', 'Amount=$10.00']

        # Call the function
        edit.edit_cost(self.message, self.mock_bot, selected_data)

        # Assert that write_json was not called
        self.assertFalse(mock_helper.write_json.called)

        # Assert that reply_to was called with 'The cost is invalid'
        self.mock_bot.reply_to.assert_called_with(self.message, "The cost is invalid")

if __name__ == '__main__':
    unittest.main()
