"""
File: card.py
Author: Alex Gill
Used to build a deck of cards in a card game.
"""
import random

class Card:
    """A card with a suit and a rank."""

    RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    SUITS = ('Spades', 'Diamonds', 'Hearts', 'Clubs')

    def __init__(self, rank, suit, faceup=False):
        """Initializes a card with the given rank and suit."""
        self.rank = rank
        self.suit = suit
        self.faceup = faceup

    def flip(self):
        """Flips the card."""
        self.faceup = not self.faceup
    
    def __str__(self):
        """Returns a string representation of a card."""
        if self.rank == 1:
            rank = 'Ace'
        elif self.rank == 11:
            rank = 'Jack'
        elif self.rank == 12:
            rank = 'Queen'
        elif self.rank == 13:
            rank = 'King'
        else:
            rank = self.rank
        return str(rank) + ' of ' + self.suit


class Deck:
    """A deck containing 52 cards."""

    def __init__(self):
        """Creates a full deck of cards."""
        self.cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                c = Card(rank, suit)
                self.cards.append(c)

    def shuffle(self):
        """Shuffles the cards."""
        random.shuffle(self.cards)

    def deal(self):
        """Removes and returns the top card or None
        if the deck is empty."""
        if len(self) == 0:
            return None
        else:
            return self.cards.pop(0)

    def __len__(self):
        """Returns the number of cards left in the deck."""
        return len(self.cards)
    
    def __str__(self):
        """Returns a string representation of the deck."""
        result = ''
        for c in self.cards:
            result = result + str(c) + '\n'
        return result