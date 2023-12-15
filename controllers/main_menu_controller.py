from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.reports_controller import ReportsController
from views.main_menu_view import MainMenuView
from views.tournament_view import TournamentView
from views.player_view import PlayerView
from views.reports_view import ReportsView


class MainMenuController:
    """ Controller for the main menu functionality. """
    def __init__(self):
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.reports_controller = ReportsController()

    def show_main_menu(self):
        """ Display the main menu and return the user's choice. """
        return MainMenuView.show_menu()

    def run(self):
        """ Main loop to run the program based on user choices """

        while True:
            choice = self.show_main_menu()

            if choice == 1:
                self.manage_players()

            elif choice == 2:
                self.manage_tournaments()

            elif choice == 3:
                self.manage_reports()

            elif choice == 0:
                print("Exiting the application.")
                break

            else:
                print("Invalid choice. Please try again.")

    def manage_players(self):
        """ Sub-menu for managing player-related actions """
        while True:
            PlayerView.show_player_menu()
            player_choice = input("Enter your choice: ")

            if player_choice == '1':
                self.player_controller.create_player()
            elif player_choice == '2':
                self.player_controller.view_player_details()
            elif player_choice == '3':
                self.player_controller.list_players()
            elif player_choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_tournaments(self):
        """ Sub-menu for managing tournament-related actions. """
        while True:
            TournamentView.display_tournament_menu()
            tournament_choice = input("Enter your choice: ")

            if not tournament_choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            tournament_choice = int(tournament_choice)

            if tournament_choice == 1:
                self.tournament_controller.create_tournament()
            elif tournament_choice == 2:
                self.tournament_controller.list_tournaments()
            elif tournament_choice == 3:
                self.tournament_controller.select_tournament()
            elif tournament_choice == 4:
                self.tournament_controller.register_players()
            elif tournament_choice == 0:
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_reports(self):
        """ Sub-menu for managing report-related actions. """
        while True:
            ReportsView.display_reports_menu()
            report_choice = input("enter your choice:")

            if not report_choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            report_choice = int(report_choice)

            if report_choice == 1:
                self.reports_controller.generate_players_alphabetical_report()
            elif report_choice == 2:
                self.reports_controller.generate_all_tournaments_report()
            elif report_choice == 3:
                self.reports_controller.generate_tournament_info_report()
            elif report_choice == 4:
                self.reports_controller.generate_players_in_tournament_report()
            elif report_choice == 5:
                self.reports_controller.generate_tournament_rounds_and_matches_report()
            elif report_choice == 0:
                break
            else:
                print("Invalid choice. Please try again.")
