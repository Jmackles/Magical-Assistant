import os
import unittest
from openai_integration import OpenAIIntegration

class TestOpenAIIntegration(unittest.TestCase):

    def setUp(self):
        api_key = os.environ.get("OPENAI_TOKEN")
        self.openai_integration = OpenAIIntegration(api_key)

    def test_generate_chatbot_response(self):
        user_message = "What is the capital of France?"
        last_context = ""
        response = self.openai_integration.generate_chatbot_response(user_message, last_context)
        self.assertIsNotNone(response, msg="The generated chatbot response should not be None.")
        self.assertNotEqual(response.strip(), "", msg="The generated chatbot response should not be an empty string.")

if __name__ == '__main__':
    unittest.main()
