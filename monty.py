from player import Player
from deck import Deck
import copy

class Monty(Player):
    def get_action(self, table):
        the_call = table.current_call
        amount_to_call = max(0, the_call - self.bet_this_round)
        
        print(f"{Monty} Monty analyzes hand...")

        new_deck = Deck()
        new_deck.cards = [card for card in new_deck.cards if card not in (table.community_cards + self.hand)]

        win = 0
        tie = 0
        for iteration in range(0, 1000):
            cards_out = copy.deepcopy(table.community_cards)
            the_deck = copy.deepcopy(new_deck)
            the_deck.shuffle()

            cards_needed = 5 - len(cards_out)
            for i in range(cards_needed):
                cards_out.append(the_deck.deal_card())

            opp_hand = [the_deck.deal_card(), the_deck.deal_card()]

            my_score = table.dealer.evaluate_best_hand(self.hand, cards_out)
            opp_score = table.dealer.evaluate_best_hand(opp_hand, cards_out)

            if my_score > opp_score:
                win += 1
            elif my_score == opp_score:
                tie += 1

        average = ((win + tie/2) / 1000)

            

        self.bankroll -= amount_to_call
        self.update_bets(amount_to_call)
        return "call", amount_to_call, self.bet_this_round