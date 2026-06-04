from Game import Game
from typing import override
from tabulate import tabulate

class DiminishingReturns(Game):
    def __init__(self, player_count:int):
        super().__init__(player_count)
        self.guessed_bb_players = set()
        self.per_player_ceilings = {player:-1 for player in self.player_scores}

        print("You are playing Diminishing Returns! \n")
        self.play()

    @override
    def score_player(self, player_name):
        rk, bb_player, stat = self.get_player_guess()

        while bb_player in self.guessed_bb_players:
            print(f"The player \"{bb_player}\" has already been guessed.")
            rk, bb_player, stat = self.get_player_guess()

        if self.per_player_ceilings[player_name] == -1:
            self.per_player_ceilings[player_name] = stat

            self.guessed_bb_players.add(bb_player)
            self.per_player_guesses[player_name].append(f"+1 ({stat}) {bb_player}")
            return 1
        
        if self.per_player_ceilings[player_name] >= stat:
            self.guessed_bb_players.add(bb_player)
            self.per_player_guesses[player_name].append(f"+1 ({stat}) {bb_player}")
            self.per_player_ceilings[player_name] = stat
            return 1
        else: # strike
            self.guessed_bb_players.add(bb_player)
            self.per_player_strikes[player_name] += 1
            self.per_player_guesses[player_name].append(f"{self.per_player_strikes[player_name]}X ({stat}) {bb_player}")
            print(f"{player_name}'s strike {self.per_player_strikes[player_name]}!")
            return 0

    def get_player_guess(self):
        try:
            baseball_player_info = input("Provide (Rk   Player Name   Stat): ")
            baseball_player_info = baseball_player_info.split("\t")
            return int(baseball_player_info[0]), baseball_player_info[1], int(baseball_player_info[2])
        except Exception as e:
            print(f"get_player_guess errored with \"{e}\", try again")
            retry = self.get_player_guess()
            return retry[0], retry[1], retry[2]

    @override
    def create_player_scores_list(self):
        og_list = super().create_player_scores_list()

        for index, player in enumerate(self.per_player_ceilings):
            og_list[index] = og_list[index] + f" ({self.per_player_ceilings[player]})"
        
        return og_list

    @override
    def save_game_specific_save_data(self):
        headers = self.create_player_scores_list()
        data = list(zip(*self.per_player_guesses.values()))

        return tabulate(data, headers=headers, tablefmt="github")