from client import ChessClient
from datetime import date, timedelta


class DataFormatter:
    def __init__(self): ...
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


class OutputFormatter:
    def __init__(self): ...

    def player_rating_output(self, username: str, historical_ratings: list) -> None:
        date_rating_dict = dict()

        for historical_rating in historical_ratings:
            rating_date, rating = historical_rating["date"], historical_rating["rating"]
            date_string = rating_date.strftime("%d %B")

            date_rating_dict[date_string] = rating

        print("- " + username + ", " + str(date_rating_dict))


class Interface:
    def __init__(self):
        self.chess_client = ChessClient()
        self.data_formatter = DataFormatter()
        self.output_formatter = OutputFormatter()

    def print_top_50_classical_players(self) -> None:
        chess_players = self.chess_client.get_leaderboard(50, "classical")

        for player in chess_players:
            username = player["username"]
            print(username)

    def print_last_30_day_rating_for_top_player(self) -> None:
        top_classical_chess_player = self.chess_client.get_leaderboard(1, "classical")

        top_classical_chess_player_username = top_classical_chess_player[0]["username"]

        player_rating_histories = self.chess_client.get_player_rating_history(
            top_classical_chess_player_username
        )

        for player_rating_history in player_rating_histories:
            if player_rating_history["name"] == "Classical":
                ratings = self.data_formatter.mount_historical_ratings_object(
                    player_rating_history["points"]
                )

                past_30_day_ratings = (
                    self.data_formatter.generate_past_x_days_rating_object(30, ratings)
                )

                self.output_formatter.player_rating_output(
                    top_classical_chess_player_username, past_30_day_ratings
                )

    def generate_rating_csv_for_top_50_classical_players() -> None: ...


if __name__ == "__main__":
    interface = Interface()
    # interface.print_top_50_classical_players()
    interface.print_last_30_day_rating_for_top_player()
