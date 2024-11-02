import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import sys
import os

# Adjust sys.path to include the directory where 'helper.py' is located
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import helper  # Assuming 'helper.py' is in the 'code' directory

class TestHelperModule(unittest.TestCase):

    def setUp(self):
        self.chat_id = 12345
        self.bot = MagicMock()

    # Test the 'convert_currency' function
    def test_convert_currency_same_currency(self):
        """Test currency conversion when from_currency and to_currency are the same."""
        amount = 100
        from_currency = 'USD'
        to_currency = 'USD'
        result = helper.convert_currency(amount, from_currency, to_currency)
        self.assertEqual(result, amount)

    def test_convert_currency_supported_conversion(self):
        """Test currency conversion with supported currency pairs."""
        amount = 100
        from_currency = 'USD'
        to_currency = 'EUR'
        expected_result = round(amount * 0.95, 2)
        result = helper.convert_currency(amount, from_currency, to_currency)
        self.assertEqual(result, expected_result)

    def test_convert_currency_unsupported_conversion(self):
        """Test currency conversion with unsupported currency pairs."""
        amount = 100
        from_currency = 'USD'
        to_currency = 'JPY'  # Not in conversion_rates
        with self.assertRaises(ValueError):
            helper.convert_currency(amount, from_currency, to_currency)

    # Test the 'validate_entered_amount' function
    def test_validate_entered_amount_valid_int(self):
        """Test validation with a valid integer amount."""
        amount_entered = '100'
        result = helper.validate_entered_amount(amount_entered)
        self.assertEqual(result, '100.0')

    def test_validate_entered_amount_valid_float(self):
        """Test validation with a valid float amount."""
        amount_entered = '100.50'
        result = helper.validate_entered_amount(amount_entered)
        self.assertEqual(result, '100.5')

    def test_validate_entered_amount_invalid(self):
        """Test validation with an invalid amount."""
        amount_entered = 'abc'
        result = helper.validate_entered_amount(amount_entered)
        self.assertEqual(result, 0)

    # Test the 'read_json' function
    @patch('helper.os.path.exists')
    @patch('helper.os.stat')
    @patch('helper.open', new_callable=mock_open, read_data='{"data": "test_data"}')
    @patch('helper.json.load')
    def test_read_json_file_exists_with_data(self, mock_json_load, mock_open_file, mock_stat, mock_exists):
        """Test reading JSON when file exists and has data."""
        mock_exists.return_value = True
        mock_stat.return_value.st_size = 100  # Non-zero file size
        mock_json_load.return_value = {'data': 'test_data'}
        result = helper.read_json()
        mock_open_file.assert_called_with('expense_record.json')
        self.assertEqual(result, {'data': 'test_data'})

    @patch('helper.os.path.exists')
    @patch('helper.os.stat')
    @patch('helper.open', new_callable=mock_open)
    def test_read_json_file_exists_empty(self, mock_open_file, mock_stat, mock_exists):
        """Test reading JSON when file exists but is empty."""
        mock_exists.return_value = True
        mock_stat.return_value.st_size = 0  # Zero file size
        result = helper.read_json()
        self.assertEqual(result, {})

    @patch('helper.os.path.exists')
    @patch('helper.open', new_callable=mock_open)
    def test_read_json_file_not_exists(self, mock_open_file, mock_exists):
        """Test reading JSON when file does not exist."""
        mock_exists.return_value = False
        result = helper.read_json()
        mock_open_file.assert_called_with('expense_record.json', 'w')
        self.assertEqual(result, {})

    # Test the 'write_json' function
    @patch('helper.open', new_callable=mock_open)
    @patch('helper.json.dump')
    def test_write_json(self, mock_json_dump, mock_open_file):
        """Test writing data to JSON."""
        user_list = {'test': 'data'}
        helper.write_json(user_list)
        mock_open_file.assert_called_with('expense_record.json', 'w')
        mock_json_dump.assert_called_with(user_list, mock_open_file.return_value.__enter__(), ensure_ascii=False, indent=4)

    # Test 'getUserData' function
    @patch('helper.read_json')
    def test_getUserData_existing_user(self, mock_read_json):
        """Test getting user data when user exists."""
        mock_read_json.return_value = {str(self.chat_id): {'data': 'user_data'}}
        result = helper.getUserData(self.chat_id)
        self.assertEqual(result, {'data': 'user_data'})

    @patch('helper.read_json')
    def test_getUserData_non_existing_user(self, mock_read_json):
        """Test getting user data when user does not exist."""
        mock_read_json.return_value = {}
        result = helper.getUserData(self.chat_id)
        self.assertEqual(result, {})

    # Test 'setUserIncome' function
    @patch('helper.write_json')
    @patch('helper.read_json')
    def test_setUserIncome_new_user(self, mock_read_json, mock_write_json):
        """Test setting user income for a new user."""
        mock_read_json.return_value = {}
        helper.setUserIncome(self.chat_id, 5000)
        expected_data = {
            str(self.chat_id): {
                'data': [],
                'budget': {
                    'overall': None,
                    'category': None,
                    'max_per_txn_spend': None
                },
                'income': 5000
            }
        }
        mock_write_json.assert_called_once_with(expected_data)

    # Test 'calculate_total_expenditure' function
    @patch('helper.getUserData')
    def test_calculate_total_expenditure_no_data(self, mock_getUserData):
        """Test calculating total expenditure when no data is available."""
        mock_getUserData.return_value = {}
        total = helper.calculate_total_expenditure(self.chat_id)
        self.assertEqual(total, 0.0)

    @patch('helper.getUserData')
    def test_calculate_total_expenditure_with_data(self, mock_getUserData):
        """Test calculating total expenditure with transaction data."""
        mock_getUserData.return_value = {
            'data': [
                '01-Jan-2021,Food,100',
                '02-Jan-2021,Transport,50'
            ]
        }
        total = helper.calculate_total_expenditure(self.chat_id)
        self.assertEqual(total, 150.0)

    @patch('helper.getUserData')
    def test_calculate_total_expenditure_with_category(self, mock_getUserData):
        """Test calculating total expenditure for a specific category."""
        mock_getUserData.return_value = {
            'data': [
                '01-Jan-2021,Food,100',
                '02-Jan-2021,Transport,50',
                '03-Jan-2021,Food,75'
            ]
        }
        total_food = helper.calculate_total_expenditure(self.chat_id, category='Food')
        self.assertEqual(total_food, 175.0)

    # Test 'validate_transaction_limit' function
    @patch('helper.isMaxTransactionLimitAvailable')
    @patch('helper.getMaxTransactionLimit')
    def test_validate_transaction_limit_over_limit(self, mock_getMaxLimit, mock_isMaxLimitAvailable):
        """Test validating transaction limit when amount exceeds the limit."""
        mock_isMaxLimitAvailable.return_value = True
        mock_getMaxLimit.return_value = 100
        amount_value = 150
        helper.validate_transaction_limit(self.chat_id, amount_value, self.bot)
        self.bot.send_message.assert_called_once_with(self.chat_id, 'Warning! You went over your transaction spend limit.')

    @patch('helper.isMaxTransactionLimitAvailable')
    def test_validate_transaction_limit_no_limit_set(self, mock_isMaxLimitAvailable):
        """Test validating transaction limit when no limit is set."""
        mock_isMaxLimitAvailable.return_value = False
        amount_value = 150
        helper.validate_transaction_limit(self.chat_id, amount_value, self.bot)
        self.bot.send_message.assert_not_called()

    # Test 'get_remaining_budget' function
    @patch('helper.getUserData')
    @patch('helper.calculate_total_expenditure')
    def test_get_remaining_budget_with_income(self, mock_calc_total_exp, mock_getUserData):
        """Test getting remaining budget when income is set."""
        mock_getUserData.return_value = {'income': 1000}
        mock_calc_total_exp.return_value = 300
        remaining_budget = helper.get_remaining_budget(self.chat_id, None)
        self.assertEqual(remaining_budget, 700.0)

    @patch('helper.getUserData')
    def test_get_remaining_budget_no_income(self, mock_getUserData):
        """Test getting remaining budget when income is not set."""
        mock_getUserData.return_value = {}
        remaining_budget = helper.get_remaining_budget(self.chat_id, None)
        self.assertEqual(remaining_budget, 0.0)

    # Test 'get_user_preferred_currency' function
    @patch('helper.getUserData')
    def test_get_user_preferred_currency_set(self, mock_getUserData):
        """Test retrieving user's preferred currency when set."""
        mock_getUserData.return_value = {'preferred_currency': 'EUR'}
        currency = helper.get_user_preferred_currency(self.chat_id)
        self.assertEqual(currency, 'EUR')

    @patch('helper.getUserData')
    def test_get_user_preferred_currency_default(self, mock_getUserData):
        """Test retrieving user's preferred currency when not set."""
        mock_getUserData.return_value = {}
        currency = helper.get_user_preferred_currency(self.chat_id)
        self.assertEqual(currency, 'USD')

    # Test 'createNewUserRecord' function
    def test_createNewUserRecord(self):
        """Test creating a new user record."""
        expected_record = {
            'data': [],
            'budget': {
                'overall': None,
                'category': None,
                'max_per_txn_spend': None
            }
        }
        result = helper.createNewUserRecord()
        self.assertEqual(result, expected_record)

    # Additional tests can be added here for other helper functions

if __name__ == '__main__':
    unittest.main()
