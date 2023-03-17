import datetime

class Message:
    def __init__(self, sender, message):
        self.sender = sender
        self.message = message
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def formatted_message(self):
        return f"{self.timestamp} - {self.sender}: {self.message}"


class ChatHistory:
    def __init__(self):
        self.chat_log = []

    def add_message(self, sender, message):
        self.chat_log.append(Message(sender, message))

    def get_chat_history(self):
        return [message.formatted_message() for message in self.chat_log]

    def clear_chat_history(self):
        self.chat_log.clear()

    def get_last_context(self, num_messages=3):
        context_messages = self.chat_log[-num_messages:] if len(self.chat_log) >= num_messages else self.chat_log
        return ' '.join(message.formatted_message() for message in context_messages)


class Chat:
    def __init__(self, name):
        self.name = name
        self.chat_history = ChatHistory()

    def send_message(self, sender, message):
        self.chat_history.add_message(sender, message)

    def get_context(self, num_messages=3):
        return self.chat_history.get_last_context(num_messages=num_messages)

    def clear_chat(self):
        self.chat_history.clear_chat_history()

    def __repr__(self):
        return f"Chat('{self.name}')"

    def __str__(self):
        return f"{self.name}"

