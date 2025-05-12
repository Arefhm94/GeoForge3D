from datetime import datetime
import json

class MessagingService:
    def __init__(self):
        self.messages = []

    def send_message(self, message):
        timestamp = datetime.utcnow().isoformat()
        self.messages.append({"timestamp": timestamp, "message": message})
        # Here you could add logic to send the message to a message queue or another service

    def get_messages(self):
        return json.dumps(self.messages)

    def clear_messages(self):
        self.messages = []