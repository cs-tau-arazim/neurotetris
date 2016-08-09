import ann, tetris

if __name__ == '__main__':
    matrix = []
    player_ai = ann.Ann(matrix)
    App = tetris.TetrisApp(player_ai)

    App.run()


