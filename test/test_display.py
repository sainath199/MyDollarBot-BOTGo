import os
from unittest.mock import patch, MagicMock
from telebot import types
from code import display
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../code')))
import helper

# Helper function to create a mock mesimport unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
from datetime import datetime

# Adjust sys.path to include the directory where 'display.py' is located
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import display  # Assuming 'display.py' is in the 'code' directory
from telebot import types

def create_message(text, chat_id=12345):
    """Helper function to create a dummy message object."""
    chat = types.Chat(chat_id, 'private')
    from_user = types.User(chat_id, False, 'test_user')
    message = types.Message(
        message_id=1,
        from_user=from_user,
        date=datetime.now(),
        chat=chat,
        content_type='text',
        options={},
        json_string=""
    )
    message.text = text
    return message

class TestDisplayModule(unittest.TestCase):

    def setUp(self):
        self.chat_id = 12345
        self.bot = MagicMock()
        self.message = create_message("Test message", chat_id=self.chat_id)

    @patch('display.helper')
    def test_run_no_history(self, mock_helper):
        """Test the 'run' function when there is no user history."""
        # Mock helper functions
        mock_helper.getUserHistory.return_value = None

        # Call the function
        display.run(self.message, self.bot)

        # Assert that bot.send_message was called with the appropriate message
        self.bot.send_message.assert_called_once_with(self.chat_id, "Sorry, there are no records of the spending!")

    @patch('display.helper')
    def test_run_with_history(self, mock_helper):
        """Test the 'run' function when there is user history."""
        # Mock helper functions
        mock_helper.getUserHistory.return_value = ['History data']
        mock_helper.getSpendCategories.return_value = ['Food', 'Transport']

        # Call the function
        display.run(self.message, self.bot)

        # Assert that bot.reply_to was called to prompt for category selection
        self.bot.reply_to.assert_called_once()
        args, kwargs = self.bot.reply_to.call_args
        self.assertIn('Please select a category to see details', args[1])

    @patch('display.helper')
    def test_select_period(self, mock_helper):
        """Test the 'select_period' function."""
        # Mock message with selected category
        message = create_message('Food', chat_id=self.chat_id)

        # Call the function
        display.select_period(message, self.bot)

        # Assert that bot.send_message was called to confirm category selection
        self.bot.send_message.assert_any_call(self.chat_id, 'You selected Food. Now please select a time period (Day or Month).')

        # Assert that bot.reply_to was called to prompt for period selection
        self.bot.reply_to.assert_called()
        args, kwargs = self.bot.reply_to.call_args
        self.assertIn('Please select a period to see the spending details.', args[1])

    @patch('display.helper')
    def test_display_total_no_spending(self, mock_helper):
        """Test 'display_total' when there are no expenses in the selected period and category."""
        # Set up the helper functions
        mock_helper.getSpendDisplayOptions.return_value = ['Day', 'Month']
        mock_helper.getUserHistory.return_value = ['01-Jan-2022,Food,100,USD']
        mock_helper.getDateFormat.return_value = '%d-%b-%Y'
        mock_helper.getMonthFormat.return_value = '%b-%Y'
        mock_helper.get_user_preferred_currency.return_value = 'USD'
        mock_helper.getOverallRemainingBudget.return_value = 1000
        mock_helper.get_remaining_budget.return_value = 900

        # Create a message with an invalid period
        message = create_message('Year', chat_id=self.chat_id)

        # Call the function
        display.display_total(message, self.bot, 'Food')

        # Assert that bot.reply_to was called with the appropriate error message
        self.bot.reply_to.assert_called_once()
        args, kwargs = self.bot.reply_to.call_args
        self.assertIn("Sorry I can't show spendings for", args[1])

    @patch('display.helper')
    def test_display_total_with_spending(self, mock_helper):
        """Test 'display_total' when there are expenses in the selected period and category."""
        # Set up the helper functions
        mock_helper.getSpendDisplayOptions.return_value = ['Day', 'Month']
        current_month_str = datetime.now().strftime('%b-%Y')
        current_date_str = datetime.now().strftime('%d-%b-%Y')
        mock_helper.getUserHistory.return_value = [f'{current_date_str},Food,100,USD']
        mock_helper.getDateFormat.return_value = '%d-%b-%Y'
        mock_helper.getMonthFormat.return_value = '%b-%Y'
        mock_helper.get_user_preferred_currency.return_value = 'USD'
        mock_helper.getCategoryBudgetByCategory.return_value = 500
        mock_helper.getOverallBudget.return_value = 1000
        mock_helper.get_remaining_budget.return_value = 900
        mock_helper.getplot.return_value = ['Bar with budget', 'Pie', 'Bar without budget']

        # Create a message with 'Month' as the period
        message = create_message('Month', chat_id=self.chat_id)

        # Mock 'calculate_spendings' function
        display.calculate_spendings = MagicMock(return_value='Food 100.00 USD\n')

        # Call the function
        display.display_total(message, self.bot, 'Food')

        # Assert that bot.send_message was called to show spendings
        self.bot.send_message.assert_any_call(
            self.chat_id,
            f'Here are your total spendings for Food in month:\nCATEGORIES, AMOUNT \n----------------------\nFood 100.00 USD\n'
        )

        # Assert that bot.send_message was called to show remaining amount
        self.bot.send_message.assert_any_call(
            self.chat_id,
            'Remaining Amount: $900.00'
        )

        # Assert that bot.reply_to was called to prompt for plot selection
        self.bot.reply_to.assert_called()
        args, kwargs = self.bot.reply_to.call_args
        self.assertIn('Please select a plot to see the total expense', args[1])

    @patch('display.helper')
    @patch('display.graphing')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove')
    def test_plot_total_bar_with_budget(self, mock_remove, mock_file_open, mock_graphing, mock_helper):
        """Test 'plot_total' when 'Bar with budget' is selected."""
        # Set up the helper functions
        mock_helper.getUserHistory.return_value = ['01-Jan-2022,Food,100,USD']

        # Set global variables
        display.total = 'Food 100.00 USD\n'
        display.bud = 500

        # Create a message with 'Bar with budget' as the selection
        message = create_message('Bar with budget', chat_id=self.chat_id)

        # Mock 'visualize' function
        mock_graphing.visualize.return_value = None

        # Call the function
        display.plot_total(message, self.bot)

        # Assert that 'visualize' was called
        mock_graphing.visualize.assert_called_once_with('Food 100.00 USD\n', 500)

        # Assert that bot.send_photo was called
        self.bot.send_photo.assert_called_once()

        # Assert that 'open' was called with 'expenditure.png'
        mock_file_open.assert_called_with('expenditure.png', 'rb')

        # Assert that 'os.remove' was called with 'expenditure.png'
        mock_remove.assert_called_with('expenditure.png')

    @patch('display.helper')
    @patch('display.graphing')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove')
    def test_plot_total_pie_chart(self, mock_remove, mock_file_open, mock_graphing, mock_helper):
        """Test 'plot_total' when 'Pie' is selected."""
        # Set up the helper functions
        mock_helper.getUserHistory.return_value = ['01-Jan-2022,Food,100,USD']

        # Set global variables
        display.total = 'Food 100.00 USD\n'

        # Create a message with 'Pie' as the selection
        message = create_message('Pie', chat_id=self.chat_id)

        # Mock 'vis' function
        mock_graphing.vis.return_value = None

        # Call the function
        display.plot_total(message, self.bot)

        # Assert that 'vis' was called
        mock_graphing.vis.assert_called_once_with('Food 100.00 USD\n')

        # Assert that bot.send_photo was called
        self.bot.send_photo.assert_called_once()

        # Assert that 'open' was called with 'pie.png'
        mock_file_open.assert_called_with('pie.png', 'rb')

        # Assert that 'os.remove' was called with 'pie.png'
        mock_remove.assert_called_with('pie.png')

    @patch('display.helper')
    def test_calculate_spendings(self, mock_helper):
        """Test 'calculate_spendings' function."""
        # Set up the helper functions
        mock_helper.convert_currency.side_effect = lambda amount, from_currency, to_currency: amount

        # Sample query result
        queryResult = [
            '01-Jan-2022,Food,100,USD',
            '01-Jan-2022,Transport,50,USD',
            '01-Jan-2022,Food,25,USD'
        ]

        # Call the function
        total_text = display.calculate_spendings(queryResult, 'USD')

        # Expected result
        expected_text = 'Food 125.00 USD\nTransport 50.00 USD\n'

        self.assertEqual(total_text, expected_text)

if __name__ == '__main__':
    unittest.main()
sage object
def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(894127939, None, None, chat, 'text', params, "")

# Setup function for mocking telebot to pass all tests
def setup_telebot_mocks(mock_telebot):
    mc = mock_telebot.return_value
    mc.reply_to = MagicMock()
    mc.send_message = MagicMock()
    return mc


