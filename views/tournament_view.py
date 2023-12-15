import pyinputplus as pyip
from models.tournament_model import TournamentModel


class TournamentView:

    @staticmethod
    def display_tournament_menu():
        """Display the tournament menu options."""
        print("--------------------------------------------------------------------------")
        print("** TOURNAMENT MENU **", end="\n\n")
        print("1. Create Tournament")
        print("2. List Tournaments")
        print("3. Select Tournament")
        print("4. Register Players")
        print("0. Back to Main Menu", end="\n\n")
        print("--------------------------------------------------------------------------")

    @staticmethod
    def get_tournament_menu_choice():
        """Get the user's choice from the tournament menu."""
        choice = input("Enter your choice: ")
        try:
            choice = int(choice)
            print("DEBUG: Entered choice:", choice)
            return choice
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

    @staticmethod
    def display_tournaments(tournament_files):
        """Display a list of available tournaments."""
        print("\nList of Tournaments:")
        print("Index | Name | Location | Start Date | End Date")
        print("-----------------------------------------------")

        print("DEBUG: tournament_files =", tournament_files)

        for index, tournament_file in enumerate(tournament_files):
            tournament_data = TournamentModel.load_from_file(tournament_file)
            print(f"{index}. {tournament_data['name']} - {tournament_data['location']} - "
                  f"{tournament_data['start_date']} to {tournament_data['end_date']}")

    @staticmethod
    def display_selected_tournament(tournament_info):
        """Display information about a selected tournament."""
        if tournament_info:
            print("{:<20} {:<20} {:<20} {:<20}".format("Name", "Location", "Start Date", "End Date"))
            print("-" * 80)
            print("{:<20} {:<20} {:<20} {:<20}".format(
                tournament_info["Name"],
                tournament_info["Location"],
                tournament_info["Start Date"],
                tournament_info["End Date"]
            ))
            print("\n")
        else:
            print("Tournament not found.")

    @staticmethod
    def display_selected_tournament_with_players(tournament):
        """Display information about a selected tournament and its registered players."""
        print("Selected Tournament:")
        print(f"Name: {tournament.name}\nLocation: {tournament.location}\n"
              f"Start Date: {tournament.start_date}\nEnd Date: {tournament.end_date}")

        print("Registered Players:")
        for index, player in enumerate(tournament.players, start=1):
            print(f"{index}: {player.chess_id} {player.get_full_name()}")

    @staticmethod
    def get_tournament_info():
        """Get information about a new tournament from user input."""
        name = input("Enter tournament name: ")
        location = input("Enter tournament location: ")
        start_date = pyip.inputDate(prompt="Enter Start date (YYYY-MM-DD): ", formats=["%Y-%m-%d"])
        end_date = pyip.inputDate(prompt="Enter End date (YYYY-MM-DD): ", formats=["%Y-%m-%d"])
        description = input("Enter Tournament Description: ")
        return {
            'name': name,
            'location': location,
            'start_date': start_date,
            'end_date': end_date,
            'description': description
        }

    @staticmethod
    def display_created_tournament(tournament):
        """Display information about a newly created tournament."""
        print("\nYou have created the tournament:")
        print(f"Name: {tournament['name']}")
        print(f"Location: {tournament['location']}")
        print(f"Start Date: {tournament['start_date']}")
        print(f"End Date: {tournament['end_date']}\n")
        print("number of rounds is 4")

    @staticmethod
    def display_all_tournaments(tournaments):
        """Display a formatted list of all tournaments."""
        if not tournaments:
            print("No tournaments available.")
            return

        print("\nList of Tournaments:")
        print("{:<5} {:<20} {:<20} {:<20} {:<20}".format("Index", "Name", "Location", "Start Date", "End Date"))
        print("-" * 80)

        for index, tournament in enumerate(tournaments, start=1):
            print("{:<5} {:<20} {:<20} {:<20} {:<20}".format(
                index,
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date
            ))

        print("\n")
