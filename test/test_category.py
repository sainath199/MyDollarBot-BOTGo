import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import sys
import os

# Adjust sys.path to include the directory where 'category.py' is located
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))

import category  # Assuming 'category.py' is in the 'code' directory
from telebot import types

def create_message(text, chat_id=11):
    """Helper function to create a dummy message object"""
    params = {'messagebody': text}
    chat = types.User(chat_id, False, 'test')
    message = types.Message(1, None, None, chat, 'text', params, "")
    message.text = text
    return message

class TestCategoryModule(unittest.TestCase):

    def setUp(self):
        self.chat_id = 12345
        self.bot = MagicMock()
        self.message = create_message("Test message", chat_id=self.chat_id)

    @patch('category.helper')
    def test_run(self, mock_helper):
        # ... (no changes needed here)
        pass

    # ... (other test methods)

    @patch('category.helper')
    def test_post_operation_selection_delete_single_category(self, mock_helper):
        # ... (no changes needed here)
        pass

    @patch('category.helper')
    def test_post_operation_selection_invalid(self, mock_helper):
        # ... (no changes needed here)
        pass

    def test_category_add_empty_file(self):
        """Test 'category_add' when categories.txt is initially empty."""
        m_open = mock_open(read_data='')

        with patch('builtins.open', m_open):
            # Set message text to the new category name
            self.message.text = 'NewCategory'

            # Call the function
            category.category_add(self.message, self.bot)

            # Assert that bot.send_message was called with confirmation message
            self.bot.send_message.assert_called_with(self.chat_id, 'Add category "NewCategory" successfully!')

            # Check that open was called correctly
            expected_calls = [call('categories.txt', 'r'), call('categories.txt', 'a')]
            self.assertEqual(m_open.call_args_list, expected_calls)

            # Check that the new category was written to the file
            handle = m_open()
            handle.write.assert_called_with('NewCategory')

    def test_category_add_non_empty_file(self):
        """Test 'category_add' when categories.txt has existing categories."""
        m_open_read = mock_open(read_data='Food,Transport')
        m_open_append = mock_open()

        # Side effect to return different mocks based on the mode
        def open_side_effect(file, mode):
            if file == 'categories.txt' and mode == 'r':
                return m_open_read()
            elif file == 'categories.txt' and mode == 'a':
                return m_open_append()
            else:
                raise ValueError("Unrecognized file/mode combination: {} {}".format(file, mode))

        with patch('builtins.open', side_effect=open_side_effect) as mock_file:
            # Set message text to the new category name
            self.message.text = 'NewCategory'

            # Call the function
            category.category_add(self.message, self.bot)

            # Assert that bot.send_message was called with confirmation message
            self.bot.send_message.assert_called_with(self.chat_id, 'Add category "NewCategory" successfully!')

            # Check that open was called correctly
            expected_calls = [call('categories.txt', 'r'), call('categories.txt', 'a')]
            mock_file.assert_has_calls(expected_calls, any_order=False)

            # Check that the new category was written to the file
            m_open_append().write.assert_called_with(',NewCategory')

    def test_category_delete_existing(self):
        """Test 'category_delete' when the category exists."""
        m_open_read = mock_open(read_data='Food,Transport,NewCategory')
        m_open_write = mock_open()

        # Side effect to return different mocks based on the mode
        def open_side_effect(file, mode):
            if file == 'categories.txt' and mode == 'r':
                return m_open_read()
            elif file == 'categories.txt' and mode == 'w':
                return m_open_write()
            else:
                raise ValueError("Unrecognized file/mode combination: {} {}".format(file, mode))

        with patch('builtins.open', side_effect=open_side_effect) as mock_file:
            # Set message text to the category to delete
            self.message.text = 'Transport'

            # Call the function
            category.category_delete(self.message, self.bot)

            # Assert that bot.send_message was called with confirmation message
            self.bot.send_message.assert_called_with(self.chat_id, 'Delete category "Transport" successfully!')

            # Check that open was called correctly
            expected_calls = [call('categories.txt', 'r'), call('categories.txt', 'w')]
            mock_file.assert_has_calls(expected_calls, any_order=False)

            # Check that the categories were written back to the file without the deleted one
            handle = m_open_write()
            expected_write_calls = [call.write('Food'), call.write(',NewCategory')]
            handle.assert_has_calls(expected_write_calls, any_order=False)

    def test_category_delete_nonexistent(self):
        """Test 'category_delete' when the category does not exist."""
        # ... (no changes needed here)
        pass

    def test_category_delete_empty_file(self):
        """Test 'category_delete' when categories.txt is empty."""
        # ... (no changes needed here)
        pass

    # ... (other test methods)

if __name__ == '__main__':
    unittest.main()
