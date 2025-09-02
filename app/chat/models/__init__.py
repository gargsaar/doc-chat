from pydantic import BaseModel, ConfigDict
from typing import Optional


class RetrievalConfig(BaseModel):
    """Configuration for document retrieval"""
    model_config = ConfigDict(extra='allow')
    
    k: int = 10  # Number of documents to retrieve
    search_type: str = "similarity"  # Search strategy
    
    @classmethod
    def create_comprehensive(cls) -> "RetrievalConfig":
        """Config optimized for comprehensive answers (lists, overviews)"""
        return cls(k=15, search_type="similarity")
    
    @classmethod
    def create_focused(cls) -> "RetrievalConfig":
        """Config optimized for focused, specific answers"""
        return cls(k=6, search_type="similarity")
    
    @classmethod
    def create_balanced(cls) -> "RetrievalConfig":
        """Default balanced configuration"""
        return cls(k=10, search_type="similarity")


class Metadata(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    conversation_id: str
    user_id: str
    pdf_id: str


class ChatArgs(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    conversation_id: str
    pdf_id: str
    metadata: Metadata
    streaming: bool
    retrieval_config: Optional[RetrievalConfig] = None
    
    def get_retrieval_config(self) -> RetrievalConfig:
        """Get retrieval config with sensible defaults"""
        if self.retrieval_config:
            return self.retrieval_config
        
        # Default to balanced retrieval
        return RetrievalConfig.create_balanced()
