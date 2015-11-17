# What is blackjack?
`blackjack` contains a python version of Blackjack as well as tools for card counting and a bot called `battle_bot` which plays Blackjack using basic strategy. This allows the ability to test large amount of games and strategies.

# Example scripts
### Using `battle_bot`
Automated playing using `battle_bot`. `num_cycles` determines the number of full games to play and `num_decks` determines the number of decks used in each cycle. This script is running 1000 cycles using 6 decks.
```
from blackjack import Blackjack

score = (0, 0, 0, 0)
num_cycles = 1000
num_decks = 6
for i in range(num_cycles):
    game = Blackjack(num_decks).play(battle_bot=True)
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

```

##### Output:

```
Player win = 23127
Computer win = 25454
Number of games = 52907
Draws = 4326
Win/Loss = 0.91

--------------------

Player win = 23152
Computer win = 25475
Number of games = 52958
Draws = 4331
Win/Loss = 0.91

--------------------
```

## Playing manually:
Play a normal game using 4 decks and shuffling 6 times on startup.
```
from blackjack import Blackjack

num_decks = 4
num_shuffles = 6
Blackjack(num_decks, num_shuffles).play()
```

#### Output:
```
The player has [['K', 'diamonds'], ['J', 'diamonds']]
Player total: 20
The computer has[['4', 'clubs']]
Computer total: 4
Decks left: 4 (cards left 198)
High-Low value: -0.75
## Recommended move is to 's' ##
Hit or Stand (h or s): h
********************
The player has [['K', 'diamonds'], ['J', 'diamonds'], ['K', 'clubs']]
Player total: 30
The computer has[['4', 'clubs']]
Computer total: 4
Decks left: 4 (cards left 197)
High-Low value: -1.0
## Recommended move is to 's' ##
** The player busts **
The computer has [['4', 'clubs'], ['3', 'clubs']]
Computer total: 7
The computer wins!
-----------------------------
| Games  = 2 | Draws    = 0 |
-----------------------------
| Player = 1 | Computer = 1 |
-----------------------------
Press Enter (or q to quit):
```


#Setup
`python3 setup.py install`
