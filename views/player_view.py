import pyinputplus as pyip
import re


class PlayerView:

    @staticmethod
    def show_player_menu():
        """Display the player menu options."""
        print("--------------------------------------------------------------------------")
        print("** PLAYER MENU **", end="\n\n")
        print("1. Add Player")
        print("2. View Player Details")
        print("3. List Players")
        print("0. Back to Main Menu", end="\n\n")
        print("--------------------------------------------------------------------------")

    @staticmethod
    def get_player_info():
        """Get player information from user input."""
        chess_id_regex = r'^[A-Za-z]{2}\d{5}$'

        def input_valid_name(prompt):
            return pyip.inputStr(prompt=prompt, allowRegexes=[r'^[A-Za-z]+$'],
                                 blockRegexes=[r'[0-9&@=£%<>,;:/§\^\$\\\|\{\}\[\]\(\)\?\#\!\+\*\.]'])

        first_name = input_valid_name("Enter the player's first name (letters only): ")
        last_name = input_valid_name("Enter the player's last name (letters only): ")

        birth_date = pyip.inputDate(prompt="Enter birth date (YYYY-MM-DD): ", formats=["%Y-%m-%d"])
        while True:
            chess_id = pyip.inputStr(prompt="Enter chess ID (for exemple :AB12345):  ").upper()
            if re.match(chess_id_regex, chess_id):
                break
            else:
                print("Invalid chess ID. Please enter a valid chess ID.")

        return {
            'first_name': first_name,
            'last_name': last_name,
            'birth_date': birth_date,
            'chess_id': chess_id
        }

    @staticmethod
    def get_player_id():
        """Get the chess ID of the player."""
        return input("Enter chess ID of the player: ")

    @staticmethod
    def show_player_registered_confirmation(player):
        """Display confirmation for successful player registration."""
        print("Player successfully registered:")
        print(f"Full Name: {player.get_full_name()}")
        print(f"Birth Date: {player.birth_date}")
        print(f"Chess ID: {player.chess_id}")

    @staticmethod
    def display_players(players):
        """Display a formatted list of players."""
        print("{:<10} {:<15} {:<15} {:<20}".format("Chess ID", "First Name", "Last Name", "Birth Date"))
        print("-" * 70)
        for player in players:
            if player:
                print("{:<10} {:<15} {:<15} {:<20}".format(
                       player.chess_id, player.first_name, player.last_name, str(player.birth_date)))
            else:
                print("Player not found.")
