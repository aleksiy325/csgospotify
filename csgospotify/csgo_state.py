import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from spotify_controller import SpotifyController


class GameState(object):

    def __init__(self, payload):
        self.game_state = json.loads(payload)

    def is_player(self):
        return self.game_state['provider']['steamid'] == self.game_state['player']['steamid']

    def is_playing(self):
        return self.game_state['player']['activity'] == 'playing'

    def game_is_live(self):
        return self.game_state['map']['phase'] == 'live'

    def is_alive(self):
        return self.game_state['player']['state']['health'] > 0

    def is_competitive(self):
        return self.game_state['map']['mode'] == 'competitive'

    def is_freezetime(self):
        return self.game_state['round']['phase'] == 'freezetime'

    def no_music(self):
        return self.is_playing() and self.is_competitive() and self.game_is_live() and self.is_player() and self.is_alive() and not self.is_freezetime()


class GameStateServer(HTTPServer):

    def init_state(self):
        self.spotify = SpotifyController()


class GameStateRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        game_state = GameState(body)
        self.control_music(game_state)
        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    def control_music(self, game_state):
        if game_state.no_music():
            if self.server.spotify.is_playing():
                self.server.spotify.pause()
                print("Pausing music")
        elif not self.server.spotify.is_playing():
            self.server.spotify.unpause()
            print("Unpausing music")

    def log_message(self, format, *args):
        """
        Prevents requests from printing into the console
        """
        return
