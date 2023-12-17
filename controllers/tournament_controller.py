import os
from models.tournament_model import TournamentModel, RoundModel, MatchModel
from views.tournament_view import TournamentView
from controllers.player_controller import PlayerController
import random
from datetime import datetime


class TournamentController:
    """ Controller for tournament-related actions. """

    def __init__(self):
        self.tournament_model = TournamentModel()
        self.data_folder = 'data'
        self.tournaments_folder = 'data/tournaments'
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(self.tournaments_folder, exist_ok=True)
        self.tournaments = self.load_tournaments()
        self.player_controller = PlayerController()
        self.current_tournament = TournamentModel()

    def tournament_menu(self):
        """ Display the tournament menu and handle user choices. """
        while True:
            TournamentView.display_tournament_menu()

            choice = TournamentView.get_tournament_menu_choice()

            if choice is None:
                continue

            if choice == 0:
                return 0
            elif choice == 1:
                self.create_tournament()
            elif choice == 2:
                self.list_tournaments()
            elif choice == 3:
                self.select_tournament()
            elif choice == 4:
                self.register_players()
            else:
                print("Invalid choice. Please try again.")

    def load_tournaments(self):
        """ Load tournament data from files. """
        tournament_files = [f for f in os.listdir('data/tournaments') if f.endswith('.json')]
        tournaments = []

        for file_path in tournament_files:
            full_path = os.path.join('data/tournaments', file_path)
            tournament = TournamentModel.load_from_file(full_path)
            if tournament:
                tournaments.append(tournament)

        return tournaments

    def load_tournament_from_file(self, file_path):
        """ Load a specific tournament from a file. """
        tournament = TournamentModel.load_from_file(file_path)
        return tournament

    def create_tournament(self):
        """ Create a new tournament and save it to a file. """
        tournament_info = TournamentView.get_tournament_info()

        while not tournament_info['name']:
            print("Tournament name cannot be empty.")
            tournament_info = TournamentView.get_tournament_info()

        tournament = TournamentModel(**tournament_info)

        tournaments_folder = 'data/tournaments'
        os.makedirs(tournaments_folder, exist_ok=True)

        self.tournaments.append(tournament)
        tournament.save_to_file()

        print(f"Le tournoi '{tournament.name}' a été créé avec succès.")

    def select_tournament(self):
        """ Select a tournament from the list. """
        tournaments = self.load_tournaments()
        if not tournaments:
            print("No tournaments found.")
            return

        TournamentView.display_all_tournaments(tournaments)

        try:
            selected_index = int(input("Enter the index of the tournament you want to select (or -1 to cancel): "))
        except ValueError:
            print("Invalid input. Please enter a valid index.")
            return

        if selected_index == -1:
            print("Operation canceled.")
            return

        if 1 <= selected_index <= len(tournaments):
            selected_tournament = tournaments[selected_index - 1]

            if selected_tournament:
                TournamentView.display_selected_tournament_with_players(selected_tournament)
                self.current_tournament = selected_tournament
                self.manage_selected_tournament()
            else:
                print("Error loading selected tournament.")
        else:
            print("Invalid index. Please try again.")

    def manage_selected_tournament(self):
        """ Manage actions for the selected tournament. """
        while True:

            print("\nDo you want to register more players, start the tournament, or go back to the menu?"
                  "(R for register, S for start, M for menu):")
            user_choice = input().upper()

            if user_choice == 'R':
                self.register_players()
                TournamentView.display_selected_tournament_with_players(self.current_tournament)
            elif user_choice == 'S':
                self.start_tournament()
                break
            elif user_choice == 'M':
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def list_tournaments(self):
        """ List all tournaments. """
        tournament_folder = os.path.join(self.data_folder, 'tournaments')
        tournament_files = [f for f in os.listdir(tournament_folder) if f.endswith('.json')]

        tournaments_data = []
        for tournament_file in tournament_files:
            tournament_path = os.path.join(tournament_folder, tournament_file)
            try:
                tournament = TournamentModel.load_from_file(tournament_path)
                tournaments_data.append(tournament)
            except FileNotFoundError:
                print(f"File not found: {tournament_path}")

        TournamentView.display_all_tournaments(tournaments_data)

    def register_players(self):
        """ Register players for the selected tournament. """
        if not self.current_tournament:
            print("Please select a tournament first.")
            self.select_tournament()
            return

        while True:
            try:
                player_id = input("Enter the chess ID of the player you want to register (or -1 to cancel): ").upper()

                if player_id == '-1':
                    break

                player = self.player_controller.find_player_by_id(player_id)

                if player is None:
                    print(f"Player with chess ID {player_id} not found.")
                    continue

                result = self.current_tournament.register_player(
                         player_id, self.player_controller, self.current_tournament.name)

                if result is True:
                    print(f"The player {player.get_full_name()} with chess ID "
                          f"{player_id} is already registered for the tournament.")
                elif result is False:
                    print(f"The player {player.get_full_name()} with chess ID "
                          f"{player_id} has been successfully registered for the tournament.")
                elif result == 'full':
                    print("The tournament is already full. Cannot register more players.")
                else:
                    print(f"Player with chess ID {player_id} not found.")

                user_choice = input("Do you want to register another player? 'Y' for yes, 'N' for no: ").upper()
                if user_choice != 'Y':
                    break
            except ValueError:
                print("Invalid input. Please enter a valid chess ID.")

    def find_player_by_id(self, player_id):
        """ Find a player by their Chess ID. """
        return self.player_controller.find_player_by_id(player_id)

    def start_tournament(self):
        """ Start the selected tournament. """
        if len(self.current_tournament.players) < 8:
            print("You need at least 8 players to start the tournament.")
            return

        while self.current_tournament.current_round <= self.current_tournament.number_of_rounds:
            self.start_round()
            self.end_round()

        print("The tournament has ended.")

    def start_round(self):
        """ Start a new round in the tournament. """
        if self.current_tournament.current_round > self.current_tournament.number_of_rounds:
            print("The tournament is already finished.")
            return

        round_name = f"Round {self.current_tournament.current_round}"

        if self.current_tournament.current_round == 1:
            random.shuffle(self.current_tournament.players)

        round_instance = RoundModel(name=round_name)
        self.current_tournament.rounds.append(round_instance)
        self.start_round_timer()

        self.generate_pairs(round_instance)

        print(f"The {round_name} has started.")

        self.input_match_results(round_instance)

    def input_match_results(self, round_instance):
        """ Input match results for a round. """
        for match in round_instance.matches:
            print(f"Match: {match.match_data[0][0].get_full_name()} vs {match.match_data[1][0].get_full_name()}")

            while True:
                try:
                    player1_score = float(input("Enter score for Player 1 (0, 0.5, or 1): "))
                    player2_score = float(input("Enter score for Player 2 (0, 0.5, or 1): "))

                    if player1_score not in [0, 0.5, 1] or player2_score not in [0, 0.5, 1]:
                        raise ValueError("Invalid score. Please enter 0, 0.5, or 1.")

                    if (player1_score == 1 and player2_score == 1) or (player1_score == 0 and player2_score == 0):
                        raise ValueError("Invalid scores. If one player wins (1), the other must lose (0)."
                                         "If it's a draw, both scores should be 0.5.")

                    break

                except ValueError as e:
                    print(f"Error: {e}")

            match.set_scores(player1_score, player2_score)

    def generate_pairs(self, round_instance):
        """ Generate pairs for a round based on player standings. """
        sorted_players = sorted(self.current_tournament.players, key=lambda player: player.total_points, reverse=True)

        pairs = []
        used_players = set()
        for i in range(0, len(sorted_players), 2):
            player1 = sorted_players[i]
            player2 = sorted_players[i + 1]
            while (player1, player2) in used_players:
                i += 1
                player2 = sorted_players[i + 1]

            match_instance = MatchModel(player1, player2)
            pairs.append(match_instance)

            used_players.add((player1, player2))

        round_instance.matches = pairs

    def end_round(self):
        """ End the current round in the tournament. """
        if self.current_tournament.current_round > self.current_tournament.number_of_rounds:
            print("The tournament is already finished.")
            return

        round_instance = self.current_tournament.rounds[self.current_tournament.current_round - 1]
        if not isinstance(round_instance, RoundModel):
            print("Error: Invalid round instance.")
            return

        self.end_round_timer()
        round_instance.end_time = datetime.now()

        print(f"The {round_instance.name} has ended.")
        self.current_tournament.current_round += 1

        self.current_tournament.save_to_file()

    def start_round_timer(self):
        """ Start the timer for a round. """
        self.start_time = datetime.now()

    def end_round_timer(self):
        """ End the timer for a round. """
        self.end_time = datetime.now()
