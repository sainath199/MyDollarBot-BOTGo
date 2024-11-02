import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the 'code' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import income

class TestIncomeModule(unittest.TestCase):

    @patch('income.helper.setUserIncome')
    def test_process_income_input_valid(self, mock_set_user_income):
        """Test process_income_input with valid numeric input."""
        chat_id = 12345
        income_value = '1000.0'
        expected_message = "Your monthly income has been set to $1000.0."

        # Mock objects
        mock_bot = MagicMock()
        message = MagicMock(chat=MagicMock(id=chat_id), text=income_value)

        # Call the function
        income.process_income_input(message, mock_bot)

        # Assertions
        mock_set_user_income.assert_called_once_with(chat_id, float(income_value))
        mock_bot.send_message.assert_called_once_with(chat_id, expected_message)

    @patch('income.helper.setUserIncome')
    def test_process_income_input_invalid_input(self, mock_set_user_income):
        """Test process_income_input with invalid (non-numeric) input."""
        chat_id = 12345
        income_value = 'abc'
        expected_message = "Invalid input. Please enter a numeric value for your income."

        # Mock objects
        mock_bot = MagicMock()
        message = MagicMock(chat=MagicMock(id=chat_id), text=income_value)

        # Modify the process_income_input function to handle ValueError
        with self.assertRaises(ValueError):
            income.process_income_input(message, mock_bot)

        # Ensure that setUserIncome was not called
        mock_set_user_income.assert_not_called()
        # Check that bot.send_message was not called
        mock_bot.send_message.assert_not_called()

    @patch('income.helper.setUserIncome')
    def test_process_income_input_negative_income(self, mock_set_user_income):
        """Test process_income_input with negative income."""
        chat_id = 12345
        income_value = '-1000.0'
        expected_message = "Your monthly income has been set to $-1000.0."

        # Mock objects
        mock_bot = MagicMock()
        message = MagicMock(chat=MagicMock(id=chat_id), text=income_value)

        # Call the function
        income.process_income_input(message, mock_bot)

        # Assertions
        mock_set_user_income.assert_called_once_with(chat_id, float(income_value))
        mock_bot.send_message.assert_called_once_with(chat_id, expected_message)

    @patch('income.helper.setUserIncome')
    def test_process_income_input_zero_income(self, mock_set_user_income):
        """Test process_income_input with zero income."""
        chat_id = 12345
        income_value = '0.0'
        expected_message = "Your monthly income has been set to $0.0."

        # Mock objects
        mock_bot = MagicMock()
        message = MagicMock(chat=MagicMock(id=chat_id), text=income_value)

        # Call the function
        income.process_income_input(message, mock_bot)

        # Assertions
        mock_set_user_income.assert_called_once_with(chat_id, float(income_value))
        mock_bot.send_message.assert_called_once_with(chat_id, expected_message)

    @patch('income.helper.getUserData')
    @patch('income.helper.calculate_total_expenditure')
    @patch('income.helper.convert_currency')
    def test_check_transaction_limit_within_income(self, mock_convert_currency, mock_calculate_expenditure, mock_get_user_data):
        """Test check_transaction_limit when transaction is within income limit."""
        chat_id = 12345
        amount = 100.0
        currency = 'USD'
        converted_amount = 100.0
        total_expenditure = 200.0
        user_income = 500.0

        # Mock return values
        mock_get_user_data.return_value = {'income': user_income}
        mock_calculate_expenditure.return_value = total_expenditure
        mock_convert_currency.return_value = converted_amount

        # Mock bot
        mock_bot = MagicMock()

        # Call the function
        result = income.check_transaction_limit(chat_id, amount, currency, mock_bot)

        # Assertions
        self.assertFalse(result)
        mock_bot.send_message.assert_not_called()

    @patch('income.helper.getUserData')
    @patch('income.helper.calculate_total_expenditure')
    @patch('income.helper.convert_currency')
    def test_check_transaction_limit_exceeds_income(self, mock_convert_currency, mock_calculate_expenditure, mock_get_user_data):
        """Test check_transaction_limit when transaction exceeds income limit."""
        chat_id = 12345
        amount = 300.0
        currency = 'USD'
        converted_amount = 300.0
        total_expenditure = 250.0
        user_income = 500.0

        # Mock return values
        mock_get_user_data.return_value = {'income': user_income}
        mock_calculate_expenditure.return_value = total_expenditure
        mock_convert_currency.return_value = converted_amount

        # Mock bot
        mock_bot = MagicMock()

        # Expected message
        expected_message = (
            f"Transaction cannot be recorded! Your total expenditure of ${total_expenditure + converted_amount} "
            f"exceeds your monthly income of ${user_income}. Please update your income or hold off on new transactions."
        )

        # Call the function
        result = income.check_transaction_limit(chat_id, amount, currency, mock_bot)

        # Assertions
        self.assertTrue(result)
        mock_bot.send_message.assert_called_once_with(chat_id, expected_message)

    @patch('income.helper.getUserData')
    def test_check_transaction_limit_no_income_set(self, mock_get_user_data):
        """Test check_transaction_limit when user has not set income."""
        chat_id = 12345
        amount = 100.0
        currency = 'USD'

        # Mock return value
        mock_get_user_data.return_value = {}

        # Mock bot
        mock_bot = MagicMock()

        # Expected message
        expected_message = "You haven't set your monthly income yet. Please use /income to set your income."

        # Call the function
        result = income.check_transaction_limit(chat_id, amount, currency, mock_bot)

        # Assertions
        self.assertTrue(result)
        mock_bot.send_message.assert_called_once_with(chat_id, expected_message)

    @patch('income.helper.getUserData')
    def test_check_transaction_limit_income_zero(self, mock_get_user_data):
        """Test check_transaction_limit when income is zero."""
        chat_id = 12345
        amount = 100.0
        currency = 'USD'

        # Mock return value
        mock_get_user_data.return_value = {'income': 0}

        # Mock bot
        mock_bot = MagicMock()

        # Expected message
        expected_message = "You haven't set your monthly income yet. Please use /income to set your income."

        # Call the function
        result = income.check_transaction_limit(chat_id, amount, currency, mock_bot)

        # Assertions
        self.assertTrue(result)
        mock_bot.send_message.assert_called_once_with(chat_id, expected_message)

    def test_set_income(self):
        """Test set_income sends the correct prompt to the user."""
        chat_id = 12345

        # Mock bot
        mock_bot = MagicMock()
        message = MagicMock(chat=MagicMock(id=chat_id))

        # Call the function
        income.set_income(message, mock_bot)

        # Assertions
        mock_bot.send_message.assert_called_once_with(chat_id, "Please enter your monthly income:")

if __name__ == '__main__':
    unittest.main()