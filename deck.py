import random
from card import Card  # Pulling in our Card class from the other file

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        # Build the deck using a list comprehension (or a standard loop)
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        # Pop a card off the end of the list, or return None if empty
        if len(self.cards) > 0:
            return self.cards.pop()
        return None