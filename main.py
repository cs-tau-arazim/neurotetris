import ann, tetris, generic, numpy

if __name__ == '__main__':
    #generation_size = generic.generation_size
    generation_size = 3

    matrix = []
    results = []
    ai_players_data = generic.init()
    generation = 1

    while generation < 5:
        print "Generation" + str(generation) + ":"
        ai_players = [ann.Ann(ai_players_data[i]) for i in range(generation_size)]

        # Play the game for each ai
        for i in xrange(generation_size):
            App = tetris.TetrisApp(ai_players[i])
            # optional TODO - play 10 games for each AI
            results.append(App.run())

        result_list = [(ai_players_data[i], results[i]) for i in xrange(generation_size)]
        ai_players_data = generic.generate_new_gen(result_list)
        generation += 1




