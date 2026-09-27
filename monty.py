from player import Player
from deck import Deck
import random
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
        pot_odds = amount_to_call / (amount_to_call + table.pot)

        roll = random.random()
        if (average < pot_odds):
            if average < 0.25:
                self.is_folded = True
                return "fold", 0, 0
            
            elif roll <= 0.90:
                self.bankroll -= amount_to_call
                self.update_bets(amount_to_call)
                return "call", amount_to_call, self.bet_this_round

            else:
                raise_increment = max(1, int(self.bankroll * 0.10))
                target_total_bet = table.current_call + raise_increment
                
                chips_paid = target_total_bet - self.bet_this_round
                
                # Safety check: don't overspend bankroll
                if chips_paid >= self.bankroll:
                    chips_paid = self.bankroll
                    self.bankroll = 0
                    self.is_all_in = True
                else:
                    self.bankroll -= chips_paid
                    
                self.update_bets(chips_paid)
                return "raise", chips_paid, self.bet_this_round

        elif (pot_odds - 0.1) <= average <= (pot_odds + 0.2):
            if roll < 0.80:
                self.bankroll -= amount_to_call
                self.update_bets(amount_to_call)
                return "call", amount_to_call, self.bet_this_round
            else:
                self.is_folded = True
                return "fold", 0, 0

        else:
        # Monty's hand is significantly better than the pot requires!
            if roll < 0.20:
                # 1. Slowplay / Call (20% of the time)
                self.bankroll -= amount_to_call
                self.update_bets(amount_to_call)
                return "call", amount_to_call, self.bet_this_round
                
            elif roll < 0.60:
                # 2. Standard Value Raise: 100% of the call amount (40% of the time)
                # If checking is free (amount_to_call == 0), default to a standard min-bet size
                base_raise = amount_to_call if amount_to_call > 0 else 20
                raise_increment = base_raise * 1  # 100%
                target_total_bet = table.current_call + raise_increment
                
                chips_paid = target_total_bet - self.bet_this_round
                if chips_paid >= self.bankroll:
                    chips_paid = self.bankroll
                    self.bankroll = 0
                    self.is_all_in = True
                else:
                    self.bankroll -= chips_paid
                    
                self.update_bets(chips_paid)
                return "raise", chips_paid, self.bet_this_round
                
            elif roll < 0.90:
                # 3. Stronger Value Raise: 200% of the call amount (30% of the time)
                base_raise = amount_to_call if amount_to_call > 0 else 20
                raise_increment = base_raise * 2  # 200%
                target_total_bet = table.current_call + raise_increment
                
                chips_paid = target_total_bet - self.bet_this_round
                if chips_paid >= self.bankroll:
                    chips_paid = self.bankroll
                    self.bankroll = 0
                    self.is_all_in = True
                else:
                    self.bankroll -= chips_paid
                    
                self.update_bets(chips_paid)
                return "raise", chips_paid, self.bet_this_round
                
            else:
                # 4. Maximum Aggression / All-In (10% of the time)
                chips_paid = self.bankroll
                self.bankroll = 0
                self.is_all_in = True
                self.update_bets(chips_paid)
                return "raise", chips_paid, self.bet_this_round