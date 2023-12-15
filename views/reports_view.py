class ReportsView:

    @staticmethod
    def display_reports_menu():
        """Display the reports menu options."""
        print("--------------------------------------------------------------------------")
        print("** REPORTS MENU **", end="\n\n")
        print("1. players_alphabetical_report")
        print("2. all_tournaments_report")
        print("3. tournament_info_report")
        print("4. players_in_tournament_report")
        print("5. tournament_rounds_and_matches_report")
        print("0. Back to Main Menu", end="\n\n")
        print("--------------------------------------------------------------------------")

    @staticmethod
    def display_all_tournaments(tournaments):
        """Display a list of all tournaments."""
        if not tournaments:
            print("No tournaments available.")
            return

        print("\nList of Tournaments:")
        print("{:<20} {:<20} {:<20} {:<20}".format("Name", "Location", "Start Date", "End Date"))
        print("-" * 80)

        for tournament in (tournaments):
            print("{:<20} {:<20} {:<20} {:<20}".format(

                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date
            ))

        print("\n")

    @staticmethod
    def display_selected_tournament(tournament):
        """Display information about a selected tournament."""
        print("Tournament Information:")
        print(f"Name: {tournament.name}")
        print(f"Location: {tournament.location}")
        print(f"Start Date: {tournament.start_date}")
        print(f"End Date: {tournament.end_date}")

    @staticmethod
    def display_players(players):
        """Display a formatted list of players."""
        sorted_players = sorted(players, key=lambda x: (x.first_name, x.last_name))
        print("{:<10} {:<15} {:<15} {:<20}".format("Chess ID", "First Name", "Last Name", "Birth Date"))
        print("-" * 70)
        for player in sorted_players:
            if player:
                print("{:<10} {:<15} {:<15} {:<20}".format(
                       player.chess_id, player.first_name, player.last_name, str(player.birth_date)))
            else:
                print("Player not found.")

    @staticmethod
    def display_tournament_round_and_matches(tournament_name, round_num, matches):
        """Display information about tournament rounds and matches."""
        print(f"\nRound {round_num} Matches for Tournament '{tournament_name}':")
        print("-" * 40)

        for match_num, match in enumerate(matches, start=1):
            player1 = f"{match.match_data[0][0].first_name} {match.match_data[0][0].last_name}"
            player2 = f"{match.match_data[1][0].first_name} {match.match_data[1][0].last_name}"
            score1, score2 = match.match_data[0][1], match.match_data[1][1]

            print(f"Match {match_num}: Player: {player1}, score: {score1} vs Player: {player2}, score: {score2}")

        print("\n")
