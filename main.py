from client import ChessClient
from datetime import date, timedelta


class DataFormatter:
    def __init__(self):
        pass

    def _api_pattern_to_date(self, year: int, month: int, day: int) -> date:
        return date(year, month, day)

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

    def filter_historical_ratings(
        self, historical_ratings: list, days_before_today: int
    ) -> list:
        days_from_today_object = date.today() - timedelta(days=days_before_today)

        filtered_historical_ratings = list()

        for historical_rating in historical_ratings:
            if historical_ratings["date"] >= days_from_today_object:
                filtered_historical_ratings.append(historical_rating)

        return filtered_historical_ratings


class Interface:
    def __init__(self):
        self.chess_client = ChessClient()
        self.data_formatter = DataFormatter()

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
                obj = self.data_formatter.mount_historical_ratings_object(
                    elem["points"]
                )

                for elem in obj:
                    print(elem)

    def generate_rating_csv_for_top_50_classical_players() -> None: ...


if __name__ == "__main__":
    interface = Interface()
    # interface.print_top_50_classical_players()
    interface.print_last_30_day_rating_for_top_player()
