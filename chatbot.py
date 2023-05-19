# Import necessary Flask components for our magical web application
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
load_dotenv()
# Import the enchanted ChatHistory and OpenAIIntegration classes from their respective modules
from chat_history_handler import ChatHistory
from openai_integration import OpenAIIntegration

# Summon the os library to harness the power of environment variables
import os

# Create a Flask app and initialize ChatHistory and OpenAIIntegration instances
app = Flask(__name__)
chat_history = ChatHistory()

# Check if the OPENAI_API_KEY is set, raise an informative error if not
api_key = os.environ.get("OPENAI_TOKEN")
if api_key is None:
    raise ValueError("OPENAI_TOKEN environment variable not set. Please provide the API key.")
openai_integration = OpenAIIntegration(api_key)

# Define the route for the index page
@app.route("/")
def index():
    # Render the index.html template with the chat history
    return render_template("index.html", chat_history=chat_history.get_chat_history())

# Define the route for processing chat messages
@app.route("/chat", methods=["POST"])
def chat():
    # Extract the user's message from the form submission
    user_message = request.form["message"]

    # Add the user's message to the chat history
    chat_history.add_message("User", user_message)

    # Retrieve the last context from the chat history
    last_context = chat_history.get_last_context()

    # Generate the chatbot's response based on the user message and the last context
    assistant_message = openai_integration.generate_chatbot_response(user_message, last_context)

    # Add the chatbot's response to the chat history
    chat_history.add_message("Assistant", assistant_message)

    # Redirect back to the index page
    return redirect(url_for("index"))

# Run the Flask app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
