from typing import List
from langgraph.graph import MessagesState
from uuid import UUID
from langchain_core.documents import Document

class RagState(MessagesState):
    """Messages are auto-accumulated from the MessageState base class."""
    user_id : UUID
    documents: List[Document]

class ConversationState(RagState):
    """Schema for multi-conversations per user paradigm."""
    conversation_id : UUID

class RoutingState(RagState):
    decision: str