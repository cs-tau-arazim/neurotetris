import ann, tetris, generic
import random

if __name__ == '__main__':
    generation_size = generic.generation_size

    unitTime = 30
    minimal_gui = False
    minimal_ai = True

    ai_players_data = generic.init()
    generation = 1

    while True:
        results = []
        seed = 3 #random.randint(1, 100)
        print "Generation #" + str(generation) + ":"
        ai_players = [ann.Ann(ai_players_data[i]) for i in xrange(generation_size)]

        # Play the game for each ai
        for i in xrange(generation_size):
            App = tetris.TetrisApp(ai_players[i], unitTime, minimal_gui, minimal_ai, seed, 50)
            # optional TODO - play 10 games for each AI
            gameRes = App.run()
            # print "Evaluation for AI #" + str(i) + ": " + str(gameRes)
            results.append(gameRes)
        print([int(i) for i in sorted(results)])
        #print results

        # BEST

        if generation % 1 == 0:
            App = tetris.TetrisApp(ai_players[results.index(max(results))], unitTime, True, minimal_ai, seed, 999999)
            res1 = App.run()
            print res1

        result_list = [(ai_players_data[i], results[i]) for i in xrange(generation_size)]
        ai_players_data = generic.generate_new_gen(result_list)
        generation += 1






