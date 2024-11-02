import os
from unittest.mock import patch, MagicMock
from telebot import types
from code import display
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../code')))
import helper

# Helper function to create a mock message object
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

