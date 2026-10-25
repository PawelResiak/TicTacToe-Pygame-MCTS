from game import Game


if __name__ == '__main__':
    game_on = True
    while game_on:
        new_game = Game()
        game_on = new_game.start()
