from unittest.mock import patch
from table import Table

if __name__ == "__main__":

    # Initialize the Table
    poker_table = Table()

    # Add players
    poker_table.add_player("R", "Alice", 1000)
    poker_table.add_player("M", "Carlos", 1000)


    # Lez do it
    poker_table.play_hand() 