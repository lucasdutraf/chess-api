import requests

from datetime import datetime

"""
List the top 50 classical chess players. Just print their usernames.

Print the rating history for the top chess player in classical chess for the last 30 calendar days. 

This can be in the format assuming today is Sep 15:  

- username, {Sep 15: 990, Sep 14: 991, ...,  Aug 17: 932, Aug 16: 1000}  

def print_last_30_day_rating_for_player() -> None:

 	pass

Key assumption: If a player doesn't play, then the score stays the same.

Create a CSV that shows the rating history for each of these 50 players, for the last 30 days.

a. The first column should be the player’s username.
b. The 2nd column should be the player’s rating 30 days ago. 
c. The 32nd column should be the player’s rating today.

"""


class ChessClient:
    def __init__(self):
        self.base_url = "https://lichess.org/api"

    def get_leaderboard(self, size: int, perf_type: str) -> list:
        url = f"{self.base_url}/player/top/{size}/{perf_type}"

        response = requests.get(url)

        players_list = response.json()["users"]

        return players_list

    def get_player_rating_history(self, username: str) -> list:
        url = f"{self.base_url}/user/{username}/rating-history"

        response = requests.get(url)

        rating_history = response.json()

        return rating_history


class DataFormatter:
    def __init__(self):
        pass


class Interface:
    def __init__(self):
        self.chess_client = ChessClient()

    def print_top_50_classical_players(self) -> None:
        chess_players = self.chess_client.get_leaderboard(50, "classical")

        for player in chess_players:
            username = player["username"]
            print(username)

    def print_last_30_day_rating_for_top_player(self) -> None:
        top_classical_chess_player = self.chess_client.get_leaderboard(1, "classical")

        top_classical_chess_player_username = top_classical_chess_player[0]["username"]

        player_rating_history = self.chess_client.get_player_rating_history(
            top_classical_chess_player_username
        )

        for elem in player_rating_history:
            if elem["name"] == "Classical":
                print(elem)

    def generate_rating_csv_for_top_50_classical_players() -> None: ...


if __name__ == "__main__":
    interface = Interface()
    interface.print_top_50_classical_players()
    # interface.print_last_30_day_rating_for_top_player()
