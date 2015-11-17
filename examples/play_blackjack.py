from blackjack.blackjack import Blackjack

# Automated playing using `battle_bot`. Change `num_cycles` for the games to play
# and `num_decks` for the number of decks to use in each cycle. This script is running
# 1000 cycles using 6 decks.

score = (0, 0, 0, 0)
num_cycles = 1000
num_decks = 6
for i in range(num_cycles):
    game = Blackjack(num_decks).play(use_battle_bot=True)
    score = tuple([x + y for x, y in zip(score, game)])
    games, draws, player_win, computer_win = score
    print('Player win = {}'.format(player_win))
    print('Computer win = {}'.format(computer_win))
    print('Number of games = {}'.format(games))
    print('Draws = {}'.format(draws))
    try:
        print('Win/Loss = {:.2f}'.format(player_win / computer_win))
    except:
        print('Win/Loss = {}'.format(max(player_win, computer_win)))
    print('\n--------------------\n')


# # Play a normal game using 4 decks and shuffling 6 times on startup

num_decks = 4
num_shuffles = 6
Blackjack(num_decks, num_shuffles).play()
