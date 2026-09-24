from player import Player

class Monty(Player):
    def get_action(self, the_call):
        amount_to_call = max(0, the_call - self.bet_this_round)
        
        # TODO: Add Monte Carlo simulation logic here
        # Placeholder behavior: Monty simply checks or calls every time for now
        print(f"{Monty} (Bot) analyzes hand...")
        
        self.bankroll -= amount_to_call
        self.update_bets(amount_to_call)
        return "call", amount_to_call, self.bet_this_round