import requests


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
