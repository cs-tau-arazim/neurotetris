import ann, tetris, generic, numpy

if __name__ == '__main__':
    generation_size = generic.generation_size

    unitTime = 500
    minimal_gui = False

    matrix = []
    results = []
    ai_players_data = generic.init()
    generation = 1

    while generation < 15:

        print "Generation" + str(generation) + ":"
        ai_players = [ann.Ann(ai_players_data[i]) for i in xrange(generation_size)]

        # Play the game for each ai
        for i in xrange(generation_size):
            App = tetris.TetrisApp(ai_players[i], unitTime, minimal_gui)
            # optional TODO - play 10 games for each AI
            gameRes = App.run()
            # print "Evaluation for AI #" + str(i) + ": " + str(gameRes)
            results.append(gameRes)

        print max(results)

        result_list = [(ai_players_data[i], results[i]) for i in xrange(generation_size)]
        ai_players_data = generic.generate_new_gen(result_list)
        generation += 1






