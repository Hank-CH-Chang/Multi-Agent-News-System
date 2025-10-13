
from pydantic import BaseModel, Field
from typing import Optional
import time
import uuid

class NewsArticle(BaseModel):
    """
    Represents a single, structured news article.
    This data structure is used for communication between agents and for final storage.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    url: str
    source: Optional[str] = None
    summary: Optional[str] = "Not summarized."
    category: Optional[str] = "Uncategorized."
    popularity: int = Field(default=0, description="A score from 0 to 100 indicating popularity.")
    image: Optional[str] = Field(default=None, description="URL of the article's main image.")
    timestamp: float = Field(default_factory=time.time)

