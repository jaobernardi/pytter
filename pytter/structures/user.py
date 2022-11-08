from typing import Any
from datetime import datetime
from dataclasses import dataclass

@dataclass
class User:
    id: str|int
    username: str
    name: str
    created_at: datetime | None = None
    description: str | None = None
    location: str | None = None
    pinned_tweet_id: str | None = None
    pinned_tweet: Any | None = None
    
    @classmethod
    def create_from_json(cls, json):
        # TODO: Implement stuff correctly
        return cls(**json)