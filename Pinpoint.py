from Game import Game
from typing import override
from tabulate import tabulate

class Pinpoint(Game):
    MAX_ACCEPTED_RANK = 100

    def __init__(self, player_count:int):
        super().__init__(player_count)
        self.guessed_bb_players = set()
        self.per_player_guesses = {player:[] for player in self.player_scores}

        print("You are playing Pinpoint! \n")
        self.play()

    @override
    def score_player(self, player_name):
        rk, bb_player = self.get_player_guess()

        while bb_player in self.guessed_bb_players:
            print(f"The player \"{bb_player}\" has already been guessed.")
            rk, bb_player = self.get_player_guess()

        if rk > self.MAX_ACCEPTED_RANK: # strike
            self.guessed_bb_players.add(bb_player)
            self.per_player_guesses[player_name].append(f"+0 ({str(rk)}) {bb_player}")
            self.per_player_strikes[player_name] += 1
            return 0
        
        self.guessed_bb_players.add(bb_player)
        self.per_player_guesses[player_name].append(f"+{str(rk)} {bb_player}")
        return rk

    def get_player_guess(self):
        try:
            baseball_player_info = input("Provide (Rk  Player Name): ")
            baseball_player_info = baseball_player_info.split("\t")
            return int(baseball_player_info[0]), baseball_player_info[1]
        except Exception as e:
            print(f"get_player_guess errored with \"{e}\", try again")
            retry = self.get_player_guess()
            return retry[0], retry[1]

    @override
    def save_game_specific_save_data(self):
        headers = self.create_player_scores_list()
        data = list(zip(*self.per_player_guesses.values()))

        return tabulate(data, headers=headers, tablefmt="github")

    @override
    def load_game_specific_save_data(self):
        ...

        

