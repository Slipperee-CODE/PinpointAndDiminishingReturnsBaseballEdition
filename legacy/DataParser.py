from pathlib import Path
from legacy.Player import Player

class DataParser:
    def __init__(self, data_file_path):
        self.player_data = []
        self.parse_player_data(data_file_path)

    def parse_player_data(self, data_file_path):
        file_path = Path(data_file_path)
        data = file_path.read_text(encoding="utf-8")
        
        for line in data.split("\n"):
            split_line = line.split(",")
            self.player_data.append(Player(int(split_line[0]), split_line[1], int(split_line[2])))

    def begin(self):
        ...