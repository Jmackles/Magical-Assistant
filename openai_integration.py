# Import the openai library to access its arcane powers
import openai

# Invoke the time library to control the flow of moments
import time

# Summon the logging library to scribe the tales of our adventure
import logging

# Declare the enchanted OpenAIIntegration class
class OpenAIIntegration:
    # Construct the class with the mystical API key
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    # Generate a chatbot response using the OpenAI API
    def generate_chatbot_response(self, prompt, last_context):
        # Combine user prompt and conversation history
        full_prompt = f"{last_context}\nUser: {prompt}\nAssistant:"
        
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=full_prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.5,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred while generating a response."
