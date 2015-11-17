import random
from queue import Queue


class Deck:
    def __init__(self, decks=1, shuffle=4):
        """
        Uses a queue system to simulate cards being drawn and discarded

        :param decks: number of decks to use
        :param shuffle: number of times to shuffle
        :return:
        """
        self.deck = Queue()
        self.shuffle_times = shuffle
        self.suits = ['spades', 'clubs', 'hearts', 'diamonds']
        self.cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for deck in range(decks):
            for suit in self.suits:
                for card in self.cards:
                    self.deck.put([card, suit])

    def draw(self):
        """
        :return: a random card from the deck
        """
        card = self.deck.get()
        return card

    def shuffle(self):
        """
        Shuffles the deck n times
        :return: none
        """
        if self.shuffle_times > 0:
            temp = list(self.deck.queue)
            [random.shuffle(temp) for _ in range(self.shuffle_times)]
            self.deck = Queue()
            for card in temp:
                self.deck.put(card)


class Blackjack:
    def __init__(self, decks=1, shuffle=1):
        """
        :param decks: number of decks to use
        :param shuffle: number of times to shuffle
        :return: none
        """
        self.num_decks = decks
        self.deck = Deck(self.num_decks, shuffle)
        self.deck.shuffle()
        self.cards_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                           '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        self.high_low = {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0,
                         '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}
        self.games = 0
        self.draws = 0
        self.computer_win = 0
        self.player_win = 0
        self.running_count = 0
        self.player_hand = []
        self.computer_hand = []
        self.player_total = 0
        self.computer_total = 0

    def battle_bot(self):
        """
        Uses the Blackjack basic strategy to decide which move to make. Ability to distinguish soft and hard hands
        """
        if 'A' in [card[0] for card in self.player_hand]:
            if self.player_total <= 17:
                return 'h'
            elif self.player_total >= 19:
                return 's'
            elif self.player_total == 18 and 2 <= self.computer_total <= 8:
                return 's'
            elif self.player_total == 18 and self.computer_total >= 9:
                return 'h'
        else:
            if self.player_total <= 11:
                return 'h'
            elif self.player_total >= 17:
                return 's'
            elif self.player_total == 12 and 2 <= self.computer_total <= 3:
                return 'h'
            elif 12 <= self.player_total <= 16 and 4 <= self.computer_total <= 6:
                return 's'
            elif 13 <= self.player_total <= 16 and 2 <= self.computer_total <= 3:
                return 's'
            elif 4 <= self.player_total <= 16 and self.computer_total >= 7:
                return 'h'

    def total(self, hand):
        """
        Helper to check for aces in the hand and calculates the value of the hand

        :param hand: list of cards in the hand
        :return: value of the hand
        """
        aces = hand.count(11)
        hand_value = sum(hand)
        if hand_value > 21 and aces > 0:
            while aces > 0 and hand_value > 21:
                hand_value -= 10
                aces -= 1
        return hand_value

    def high_low_count(self, card):
        """
        Keeps track of the high/low count for card counting

        :param card: value of card
        :return: value of card according to high/low count
        """
        self.running_count += self.high_low[card[0]]
        return card

    def play(self, use_battle_bot=False):
        """
        The meat of the Blackjack class

        :param use_battle_bot: turns on the automated bot which plays the game
        :return: total games, total draws, total player wins, total computer wins
        """
        while self.deck.deck.qsize() >= 15:
            self.player_hand = [self.high_low_count(self.deck.draw()), self.high_low_count(self.deck.draw())]
            self.computer_hand = [self.high_low_count(self.deck.draw())]
            self.computer_total = self.total([self.cards_dict[card[0]] for card in self.computer_hand])
            player_bust = False
            computer_bust = False
            while True:
                self.player_total = self.total([self.cards_dict[card[0]] for card in self.player_hand])
                if not use_battle_bot:
                    print('The player has {}\nPlayer total: {}'.format(self.player_hand, self.player_total))
                    print('The computer has{}\nComputer total: {}'.format(self.computer_hand, self.computer_total))
                    print('Decks left: {} (cards left {})'.format(int(self.deck.deck.qsize() / 52 + 1),
                                                                  self.deck.deck.qsize()))
                    print('High-Low value: {}'.format(self.running_count / int(self.deck.deck.qsize() / 52 + 1)))
                    print('## Recommended move is to \'{}\' ##'.format(self.battle_bot()))
                if self.player_total > 21:
                    if not use_battle_bot:
                        print('** The player busts **')
                    player_bust = True
                    break
                elif self.player_total == 21:
                    if not use_battle_bot:
                        print('## Blackjack! ##')
                    break
                else:
                    if use_battle_bot:
                        hs = self.battle_bot()
                    else:
                        hs = input('Hit or Stand (h or s): ').lower()
                    if 'h' in hs:
                        self.player_hand.append(self.high_low_count(self.deck.draw()))
                        if not use_battle_bot:
                            print('********************')
                    else:
                        break
            while True:
                self.computer_hand.append(self.high_low_count(self.deck.draw()))
                while True:
                    self.computer_total = self.total([self.cards_dict[card[0]] for card in self.computer_hand])
                    if self.computer_total < 18 and not player_bust:
                        self.computer_hand.append(self.high_low_count(self.deck.draw()))
                    else:
                        break
                if not use_battle_bot:
                    print('The computer has {}\nComputer total: {}'.format(self.computer_hand, self.computer_total))
                if self.computer_total > 21:
                    if not use_battle_bot:
                        print('** The computer busts **')
                    computer_bust = True
                    if not player_bust:
                        if not use_battle_bot:
                            print('The player wins!')
                        self.player_win += 1
                elif self.computer_total > self.player_total:
                    if not use_battle_bot:
                        print('The computer wins!')
                    self.computer_win += 1
                elif self.computer_total == self.player_total:
                    if not use_battle_bot:
                        print('It\'s a draw!')
                    self.draws += 1
                elif self.player_total > self.computer_total:
                    if not player_bust:
                        if not use_battle_bot:
                            print('The player wins!')
                        self.player_win += 1
                    elif not computer_bust:
                        if not use_battle_bot:
                            print('The computer wins!')
                        self.computer_win += 1
                break
            self.games += 1
            if not use_battle_bot:
                print('-----------------------------')
                print('| Games  = {0} | Draws    = {1} |'.format(self.games, self.draws))
                print('-----------------------------')
                print('| Player = {0} | Computer = {1} |'.format(self.player_win, self.computer_win))
                print('-----------------------------')
                if not use_battle_bot:
                    end = input('Press Enter (or q to quit): ').lower()
                    if 'q' in end:
                        print('Thanks for playing blackjack with the computer!')
                        exit()
                print('\n----------------------------------------\n')
        if not use_battle_bot:
            print('\n**Finished deck**\n')
        return self.games, self.draws, self.player_win, self.computer_win
