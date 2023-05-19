# Import the openai library to access its arcane powers
import openai

# Invoke the time library to control the flow of moments
import time

# Summon the logging library to scribe the tales of our adventure
import logging

    import tiktoken
    
    def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo":
            print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
            return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
        elif model == "gpt-4":
            print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
            return num_tokens_from_messages(messages, model="gpt-4-0314")
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|im_start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif model == "gpt-4-0314":
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|im_start|>assistant<|im_sep|>
        return num_tokens
    

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
            MODEL = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Knock knock."},
                    {"role": "assistant", "content": "Who's there?"},
                    {"role": "user", "content": "Orange."},
                ],
                temperature=0,
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred while generating a response."
