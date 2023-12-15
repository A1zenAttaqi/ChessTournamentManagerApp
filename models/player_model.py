from tinydb import TinyDB
import json


class PlayerModel:
    """ Represents a chess player. """
    players_db = TinyDB('data/players/players_db.json')

    def __init__(self, first_name, last_name, birth_date, chess_id, tournaments_participated=None):
        """ Initialize a PlayerModel instance. """
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.total_points = 0
        self.tournaments_participated = tournaments_participated or []

    def __str__(self):
        """Return a string representation of the player."""
        return f"Player: {self.first_name} {self.last_name}, Chess ID: {self.chess_id}"

    def get_full_name(self):
        """Get the full name of the player."""
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        """Serialize the Player object to a dictionary."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": str(self.birth_date),
            "chess_id": self.chess_id,
            "tournaments_participated": self.tournaments_participated,

        }

    @classmethod
    def from_dict(cls, player_dict):
        """Deserialize a dictionary to create a PlayerModel instance."""
        first_name = player_dict.get("first_name", "")
        last_name = player_dict.get("last_name", "")
        birth_date = player_dict.get("birth_date", "")
        chess_id = player_dict.get("chess_id", "")
        tournaments_participated = player_dict.get("tournaments_participated", [])
        return cls(first_name, last_name, birth_date, chess_id, tournaments_participated)

    def save_to_db(self, tournament_name=None):
        """ Save player information to the database. """
        player_data = self.to_dict()
        self.players_db.insert(player_data)

        if tournament_name:
            playerdb_json_path = 'data/players/players_db.json'
            with open(playerdb_json_path, 'r') as file:
                playerdb = json.load(file)

            for player_info in playerdb['_default'].values():
                if player_info['chess_id'] == self.chess_id:
                    if 'tournaments_participated' not in player_info:
                        player_info['tournaments_participated'] = []

                    player_info['tournaments_participated'].append(tournament_name)
                    break

            with open(playerdb_json_path, 'w') as file:
                json.dump(playerdb, file, indent=2)
