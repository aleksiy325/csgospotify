from csgo_state import GameStateServer, GameStateRequestHandler
import time
import sys

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