from csgo_state import GameStateServer, GameStateRequestHandler
from winreg import ConnectRegistry, OpenKey, QueryValueEx, HKEY_CURRENT_USER
import time
import sys

# TODO: auto insert config

def get_csgo_path():
	Registry = ConnectRegistry(None, HKEY_CURRENT_USER)
	key = OpenKey(Registry, "Software\Valve\Steam")
	path = QueryValueEx(key, "SteamPath")
	return path[0]

if __name__ == '__main__':
    server = GameStateServer(('localhost', 3000), GameStateRequestHandler)
    server.init_state()

    print(time.asctime(), '-', 'CS:GO Spotify server starting')

    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

    server.server_close()
    print(time.asctime(), '-', 'CS:GO Spotify server stopped')