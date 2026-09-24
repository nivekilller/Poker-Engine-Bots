class Player:
    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = bankroll
        self.is_folded = False
        self.is_all_in = False
        self.bet_this_game = 0
        self.bet_this_round = 0
        self.hand = []

    def give_card(self, card):
        self.hand.append(card)

    def give_money(self, money):
        self.bankroll += money

    def clear_hand(self):
        self.hand = []
        self.is_folded = False
        self.is_all_in = False
        self.bet_this_game = 0
        self.clear_round()

    def clear_round(self):
        self.bet_this_round = 0

    def update_bets(self, num):
        self.bet_this_game += num
        self.bet_this_round += num

    def take_big_blind(self):
        self.bankroll -= 2
        self.update_bets(2)

    def take_small_blind(self):
        self.bankroll -= 1
        self.update_bets(1)

    def get_action(self, the_call):
        amount_to_call = max(0, the_call - self.bet_this_round)
        action = input(f"{self.name}, ${amount_to_call} to call. [c] to call, [r] to raise, [a] for all-in, [f] to fold: ").lower()

        if action == "f":
            self.is_folded = True
            return "fold", 0, 0

        elif action == "c":
            self.bankroll -= amount_to_call
            self.update_bets(amount_to_call)
            return "call", amount_to_call, self.bet_this_round

        elif action == "a":
            chips_paid = self.bankroll
            self.bankroll = 0
            self.is_all_in = True
            self.update_bets(chips_paid)
            return "raise", chips_paid, self.bet_this_round

        elif action == "r":
            increase_str = input("Input total amount to raise TO for this round, or [a] for all in: ")
            
            if increase_str.lower() == 'a':
                chips_paid = self.bankroll
                self.bankroll = 0
                self.is_all_in = True
                self.update_bets(chips_paid)
                return "raise", chips_paid, self.bet_this_round

            try:
                target_total_bet = int(increase_str)
            except ValueError:
                target_total_bet = the_call

            # Rule 1: If you try to raise less than the call amount, default to call
            if target_total_bet < the_call:
                print(f"Raise amount is less than the call requirement. Defaulting to call.")
                chips_paid = amount_to_call
                self.bankroll -= chips_paid
                self.update_bets(chips_paid)
                return "call", chips_paid, self.bet_this_round

            chips_paid = target_total_bet - self.bet_this_round

            # Rule 2: If you try to raise above what you have, default to all-in
            if chips_paid > self.bankroll:
                print(f"Raise exceeds your bankroll! Shoving all-in for ${self.bankroll}.")
                chips_paid = self.bankroll
                self.bankroll = 0
                self.is_all_in = True
                self.update_bets(chips_paid)
                return "raise", chips_paid, self.bet_this_round

            if chips_paid < 0:
                chips_paid = 0

            self.bankroll -= chips_paid
            self.update_bets(chips_paid)
            return "raise", chips_paid, self.bet_this_round

            
    def __str__(self):
        hand_str = ", ".join(str(card) for card in self.hand)
        return f"{self.name} (${self.bankroll}) [Hole Cards: {hand_str}]"