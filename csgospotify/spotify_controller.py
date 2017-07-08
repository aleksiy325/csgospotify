from urllib.request import urlopen, Request
from urllib.error import HTTPError 
from string import ascii_lowercase
from random import choice
from urllib import parse
import json

# Inspired by http://cgbystrom.com/articles/deconstructing-spotifys-builtin-http-server/
ORIGIN_HEADER = {'Origin': 'https://open.spotify.com'}

class SpotifyController(object):

    def __init__(self):
        self.get_port()
        self.oauth_token = self.get_oauth_token()
        self.csrf_token = self.get_csrf_token()

    def get_port(self):
        for self.port in range(4370, 4380):
            try:
                response = self.get_version()
                return 
            except Exception as e:
                self.port += 1

        raise RuntimeError("Could not find Spotify port. Is Spotify running?")

    def generate_local_hostname(self):
        """Generate a random hostname under the .spotilocal.com domain"""
        subdomain = ''.join(choice(ascii_lowercase) for x in range(10))
        return subdomain + '.spotilocal.com'

    def get_url(self, url):
        return "https://%s:%d%s" % (self.generate_local_hostname(), self.port, url)

    def get_json(self, url, params={}, headers={}):
        if params:
            url += "?" + parse.urlencode(params)
        request = Request(url, headers=headers)
        return json.loads(urlopen(request).read().decode('utf8'))

    def get_oauth_token(self):
        return self.get_json('http://open.spotify.com/token')['t']

    def get_csrf_token(self):
        # Requires Origin header to be set to generate the CSRF token.
        res = self.get_json(self.get_url('/simplecsrf/token.json'), headers=ORIGIN_HEADER)
        if 'error' in res:
            raise RuntimeError('Spotify: ' + res['error']['message'])
        return res['token']

    def get_version(self):
        return self.get_json(self.get_url('/service/version.json'), params={'service': 'remote'}, headers=ORIGIN_HEADER)

    def get_status(self):
        params = {
            'oauth': self.oauth_token,
            'csrf': self.csrf_token,
        }
        return self.get_json(self.get_url('/remote/status.json'), params=params, headers=ORIGIN_HEADER)

    def is_playing(self):
        return self.get_status()['playing']

    def pause(self, pause=True):
        params = {
            'oauth': self.oauth_token,
            'csrf': self.csrf_token,
            'pause': 'true' if pause else 'false'
        }
        self.get_json(self.get_url('/remote/pause.json'),
                      params=params, headers=ORIGIN_HEADER)

    def unpause(self):
        self.pause(pause=False)

    def play(spotify_uri):
        params = {
            'oauth': self.oauth_token,
            'csrf': self.csrf_token, 
            'uri': spotify_uri,
            'context': spotify_uri,
        }
        self.get_json(self.get_url('/remote/play.json'),
                      params=params, headers=ORIGIN_HEADER)
