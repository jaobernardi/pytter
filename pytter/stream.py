import json
import httpx
from dataclasses import dataclass, field
from typing import Any
from __version__ import __version__, __title__
from structures import Tweet


@dataclass
class Stream:
    client: Any
    endpoint: str = 'https://api.twitter.com/2/tweets/search/stream'
    rules: dict[str, list[dict[str, str]]] = field(default_factory={'add': []}.copy)

    async def connect(self, expansions: list[str] | None = None, tweet_fields: list[str] | None = None, user_fields: list[str] | None = None):
        params = {
            "expansions": "author_id,entities.mentions.username,referenced_tweets.id,referenced_tweets.id.author_id",
            "tweet.fields": "attachments,public_metrics,reply_settings,possibly_sensitive,source"
        }

        if expansions != None:
            params["expansions"] = ",".join(expansions)

        if tweet_fields != None:
            params["tweet.fields"] = ",".join(tweet_fields)

        if user_fields != None:
            params["user.fields"] = ",".join(user_fields)

        session = httpx.AsyncClient()
        session.headers['Authorization'] = f'Bearer {self.client.bearer_token}'
        session.headers['User-Agent'] = f'{__title__}/{__version__}'
        await self.clear_rules()
        await session.post(f'{self.endpoint}/rules', json=self.rules)
        
        async with session.stream('GET', self.endpoint, params=params) as response:
            async for chunk in response.aiter_lines():
                try:
                    tweet_json = json.loads(chunk)
                    tweet = Tweet.from_json_tweets_end(tweet_json)
                    await self.on_tweet(tweet)   # type: ignore
                except:
                    print(f'failed to parse json: {chunk!r}')

    def add_rule(self, rule, rule_name):
        self.rules['add'].append({'value': rule, 'tag': rule_name})

    async def clear_rules(self):
        rules = await self.get_rules()
        if not rules: return
        r: httpx.Response = await self.client.make_request('POST', f'2/tweets/search/stream/rules', json={'delete': {'ids': [i['id'] for i in rules]}})
        assert r.status_code == 200, f'Failed to clear stream rules. (http {r.status_code})'

    async def get_rules(self):
        r: httpx.Response = await self.client.make_request('GET', f'2/tweets/search/stream/rules')
        assert r.status_code == 200, f'Failed to get stream rules. (http {r.status_code})'
        j = r.json()
        return j['data'] if 'data' in j else []
    
    async def on_tweet(self, tweet: Tweet):
        pass
