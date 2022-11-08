from typing import Union
import httpx
from requests_oauthlib import OAuth1
from structures import Tweet
from __version__ import __version__, __title__
from stream import Stream

class Client:
    def __init__(self, bearer_token, access_token, access_token_secret, consumer_key, consumer_secret):
        self.bearer_token = bearer_token
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
    
    async def filtered_stream(self):
        return Stream(self)# type: ignore

    async def make_request(self, method, endpoint, params: dict|None=None, json: dict|None=None, oauth: bool=False):
        async with httpx.AsyncClient() as session:
            session.headers['Authorization'] = f'Bearer {self.bearer_token}'
            session.headers['User-Agent'] = f'{__title__}/{__version__}'
            print(session.headers)
            r = await session.request(method, f"https://api.twitter.com/{endpoint}", params=params, json=json)
        return r

    
    async def get_tweet(self, tweet_id: Union[str, int, list[str]], expansions: list[str] | None = None, tweet_fields: list[str] | None = None, user_fields: list[str] | None = None) -> Tweet | tuple[Tweet]:
        if isinstance(tweet_id, str|int):
            tweet_id = [str(tweet_id)]

        params = {
            "ids": ",".join(tweet_id),
            "expansions": "author_id,entities.mentions.username,referenced_tweets.id,referenced_tweets.id.author_id",
            "tweet.fields": "attachments,public_metrics,reply_settings,possibly_sensitive,source"
        }

        if expansions != None:
            params["expansions"] = ",".join(expansions)

        if tweet_fields != None:
            params["tweet.fields"] = ",".join(tweet_fields)

        if user_fields != None:
            params["user.fields"] = ",".join(user_fields)

        response = await self.make_request('GET', '2/tweets', params)

        json = response.json()
        return Tweet.from_json_tweets_end(json)
    
    async def send_tweet(self, text, media_ids: list[str] | None = None, media_paths: str | list[str] | None = None)

    async def delete_tweet(self, tweet_id: Union[str, list[str]]):
        pass