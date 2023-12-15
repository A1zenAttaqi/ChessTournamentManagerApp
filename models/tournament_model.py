from models.player_model import PlayerModel
import json
from datetime import datetime


class TournamentModel:
    """ Represents a chess tournament. """

    def __init__(self, name=None, location=None, start_date=None, end_date=None,
                 number_of_rounds=4, current_round=1, rounds=None, players=None,
                 description=""):
        """ Initialize a TournamentModel instance. """
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.rounds = rounds or []
        self.players = players or []
        self.description = description
        self.file_path = self.generate_file_path(name)

    def generate_file_path(self, name):
        """Generate the file path based on the tournament name."""

        if name:
            return f"data/tournaments/{name.lower().replace(' ', '_')}.json"
        else:
            return "data/tournaments/default.json"

    @classmethod
    def load_from_file(cls, file_path):
        """Load tournament data from a file and create a TournamentModel instance."""

        try:
            with open(file_path, 'r') as file:
                tournament_data = json.load(file)
                tournament_data.setdefault('current_round', 1)
                tournament_data.setdefault('rounds', [])

                players = [PlayerModel.from_dict(player_data) for player_data in tournament_data.get('players', [])]

                rounds = [RoundModel.from_dict(round_data) if isinstance(round_data, dict)
                          else {} for round_data in tournament_data.get('rounds', [])]

                tournament_data['players'] = players
                tournament_data['rounds'] = rounds

                tournament = cls(**tournament_data)
                return tournament
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None

    def save_to_file(self):
        """Save tournament data to a file."""
        with open(f"data/tournaments/{self.name}.json", 'w') as file:
            json.dump(self.to_dict(), file)

    def register_player(self, player_id, player_controller, tournament_name):
        """ Register a player for the tournament. """
        if len(self.players) >= 8:
            return 'full'

        player = player_controller.find_player_by_id(player_id)

        if player is None:
            return None

        player_ids_in_tournament = [p.chess_id for p in self.players]

        if player_id in player_ids_in_tournament:
            return True
        player.tournaments_participated.append(tournament_name)
        player.save_to_db(tournament_name)

        self.players.append(player)
        self.save_to_file()
        return False

    def get_tournament_players(self):
        """Get the list of players participating in the tournament."""
        return self.players

    def get_rounds(self):
        """Get the list of RoundModel instances representing tournament rounds."""
        return self.rounds

    def create_round(self):
        """Create a new round in the tournament."""
        new_round = RoundModel(name=f"Round {self.current_round}", start_time=datetime.now())

        self.rounds.append(new_round)
        self.current_round += 1

    def to_dict(self):
        """Serialize the Tournament object to a dictionary."""
        return {
            "name": self.name,
            "location": self.location,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": [
                rnd.to_dict() for rnd in self.rounds
            ] if self.rounds else [],
            "players": [player.to_dict() if isinstance(player, PlayerModel) else player for player in self.players],
            "description": self.description
        }

    @classmethod
    def from_dict(cls, tournament_dict):
        """Deserialize a dictionary to create a Tournament object."""
        tournament = cls(
            tournament_dict["name"],
            tournament_dict["location"],
            tournament_dict["start_date"],
            tournament_dict["end_date"],
            tournament_dict["number_of_rounds"]
        )
        tournament.current_round = tournament_dict["current_round"]

        tournament.rounds = [RoundModel.from_dict(round_dict) if isinstance(round_dict, dict)
                             else round_dict for round_dict in tournament_dict.get('rounds', [])]

        tournament.players = [PlayerModel.from_dict(player_dict) if isinstance(player_dict, dict)
                              else player_dict for player_dict in tournament_dict["players"]]
        tournament.description = tournament_dict["description"]
        return tournament


class RoundModel:
    """ Represents a round in a chess tournament. """

    def __init__(self, name=None, matches=None, start_time=None, end_time=None):
        """ Initialize a RoundModel instance. """
        self.name = name
        self.matches = matches or []
        self.start_time = start_time or datetime.now()
        self.end_time = end_time

    def to_dict(self):
        """Serialize the RoundModel instance to a dictionary."""
        matches_data = [match.to_dict() for match in self.matches]

        return {
            "name": self.name,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else None,
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else None,
            "matches": matches_data,
        }

    @classmethod
    def from_dict(cls, round_dict):
        """Deserialize a dictionary to create a RoundModel instance."""
        name = round_dict["name"]

        start_time = datetime.now()
        end_time = datetime.now()
        matches = [MatchModel.from_dict(match_dict) for match_dict in round_dict.get("matches", [])]

        return cls(name, matches, start_time, end_time)


class MatchModel:
    """Represents a match between two players in a round of a chess tournament."""

    def __init__(self, player1, player2, score1=None, score2=None):
        """ Initialize a MatchModel instance. """
        self.match_data = ([player1, score1], [player2, score2])

    def set_scores(self, score1, score2):
        """ Set the scores for the players in the match. """
        self.match_data[0][1] = score1
        self.match_data[1][1] = score2

    @classmethod
    def from_dict(cls, match_dict):
        """Deserialize a dictionary to create a MatchModel instance."""

        player1_data = match_dict["player1"]
        player2_data = match_dict["player2"]

        player1, score1 = cls.parse_player_data(player1_data)
        player2, score2 = cls.parse_player_data(player2_data)

        return cls(player1, player2, score1, score2)

    def to_dict(self):
        """Serialize the MatchModel object to a dictionary."""
        return {
            "player1": {
                "first_name": self.match_data[0][0].first_name,
                "last_name": self.match_data[0][0].last_name,
                "birth_date": self.match_data[0][0].birth_date,
                "chess_id": self.match_data[0][0].chess_id,
                "tournaments_participated": self.match_data[0][0].tournaments_participated

            },
            "score1": self.match_data[0][1],
            "player2": {
                "first_name": self.match_data[1][0].first_name,
                "last_name": self.match_data[1][0].last_name,
                "birth_date": self.match_data[1][0].birth_date,
                "chess_id": self.match_data[1][0].chess_id,
                "tournaments_participated": self.match_data[1][0].tournaments_participated
            },
            "score2": self.match_data[1][1]
        }

    @classmethod
    def parse_player_data(cls, player_data):
        """Parse player data from a dictionary."""
        player = PlayerModel(
            first_name=player_data["first_name"],
            last_name=player_data["last_name"],
            birth_date=player_data["birth_date"],
            chess_id=player_data["chess_id"],
            tournaments_participated=player_data.get("tournaments_participated", [])
        )
        score = player_data.get("score", 0.0)
        return player, score
