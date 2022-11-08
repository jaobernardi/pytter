from .user import User
from datetime import datetime
from typing import Any, Type
from dataclasses import dataclass, field
from aenum import MultiValueEnum

class ReplySettings(MultiValueEnum):
    EVERYONE = 'everyone'
    MENTIONED_USERS = 'mentioned_users', 'mentionedUsers'
    FOLLOWERS = 'followers' # Mentioned in the user fields doc page
    FOLLOWING = 'following'

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
    media_keys_ids: tuple[str] | None = None
    polls: tuple[str] | None = None
    annotations: tuple[dict] | None = None
    cashtags: tuple[dict] | None = None
    hashtags: tuple[dict] | None = None
    retweet_count: int | None = None
    like_count: int | None = None
    reply_count: int | None = None
    quote_count: int | None = None
    reply_settings: ReplySettings | None = None
    source: str | None = None
    possibly_sensitive: bool | None = None

    @classmethod
    def create_from_json(cls, tweet_json, _users: dict[str, User], _ref_tweets: dict[str, Any] | None = None, **any):
        mentions = tuple()
        if 'entities' in tweet_json and 'mentions' in tweet_json['entities']:
            mentions = tuple([_users[i['id']] for i in tweet_json['entities']['mentions'] if i['id'] in _users])

        return cls(
            id = tweet_json['id'],
            edit_history_tweet_ids = tuple(tweet_json['edit_history_tweet_ids']),
            text = tweet_json['text'],
            author = _users[tweet_json['author_id']] if 'author_id' in tweet_json and tweet_json['author_id'] in _users else None,
            json = tweet_json,
            mentions = mentions,
            quoted_tweets = tuple([_ref_tweets[i['id']] for i in tweet_json['referenced_tweets'] if i['type'] == 'quoted']) if 'referenced_tweets' in tweet_json and _ref_tweets else tuple(),
            replied_to = tuple([_ref_tweets[i['id']] for i in tweet_json['referenced_tweets'] if i['type'] == 'replied_to']) if 'referenced_tweets' in tweet_json and _ref_tweets else tuple(),
            media_keys_ids = tuple(tweet_json['attachments']['media_keys']) if 'attachments' in tweet_json and 'media_keys' in tweet_json['attachments'] else tuple(),
            reply_settings = ReplySettings(tweet_json['reply_settings']) if 'reply_settings' in tweet_json else None,
            source=tweet_json['source'] if 'source' in tweet_json else None,
            possibly_sensitive=tweet_json['possibly_sensitive'] if 'possibly_sensitive' in tweet_json else None,
            **(tweet_json['public_metrics'] if 'public_metrics' in tweet_json else {}),
            **any
        )

    @classmethod
    def from_json_tweets_end(cls, json: dict[Any, Any]):
        """
        Parse the output from `/2/tweets` endpoint
        """
        # Instanciate the Users and Referenced Tweets
        _users = {i['id']: User.create_from_json(i) for i in (json['includes']['users'] if 'includes' in json and 'users' in json['includes'] else [])}
        _ref_tweets = {i['id']: cls.create_from_json(i, _users) for i in (json['includes']['tweets'] if 'includes' in json and 'tweets' in json['includes'] else [])}

        tweets = []

        assert 'data' in json
        if isinstance(json['data'], dict):
            json['data'] = [json['data']]

        for tweet in json['data']:
            tweets.append(cls.create_from_json(tweet, _users, _ref_tweets, full_json=json))
        # Return either the list or the single tweet
        return tuple(tweets) if len(tweets) > 1 else tweets[0]
