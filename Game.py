from datetime import datetime
from pathlib import Path
import os

class Game:
    GAME_DATA_PATH = "PastGameData\\"
    MAX_STRIKES = 3

    def __init__(self, player_count:int):
        self.player_scores = {}
        self.player_order = []
        self.setup_players(player_count)
        self.per_player_guesses = {player:[] for player in self.player_scores}
        self.per_player_strikes = {player:0 for player in self.player_scores}
        self.game_data_file_path = self.create_game_save_file()
        
    def setup_players(self, player_count):
        for p in range(player_count):
            curr_player_name = input(f"Player {p+1}'s name: ")
            self.player_scores[curr_player_name] = 0
            self.player_order.append(curr_player_name)

    def create_player_scores_list(self):
        return [player + ": " + str(self.player_scores[player]) for player in self.player_scores]

    def play(self):
        while True:
            for player in self.player_order:
                if self.per_player_strikes[player] < self.MAX_STRIKES:
                    print(" | ".join(self.create_player_scores_list()))
                    print(f"{player}'s turn")
                    self.player_scores[player] += self.score_player(player)
                else:
                    print(f"Skipping {player}'s turn!")
                    self.per_player_guesses[player].append(f"Skipped!")
        
            self.save_game_data()
            self.player_order.reverse() # allows for "snake" turn-ordering
            input("Press enter for next round ")
            os.system("cls")

    # to be overridden in subclasses
    def score_player(self, player_name:str):
        ...

    def create_game_save_file(self):
        now = datetime.now()
        filename = self.__class__.__name__ + "@" + now.strftime("%Y-%m-%d %H_%M_%S") + ".txt"
        file_path = Path(self.GAME_DATA_PATH + filename)
        file_path.write_text("No data yet.", encoding="utf-8")

        return file_path

    def save_game_data(self):
        # self.game_data_file_path.write_text(self.game_data_file_path.name + "\n" + self.save_game_specific_save_data(), encoding="utf-8")
        self.game_data_file_path.write_text(self.save_game_specific_save_data(), encoding="utf-8")

    # to be overridden in subclasses
    def save_game_specific_save_data(self):
        return "[Default game specific data]"

    # to be overridden in subclasses
    def load_game_specific_save_data(self):
        ...