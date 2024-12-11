from interface import Interface


if __name__ == "__main__":
    interface = Interface()
    interface.print_top_50_classical_players()
    interface.print_last_30_day_rating_for_top_player()
    interface.generate_rating_csv_for_top_50_classical_players()
