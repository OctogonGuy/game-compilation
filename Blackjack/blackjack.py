"""
File: blackjack.py
Author: Alex Gill
Simulates a game of blackjack.
"""
from tkinter import *
from tkinter import ttk
from cards import Deck, Card

class Player:
    """Represents a player in a blackjack game."""

    def __init__(self, cards):
        self.cards = cards
        

    def hit(self, card):
        """Adds a card to the hand."""
        self.cards.append(card)

    def get_points(self):
        """Returns the number of points in the hand."""
        count = 0
        for card in self.cards:
            if card.rank > 9:
                count += 10
            elif card.rank == 1:
                count += 11
            else:
                count += card.rank
        
        # Deduct 10 if Ace is available and needed as 1
        for card in self.cards:
            if count <= 21:
                break
            elif card.rank == 1:
                count -= 10
        
        return count

    def has_blackjack(self):
        """Dealt 21 or not."""
        return len(self.cards) == 2 and self.get_points() == 21

    def __str__(self):
        """Returns a string representation of cards and points."""
        result = ', '.join(map(str, self.cards))
        result += '\n' + str(self.get_points()) + ' points'
        return result


class Dealer(Player):
    """Represents the dealer in a blackjack game. Is like a Player,
    but a bit more specialized and has some restrictions."""

    def __init__(self, cards):
        """Initial state: show one card only."""
        Player.__init__(self, cards)
        self.show_one_card = True

    def __str__(self):
        """Returns just one card if not hit yet."""
        if self.show_one_card:
            return str(self.cards[0])
        else:
            return Player.__str__(self)

    def hit(self, deck):
        """Add cards while points < 17,
        then allow all to be shown."""
        self.show_one_card = False
        while self.get_points() < 17:
            self.cards.append(deck.deal())


class Blackjack:

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        # Pass the player and the dealer two cards each
        self.player = Player([self.deck.deal(),
                              self.deck.deal()])
        self.dealer = Dealer([self.deck.deal(),
                              self.deck.deal()])
    
    def play(self):
        print('Player:\n', self.player)
        print('Dealer:\n', self.dealer)

        # Player hits until user says NO
        while True:
            choice = input('Do you want a hit? [y/n]: ')
            if choice in ('Y', 'y'):
                self.player.hit(self.deck.deal())
                points = self.player.get_points()
                print('Player:\n', self.player)
                if points >= 21:
                    break
            else:
                break
        player_points = self.player.get_points()
        if player_points > 21:
            print('You bust and you lose')
        else:
            # Dealer's turn to hit
            self.dealer.hit(self.deck)
            print('Dealer:\n', self.dealer)
            dealer_points = self.dealer.get_points()
            # Determine the outcome
            if dealer_points > 21:
                print('Dealer busts and you win')
            elif dealer_points > player_points:
                print('Dealer wins')
            elif dealer_points < player_points:
                print('You win')
            elif dealer_points == player_points:
                if self.player.has_blackjack() and \
                    not self.dealer.has_blackjack():
                    print('You win')
                elif not self.player.has_blackjack() and \
                        self.dealer.has_blackjack():
                    print('Dealer wins')
                else:
                    print('There is a tie')

if __name__ == '__main__':
    Blackjack().play()