class Card:
    def __init__(self, suit, rank):
        self.suit = suit  # e.g., 'Hearts', 'Spades'
        self.rank = rank  # e.g., 'A', 'K', 10, 9

    def get_value(self):
        values = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }

        return values.get(str(self.rank))

    # This is a special Python method that controls how the object looks when printed
    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank