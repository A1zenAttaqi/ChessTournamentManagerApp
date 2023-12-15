
import os
from tinydb import TinyDB, Query
from models.player_model import PlayerModel
from views.player_view import PlayerView


class PlayerController:
    """ Controller for player-related actions. """

    def __init__(self, player_model=None):
        self.player_model = player_model
        self.data_folder = 'data'
        self.players_folder = 'data/players'
        self.players_db = TinyDB(os.path.join(self.players_folder, 'players_db.json'))
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(self.players_folder, exist_ok=True)
        self.players = self.load_players()
        self.player_view = PlayerView()

    def load_players(self):
        """ Load player data from the database. """
        return self.players_db.all()

    def get_player_info(self):
        """ Get player information from the user. """
        return self.player_view.get_player_info()

    def create_player(self):
        """ Create a new player and save to the database. """
        player_info = self.get_player_info()
        new_player = PlayerModel(**player_info)
        self.players.append(new_player)
        new_player.save_to_db()
        PlayerView.show_player_registered_confirmation(new_player)

    def save_players(self):
        """ Save player data to the database. """

        serialized_players = [player.to_dict() for player in self.players]
        existing_ids = {player['Chess_id'] for player in self.players_db.all()}

        for serialized_player in serialized_players:
            player_id = serialized_player['Chess_id']
            if player_id not in existing_ids:
                self.players_db.insert(serialized_player)
            else:
                player_query = Query()
                self.players_db.update(serialized_player, player_query.Chess_id == player_id)

    def view_player_details(self):
        """ View details of a specific player. """
        player_id = PlayerView.get_player_id()
        player = self.find_player_by_id(player_id)

        if player:
            PlayerView.display_players([player])
        else:
            print("Player not found.")

    def list_players(self):
        """ List all players. """
        players = [PlayerModel.from_dict(player) for player in self.get_players()]
        player_view = PlayerView()
        player_view.display_players(players)

    def find_player_by_id(self, chess_id):
        """ Find a player by their Chess ID. """
        player_query = Query()
        player_doc = self.players_db.get(player_query.chess_id == chess_id)

        if player_doc:
            return PlayerModel.from_dict(player_doc)
        else:
            return None

    def get_players(self):
        """ Get a list of all players. """
        players = self.players_db.all()
        for player in players:
            player["birth_date"] = str(player["birth_date"])
        return players
