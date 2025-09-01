from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import BaseChatMessageHistory
from typing import List
from langchain_core.messages import BaseMessage
from flask import current_app, has_app_context, g

from app.web.api import (
    get_messages_by_conversation_id,
    add_message_to_conversation
)

class SqlMessageHistory(BaseChatMessageHistory):
    def __init__(self, conversation_id: str):
        super().__init__()
        self.conversation_id = conversation_id
        self._app = None
        
        # Try to get the current app instance
        if has_app_context():
            self._app = current_app
            self.messages = get_messages_by_conversation_id(conversation_id)
        else:
            self.messages = []
    
    def add_message(self, message: BaseMessage) -> None:
        # Handle content type conversion
        content = message.content
        if isinstance(content, list):
            content = " ".join(str(item) for item in content)
        
        # Function to add message with proper context
        def _add_to_db():
            add_message_to_conversation(
                conversation_id=self.conversation_id,
                role=message.type,
                content=str(content)
            )
            # Refresh messages after adding
            self.messages = get_messages_by_conversation_id(self.conversation_id)
        
        if has_app_context():
            # We're already in a Flask context
            _add_to_db()
        elif self._app:
            # Use the stored app instance to create context
            with self._app.app_context():
                _add_to_db()
        else:
            # As a fallback, just add to the local messages list
            # This shouldn't happen in normal operation
            self.messages.append(message)

    def clear(self) -> None:
        # Clear would need to be implemented to delete messages from DB
        # For now, just clear the local list
        self.messages = []

def build_memory(chat_args):
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(
            conversation_id=chat_args.conversation_id
        ),
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
