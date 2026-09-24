from deck import Deck
import itertools
from collections import Counter

class Dealer:
    def __init__(self):
        self.deck = Deck()

    def shuffle_deck(self):
        self.deck = Deck()
        self.deck.shuffle()

    def deal_hands(self, table):
        # Deal 2 cards to each player at the table
        for _ in range(2):
            for player in table.players:
                card = self.deck.deal_card()
                player.give_card(card)

    def deal_flop(self, table):
        self.deck.deal_card()  # Burn card
        for _ in range(3):
            table.community_cards.append(self.deck.deal_card())

    def deal_turn_or_river(self, table):
        self.deck.deal_card()  # Burn card
        table.community_cards.append(self.deck.deal_card())


    def evaluate_best_hand(self, player_hole_cards, community_cards):
        all_cards = player_hole_cards + community_cards
        best_score = None
        
        for five_card_combo in itertools.combinations(all_cards, 5):
            score = self.score_5_card_hand(five_card_combo)
            if best_score is None or score > best_score:
                best_score = score
                
        return best_score

    
    def check_for_straight(self, ranks):
        unique_ranks = sorted(list(set(ranks)))
        if len(unique_ranks) < 5:
            return False

        for i in range(len(unique_ranks) - 4):
            window = unique_ranks[i:i+5]
            if window[4] - window[0] == 4:
                return True
        return False

    def check_for_straight_with_ace(self, ranks):
        adjusted_ranks = list(ranks)
        if 14 in adjusted_ranks:
            adjusted_ranks.append(1)
        return self.check_for_straight(adjusted_ranks)

    def score_5_card_hand(self, cards):
        suits_count = {
            'Hearts': [],
            'Diamonds': [],
            'Clubs': [],
            'Spades': []
        }

        values_list = []

        for card in cards:
            val = card.get_value() if callable(getattr(card, 'get_value', None)) else card.get_value
            suits_count[card.suit].append(val)
            values_list.append(val)

        values_list.sort(reverse=True)

        # 1. Check for Flush & Straight Flush
        flush_cards = None
        for suit, card_values in suits_count.items():
            if len(card_values) >= 5:
                # Sort the flush cards descending
                card_values.sort(reverse=True)
                flush_cards = card_values[:5]  # Take the best 5 if there are 6 or 7
                break

        if flush_cards:
            is_str_flush = self.check_for_straight_with_ace(flush_cards)
            if is_str_flush:
                # Handle Ace-low straight flush (wheel) where 5 is the high card
                sf_ranks = sorted(flush_cards, reverse=True)
                if sf_ranks == [14, 5, 4, 3, 2]:
                    high_card = 5
                else:
                    high_card = sf_ranks[0]
                return (8 * (15 ** 5)) + (high_card * (15 ** 4))

            # Regular Flush (Category 5) - uses all 5 cards as positional kickers
            score = 5 * (15 ** 5)
            for i in range(5):
                score += flush_cards[i] * (15 ** (4 - i))
            return score

        # 2. Check for Straight (Category 4)
        if self.check_for_straight_with_ace(values_list):
            unique_vals = sorted(list(set(values_list)), reverse=True)
            # Handle Wheel straight (A-2-3-4-5) high card is 5
            if set([14, 2, 3, 4, 5]).issubset(set(values_list)):
                straight_high = 5
            else:
                # Find the top of the consecutive 5-card window
                for i in range(len(unique_vals) - 4):
                    window = unique_vals[i:i+5]
                    if window[0] - window[4] == 4:
                        straight_high = window[0]
                        break
            return (4 * (15 ** 5)) + (straight_high * (15 ** 4))

        # 3. Check for Pairs, Trips, Quads, Full House, and High Card using Counter
        counts = Counter(values_list)
        sorted_counts = counts.most_common() # Sorted by frequency desc, then value desc
        
        # Flatten into a priority list of 5 cards
        priority_ranks = []
        for rank, freq in sorted_counts:
            for _ in range(freq):
                priority_ranks.append(rank)
        priority_ranks = priority_ranks[:5] # Keep best 5

        # Determine Category Number based on frequency pattern
        top_freq = sorted_counts[0][1]
        
        if top_freq == 4:
            category = 7  # Four of a Kind
        elif top_freq == 3 and len(sorted_counts) == 2:
            category = 6  # Full House
        elif top_freq == 3:
            category = 3  # Three of a Kind
        elif top_freq == 2 and len(sorted_counts) == 3:
            category = 2  # Two Pair
        elif top_freq == 2:
            category = 1  # One Pair
        else:
            category = 0  # High Card

        # Calculate final base-15 score
        score = category * (15 ** 5)
        for i in range(5):
            score += priority_ranks[i] * (15 ** (4 - i))
            
        return score