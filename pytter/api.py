import re
import requests
from requests_oauthlib import OAuth1


from pytter.tweet import Tweet


class ApiInterface:
    def __init__(self, bearer_token, access_token, access_token_secret, consumer_key, consumer_secret):
        self.bearer_token = bearer_token
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret


    def get_auth(self):
        return OAuth1(
            self.consumer_key, client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret, decoding=None
        )

    def get_session(self, oauth=False) -> requests.Session:
        session = requests.Session()
        session.headers['Authorization'] = f'Bearer {self.bearer_token}'
        return session

    def request_fabric(self, method, endpoint, params={}, session=None, json=None, oauth=False):
        # Get session
        session = self.get_session(oauth) if not session else session
        # Make the HTTP request using the session
        req = session.request(method, "https://api.twitter.com"+endpoint, params=params, json=json, auth=self.get_auth() if oauth else None)
        # Match the request's response status code.
        match req.status_code:
            # TODO: Parsing with the No Content and OK status codes.
            case 201 | 200:
                return req
            # TODO: Implement exceptions for 400 codes.
            case _:
                raise Exception(f"Placeholder — Failed to make request (code {req.status_code})")


class TwitterAPI(ApiInterface):
    def get_webhooks(self):
        return

