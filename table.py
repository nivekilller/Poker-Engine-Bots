from dealer import Dealer
from player import Player
from monty import Monty

class Table:
    def __init__(self):
        self.dealer = Dealer()
        self.players = []
        self.community_cards = []
        self.pot = 0
        self.current_call = 2
        self.big_blind = 2
        self.small_blind = 1
        self.folds = 0

    def add_player(self, type, name, bankroll):
        if type == "R":
            new_player = Player(name, bankroll)
            self.players.append(new_player)
        if type == "M":
            monty = Monty(name, bankroll)
            self.players.append(monty)

    def start_hand(self):
        # Reset table state for a new hand
        self.community_cards = []
        self.pot = self.small_blind + self.big_blind
        self.current_call = self.big_blind
        self.folds = 0
        self.dealer.shuffle_deck()
        
        for player in self.players:
            player.clear_hand()

        # Rotate button and assign blinds for the new hand
        self.rotate_button()
        self.players[0].take_small_blind()
        self.players[1].take_big_blind()

        # Dealer does the work
        self.dealer.deal_hands(self)

    def rotate_button(self):
        rotated_player = self.players.pop(0)
        self.players.append(rotated_player)

    def new_round(self):
        self.current_call = 0
        for player in self.players:
            player.clear_round()


    def display_table(self):
        print("\n" + "="*40)
        print(f"Pot: ${self.pot}")
        board_str = " | ".join(str(card) for card in self.community_cards) if self.community_cards else "None yet"
        print(f"Community Cards: [ {board_str} ]")
        print("-" * 40)
        print("Players:")
        for player in self.players:
            print(f"  {player}")
        print("="*40 + "\n")


    def prompt_player(self, player):
        self.display_table()
        action, chips_paid, new_total_bet = player.get_action(self)
        
        if action == "fold":
            self.folds += 1
            return 0

        elif action == "call":
            self.pot += chips_paid
            return 0

        elif action == "raise":
            self.pot += chips_paid
            if new_total_bet > self.current_call:
                self.current_call = new_total_bet
                return 1
                
            return 0
        
    def conduct_betting_round(self, start_index):
        num_players = len(self.players)
        current_idx = start_index
        
        consecutive_actions = 0
        
        while True:
            active_players = [p for p in self.players if not p.is_folded and not p.is_all_in]
            
            if len(active_players) <= 1:
                break
                
            if consecutive_actions >= len(active_players):
                break
                
            player = self.players[current_idx % num_players]
            
            if player.is_folded or player.is_all_in:
                current_idx = (current_idx + 1) % num_players
                continue
                
            did_raise = self.prompt_player(player)
            consecutive_actions += 1
            
            if did_raise:
                consecutive_actions = 1
                
            current_idx = (current_idx + 1) % num_players


    def pre_flop_betting(self):
        print("\n--- PRE-FLOP ---")
        self.conduct_betting_round(2)


    def post_flop(self):
        print("\n--- FLOP BETTING ---")
        self.new_round()
        self.conduct_betting_round(0)


    def turn_betting(self):
        print("\n--- TURN BETTING ---")
        self.new_round()
        self.conduct_betting_round(0)


    def river_betting_showdown(self):
        print("\n--- RIVER BETTING ---")
        self.new_round()
        self.conduct_betting_round(0)


    def calculate_pots(self):
        pots = []
        all_contributors = self.players 
        previous_cap = 0
        
        # Get unique, sorted investment levels from all players
        investment_levels = sorted(list(set(p.bet_this_game for p in all_contributors if p.bet_this_game > 0)))

        for cap in investment_levels:
            pot_slice = 0
            eligible_players = []
            
            for player in all_contributors:
                contribution_at_this_level = min(player.bet_this_game, cap) - previous_cap
                if contribution_at_this_level > 0:
                    pot_slice += contribution_at_this_level
                    
                if not player.is_folded and player.bet_this_game >= cap:
                    eligible_players.append(player)
                    
            if pot_slice > 0:
                pots.append({
                    'amount': pot_slice,
                    'eligible': eligible_players
                })
                
            previous_cap = cap
            
        return pots

    def showdown(self):
        print("\n--- SHOWDOWN ---")
        self.display_table()
        pots = self.calculate_pots()
        
        for i, pot in enumerate(pots):
            pot_amount = pot['amount']
            eligible_players = pot['eligible']
            
            if not eligible_players or pot_amount == 0:
                continue
                
            print(f"\nResolving Pot #{i+1} (${pot_amount})")
            
            # Evaluate hand scores only for players eligible for this specific pot layer
            player_scores = {}
            for player in eligible_players:
                score = self.dealer.evaluate_best_hand(player.hand, self.community_cards)
                player_scores[player] = score
                print(f"  {player.name} score: {score}")
                
            # Find the best score in this pot
            max_score = max(player_scores.values())
            
            # Find all winners who tied for this best score
            pot_winners = [player for player, score in player_scores.items() if score == max_score]
            
            # Split and pay out
            share = pot_amount / len(pot_winners)
            for winner in pot_winners:
                winner.give_money(share)
                print(f"🏆 {winner.name} wins ${share:.2f} from Pot #{i+1}!")


    def play_hand(self):
        self.start_hand()
        self.pre_flop_betting()

        if self.folds <= len(self.players)-1:
            self.dealer.deal_flop(self)
            self.post_flop()

        if self.folds <= len(self.players)-1:
            self.dealer.deal_turn_or_river(self)
            self.turn_betting()

        if self.folds <= len(self.players)-1:
            self.dealer.deal_turn_or_river(self)
            self.river_betting_showdown()

        self.showdown()