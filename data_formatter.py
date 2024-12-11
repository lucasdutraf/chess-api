from client import ChessClient
from datetime import date, timedelta
from collections import defaultdict
import pandas as pd


class DataFormatter:
    def __init__(self):
        self.chess_client = ChessClient()

    def _api_pattern_to_date(self, year: int, month: int, day: int) -> date:
        return date(year, month, day)

    def _find_ranking_based_on_date(
        self, desired_date: date, historical_ratings: list
    ) -> int:
        first_historical_rating_date = historical_ratings[0]["date"]

        if desired_date < first_historical_rating_date:
            return 0

        for historical_rating in historical_ratings:
            if historical_rating["date"] == desired_date:
                return historical_rating["rating"]

        last_historical_rating = desired_date - timedelta(days=1)

        return self._find_ranking_based_on_date(
            last_historical_rating, historical_ratings
        )

    def get_player_classical_rating_history(
        self, player_rating_histories: list
    ) -> list:
        for player_rating_history in player_rating_histories:
            if player_rating_history["name"] == "Classical":
                return player_rating_history

    def mount_historical_ratings_object(self, player_rating_history: list) -> list:
        historical_ratings = list()

        for record in player_rating_history:
            year = record[0]
            month = record[1] + 1  # months starts at 0
            day = record[2]
            rating = record[3]

            rating_history_object = {
                "date": self._api_pattern_to_date(year, month, day),
                "rating": rating,
            }

            historical_ratings.append(rating_history_object)

        return historical_ratings

    def generate_past_x_days_rating_object(
        self, days_before_today: int, player_rating_history: list
    ) -> list:
        past_x_days_rating_object = list()

        for days in range(days_before_today):
            days_from_today = date.today() - timedelta(days=days)
            rating = self._find_ranking_based_on_date(
                days_from_today, player_rating_history
            )

            rating_history_object = {"date": days_from_today, "rating": rating}

            past_x_days_rating_object.append(rating_history_object)

        return past_x_days_rating_object

    def get_past_x_days_classical_rating_object(
        self, username: str, days_before_today: int
    ) -> list:
        player_rating_history = self.chess_client.get_player_rating_history(username)

        classical_player_rating_history = self.get_player_classical_rating_history(
            player_rating_history
        )

        historical_ratings_object = self.mount_historical_ratings_object(
            classical_player_rating_history["points"]
        )

        past_x_day_ratings = self.generate_past_x_days_rating_object(
            days_before_today, historical_ratings_object
        )

        return reversed(past_x_day_ratings)

    def create_player_rating_history_dataframe(
        self, players_classical_history_rating: dict
    ) -> pd.DataFrame:
        dataframe_data = defaultdict(list)
        dataframe_data["username"] = players_classical_history_rating.keys()

        for username in players_classical_history_rating:
            for rating_history_input in players_classical_history_rating[username]:
                rating_history_date = rating_history_input["date"]
                rating_history_rating = rating_history_input["rating"]
                rating_history_date_string = rating_history_date.strftime("%Y-%m-%d")
                dataframe_data[rating_history_date_string].append(rating_history_rating)

        return pd.DataFrame(dataframe_data)
