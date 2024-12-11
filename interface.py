from data_formatter import DataFormatter
from client import ChessClient


class OutputFormatter:
    def __init__(self): ...

    def top_players_usernames(self, chess_players: list) -> None:
        players_usernames_list = [
            chess_player["username"] for chess_player in chess_players
        ]
        players_usernames = ", ".join(players_usernames_list)

        print("\n\n")
        print(
            "1. List the top 50 classical chess players. Just print their usernames.\n"
        )
        print(players_usernames)
        print("\n\n")

    def player_historical_rating_output(
        self, username: str, historical_ratings: list
    ) -> None:
        date_rating_dict = dict()

        for historical_rating in historical_ratings:
            rating_date, rating = historical_rating["date"], historical_rating["rating"]
            date_string = rating_date.strftime("%d %B")

            date_rating_dict[date_string] = rating

        print("\n\n")
        print(
            "2. Print the rating history for the top chess player in classical chess for the last 30 calendar days.\n"
        )
        print("- " + username + ", " + str(date_rating_dict))
        print("\n\n")

    def create_player_rating_history(self) -> None:
        print("\n\n")
        print(
            "3. Create a CSV that shows the rating history for each of these 50 players, for the last 30 days.\n"
        )


class Interface:
    def __init__(self):
        self.chess_client = ChessClient()
        self.data_formatter = DataFormatter()
        self.output_formatter = OutputFormatter()

    def print_top_50_classical_players(self) -> None:
        chess_players = self.chess_client.get_leaderboard(50, "classical")

        self.output_formatter.top_players_usernames(chess_players)

    def print_last_30_day_rating_for_top_player(self) -> None:
        top_classical_chess_player = self.chess_client.get_leaderboard(1, "classical")

        top_classical_chess_player_username = top_classical_chess_player[0]["username"]

        past_30_day_ratings = (
            self.data_formatter.get_past_x_days_classical_rating_object(
                top_classical_chess_player_username, 30
            )
        )

        self.output_formatter.player_historical_rating_output(
            top_classical_chess_player_username, past_30_day_ratings
        )

    def generate_rating_csv_for_top_50_classical_players(self) -> None:
        players_classical_history_rating = dict()

        chess_players = self.chess_client.get_leaderboard(50, "classical")
        print("\n\n")
        print("Creating player_rating_history.csv... \n")

        for player in chess_players:
            username = player["username"]

            past_30_day_ratings = (
                self.data_formatter.get_past_x_days_classical_rating_object(
                    username, 30
                )
            )

            players_classical_history_rating[username] = past_30_day_ratings

        player_rating_df = self.data_formatter.create_player_rating_history_dataframe(
            players_classical_history_rating
        )

        player_rating_df.to_csv("player_rating_history.csv", index=False)

        print("player_rating_history.csv created!!")
        print("\n\n")
