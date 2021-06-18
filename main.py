

if __name__ == "__main__":
    from Game import Game
    from Player import Player
    from util import POSITIONS

    game_w = 1000
    game_h = 800

    app = Game((game_w, game_h))
    player = Player(app, (game_w//2-POSITIONS["player"][2], game_h-100))

    app.run()
