
class MainMenuView:
    def __init__(self):
        pass

    @staticmethod
    def show_menu():
        """Display the main menu options."""
        print("--------------------------------------------------------------------------")
        print("** MAIN MENU **", end="\n\n")
        print("1. Manage Players")
        print("2. Manage Tournaments")
        print("3. Generate Reports")
        print("0. Exit",    end="\n\n")
        print("--------------------------------------------------------------------------")
        try:
            choice = int(input("Enter your choice: "))
            return choice
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None
