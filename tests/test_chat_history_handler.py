import unittest
from chat_history_handler import ChatHistory

# TestChatHistory class to test the ChatHistory class from chat_history_handler.py
class TestChatHistory(unittest.TestCase):

    # setUp() is called before running each test, initializes a ChatHistory instance for testing purposes
    def setUp(self):
        self.history = ChatHistory()

    # Test whether adding a message to the chat history increases the chat log's length by 1
    def test_add_message(self):
        self.history.add_message("User", "Hello")
        self.assertEqual(len(self.history.chat_log), 1)

    # Test if get_chat_history() retrieves chat history as a list of formatted messages
    def test_get_chat_history(self):
        self.history.add_message("Assistant", "Hi there!")
        formatted_messages = self.history.get_chat_history()
        self.assertTrue(isinstance(formatted_messages, list))

    # Test whether clear_chat_history() clears the chat log and results in a chat log of size zero
    def test_clear_chat_history(self):
        self.history.add_message("User", "Hello")
        self.history.clear_chat_history()
        self.assertEqual(len(self.history.chat_log), 0)

    # Test if get_last_context() with context size 2 correctly gets the last two messages of the chat history
    def test_get_last_context(self):
        self.history.add_message("User", "Hello")
        self.history.add_message("Assistant", "How may I help?")
        last_context = self.history.get_last_context(2)
        is_three_dots = ' '.join(['...'] * 3) in last_context
        self.assertFalse(is_three_dots)
        self.assertIn("User: Hello", last_context)
        self.assertIn("Assistant: How may I help?", last_context)

# Execute the tests using the command line interface
if __name__ == "__main__":
    unittest.main()
