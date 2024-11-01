import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust sys.path to include the directory where 'budget_view.py' is located
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import budget_view  # Assuming 'budget_view.py' is in the 'code' directory
from telebot import types

def create_message(text, chat_id=12345):
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
    message.text = text
    return message

class TestBudgetViewModule(unittest.TestCase):

    def setUp(self):
        self.chat_id = 12345
        self.bot = MagicMock()
        self.message = create_message("Test message", chat_id=self.chat_id)

    @patch('budget_view.helper')
    def test_display_overall_budget(self, mock_helper):
        """Test the 'display_overall_budget' function."""
        # Mock helper.getOverallBudget to return a test value
        mock_helper.getOverallBudget.return_value = '1000'

        # Call the function
        budget_view.display_overall_budget(self.message, self.bot)

        # Assert that bot.send_message was called with correct parameters
        self.bot.send_message.assert_called_once_with(
            self.chat_id,
            'Overall Budget: $1000'
        )

    @patch('budget_view.helper')
    def test_display_category_budget(self, mock_helper):
        """Test the 'display_category_budget' function."""
        # Mock helper.getCategoryBudget to return test data
        mock_helper.getCategoryBudget.return_value = {
            'Food': '200',
            'Transport': '150',
            'Entertainment': '100'
        }

        # Call the function
        budget_view.display_category_budget(self.message, self.bot)

        # Build the expected message
        expected_message = (
            'Budget Summary\n'
            'Food: $200\n'
            'Transport: $150\n'
            'Entertainment: $100\n'
        )

        # Assert that bot.send_message was called with correct parameters
        self.bot.send_message.assert_called_once_with(
            self.chat_id,
            expected_message
        )

    @patch('budget_view.helper')
    def test_run_overall_budget_available(self, mock_helper):
        """Test 'run' function when overall budget is available."""
        # Mock helper functions
        mock_helper.isOverallBudgetAvailable.return_value = True
        mock_helper.isCategoryBudgetAvailable.return_value = False

        # Mock display_overall_budget function
        with patch('budget_view.display_overall_budget') as mock_display_overall_budget:
            # Call the function
            budget_view.run(self.message, self.bot)

            # Assert that display_overall_budget was called
            mock_display_overall_budget.assert_called_once_with(self.message, self.bot)

    @patch('budget_view.helper')
    def test_run_category_budget_available(self, mock_helper):
        """Test 'run' function when category budget is available."""
        # Mock helper functions
        mock_helper.isOverallBudgetAvailable.return_value = False
        mock_helper.isCategoryBudgetAvailable.return_value = True

        # Mock display_category_budget function
        with patch('budget_view.display_category_budget') as mock_display_category_budget:
            # Call the function
            budget_view.run(self.message, self.bot)

            # Assert that display_category_budget was called
            mock_display_category_budget.assert_called_once_with(self.message, self.bot)

    @patch('budget_view.helper')
    @patch('budget_view.logging')
    def test_run_no_budget_available(self, mock_logging, mock_helper):
        """Test 'run' function when no budget is available."""
        # Mock helper functions
        mock_helper.isOverallBudgetAvailable.return_value = False
        mock_helper.isCategoryBudgetAvailable.return_value = False
        mock_helper.getBudgetOptions.return_value = {'update': '/updatebudget'}

        # Call the function
        budget_view.run(self.message, self.bot)

        # Build the expected exception message
        expected_exception = (
            'Budget does not exist. Use /updatebudget option to add/update the budget'
        )

        # Assert that helper.throw_exception was called with correct parameters
        mock_helper.throw_exception.assert_called_once()
        args, kwargs = mock_helper.throw_exception.call_args
        self.assertIsInstance(args[0], Exception)
        self.assertEqual(str(args[0]), expected_exception)
        self.assertEqual(args[1], self.message)
        self.assertEqual(args[2], self.bot)
        self.assertEqual(args[3], budget_view.logging)

    # Additional tests can be added here if needed

if __name__ == '__main__':
    unittest.main()
