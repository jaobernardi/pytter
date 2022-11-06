from datetime import datetime
from typing import Any, Type
from .user import User
from dataclasses import dataclass, field

@dataclass
class Tweet:
    id: str
    edit_history_tweet_ids: tuple[str]
    text: str
    author: User | None = None
    full_json: dict | None = field(default_factory=lambda: None,repr=False)
    json: dict | None = field(default_factory=lambda: None,repr=False)
    mentions: tuple[User] | None = None
    quoted_tweets: tuple[Any] | None = None
    replied_to: tuple[Any] | None = None
    media_keys: tuple[str] | None = None
    polls: tuple[str] | None = None
    annotations: tuple[dict] | None = None
    cashtags: tuple[dict] | None = None
    hashtags: tuple[dict] | None = None
    
    @classmethod
    def create_from_json(cls, tweet_json, _users: dict[str, User], _ref_tweets: dict[str, Any] | None = None, **any):
        mentions = tuple()
        if 'entities' in tweet_json and 'mentions' in tweet_json['entities']:
            mentions = tuple([_users[i['id']] for i in tweet_json['entities']['mentions'] if i['id'] in _users])

        return cls(
            id=tweet_json['id'],
            edit_history_tweet_ids=tuple(tweet_json['edit_history_tweet_ids']),
            text=tweet_json['text'],
            author=_users[tweet_json['author_id']] if 'author_id' in tweet_json and tweet_json['author_id'] in _users else None,
            json=tweet_json,
            mentions=mentions,
            quoted_tweets=tuple([_ref_tweets[i['id']] for i in tweet_json['referenced_tweets'] if i['type'] == 'quoted']) if 'referenced_tweets' in tweet_json and _ref_tweets else tuple(),
            replied_to=tuple([_ref_tweets[i['id']] for i in tweet_json['referenced_tweets'] if i['type'] == 'replied_to']) if 'referenced_tweets' in tweet_json and _ref_tweets else tuple(),
            media_keys = tuple([]) if 'attachments' in tweet_json and 'media_keys' in tweet_json['attachments'] else tuple(),
            **any
        )

    @classmethod
    def from_json_tweets_end(cls, json: dict[Any, Any]):
        """
        Parse the output from `/2/tweets` endpoint
        """
        # Instanciate the Users and Referenced Tweets
        _users = {i['id']: User(**i) for i in (json['includes']['users'] if 'includes' in json and 'users' in json['includes'] else [])}
        _ref_tweets = {i['id']: cls.create_from_json(i, _users) for i in (json['includes']['tweets'] if 'includes' in json and 'tweets' in json['includes'] else [])}

        tweets = []

        assert 'data' in json
        for tweet in json['data']:
            tweets.append(cls.create_from_json(tweet, _users, _ref_tweets, full_json=json))
        # Return either the list or the single tweet
        return tuple(tweets) if len(tweets) > 1 else tweets[0]


