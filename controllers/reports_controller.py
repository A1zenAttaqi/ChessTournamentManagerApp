from models.player_model import PlayerModel
from views.player_view import PlayerView
from models.tournament_model import TournamentModel
from views.reports_view import ReportsView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from tinydb import TinyDB
import os


class ReportsController:
    """ Controller for generating reports. """

    def __init__(self):
        self.tournament_controller = TournamentController()
        self.player_controller = PlayerController()
        self.tournament_report_view = ReportsView()

        self.players_folder = 'data/players'
        self.players_db = TinyDB(os.path.join(self.players_folder, 'players_db.json'))

    def generate_players_alphabetical_report(self):
        """ Generate and display an alphabetical list of players. """
        players = self.get_players_sorted()
        player_view = PlayerView()
        player_view.display_players(players)

    def get_players_sorted(self):
        """ Get a sorted list of players. """
        players = self.players_db.all()
        player_models = [PlayerModel.from_dict(player) for player in players]
        sorted_players = sorted(player_models, key=lambda x: (x.first_name, x.last_name))
        return sorted_players

    def generate_all_tournaments_report(self):
        """ Generate and display a report of all tournaments. """
        tournament_folder = os.path.join(self.tournament_controller.data_folder, 'tournaments')
        tournament_files = [f for f in os.listdir(tournament_folder) if f.endswith('.json')]

        tournaments_data = []
        for tournament_file in tournament_files:
            tournament_path = os.path.join(tournament_folder, tournament_file)
            try:
                tournament = TournamentModel.load_from_file(tournament_path)
                tournaments_data.append(tournament)
            except FileNotFoundError:
                print(f"File not found: {tournament_path}")

        self.tournament_report_view.display_all_tournaments(tournaments_data)

    def generate_tournament_info_report(self):
        """ Generate and display a report for a specific tournament. """
        tournament_name = input("Enter the name of the tournament: ")
        tournaments = self.tournament_controller.load_tournaments()

        for tournament in tournaments:
            if tournament.name == tournament_name:
                self.tournament_report_view.display_selected_tournament(tournament)
                return

        print(f"Tournament '{tournament_name}' not found.")

    def generate_players_in_tournament_report(self):
        tournament_name = input("Enter the name of the tournament: ")
        tournaments = self.tournament_controller.load_tournaments()
        for tournament in tournaments:
            if tournament.name == tournament_name:
                players = tournament.get_tournament_players()

                if players:
                    ReportsView.display_players(players)
                else:
                    print(f"No players found for tournament '{tournament_name}'.")
                break
        else:
            print(f"Tournament '{tournament_name}' not found.")

    def generate_tournament_rounds_and_matches_report(self):
        """ Generate and display a report for tournament rounds and matches. """
        tournament_name = input("Enter the name of the tournament: ")
        tournaments = self.tournament_controller.load_tournaments()

        for tournament in tournaments:
            if tournament.name == tournament_name:
                file_path = f"data/tournaments/{tournament_name}.json"
                tournament = self.tournament_controller.load_tournament_from_file(file_path)

                rounds = tournament.get_rounds()

                if rounds:
                    for round_num, round_model in enumerate(rounds, start=1):
                        matches = round_model.matches

                        ReportsView.display_tournament_round_and_matches(tournament_name, round_num, matches)
                    return
                else:
                    print("No rounds found for the tournament.")
                    return

        print(f"Tournament '{tournament_name}' not found.")
