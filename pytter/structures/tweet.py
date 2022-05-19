from .. import exceptions
from .author import Author


class Tweet:
    def __init__(self, id: int, author: Author, content: str, in_reply_to:int = None, api:int = None, media: int = None, poll: int = None):
        self.author = author
        self.id = id
        self.content = content
        self.in_reply_to = in_reply_to
        self.media = media
        self.poll = poll
        self.api = api
    
    @property
    def from_user(self):
        if not self.api:
            raise exceptions.ApiNotLinked("Cannot check if tweet is from the same client since there is not API linked.")
    
    def delete(self):
        return