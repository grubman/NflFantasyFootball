import requests
import pandas as pd

# CONFIGURATION
LEAGUE_ID = "1181338081349599232"
SEASON = "2025"
position_mapping = {
    "DE": "DL",
    "WR": "WR",
    "DB": "DB",
    "DL": "DL",
    "OL": None,
    "DT": "DL",
    "LS": None,
    "RB": "RB",
    "LB": "LB",
    "CB": "DB",
    "TE": "TE",
    "QB": "QB",
    "FB": "RB",
    "OT": None,
    "G": None,
    "T": None,
    "P": None,
    "C": None,
    "K": "K",
    "S": "DB",
    "ILB": "LB",
    "OLB": "LB",
    "SS": "DB",
    "OG": None,
    "FS": "DB",
    "NT": "DL",
    "D/ST": "D/ST"
}
team_mapping = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KC": "Kansas City Chiefs",
    "LAC": "Los Angeles Chargers",
    "LAR": "Los Angeles Rams",
    "LV": "Las Vegas Raiders",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE": "New England Patriots",
    "NO": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SEA": "Seattle Seahawks",
    "SF": "San Francisco 49ers",
    "TB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Commanders"
}


def get_json(url):
    response = requests.get(url)
    return response.json()


def main():
    print("Step 1: Fetching player database...")
    all_players = get_json("https://api.sleeper.app/v1/players/nfl")

    # Filter only players on NFL playoff teams
    playoff_player_map = {
        p_id: info for p_id, info in all_players.items()
    }

    results = {}
    for p_id, info in playoff_player_map.items():
        team = info.get("team")
        mapped_team = team_mapping.get(team)
        if mapped_team is None:
            continue
        fantasy_positions = info.get("fantasy_positions", [])
        if fantasy_positions is None:
            continue
        for pos in fantasy_positions:
            mapped_position = position_mapping.get(pos)
            if mapped_position is not None:
                # Use a unique key for each player-position combination
                key = f"{p_id}_{mapped_position}"
                results[key] = {
                    "Player Name": info.get("full_name"),
                    "Position": mapped_position,
                    "Team": mapped_team,
                }

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(results, orient='index')

    # Clean up: Remove rows with no names (e.g. empty IDs) and sort
    df = df.dropna(subset=["Player Name"])
    cols = ["Team", "Position", "Player Name"]
    df = df[cols]

    # Sort by Team and Position
    df = df.sort_values(by=["Team", "Position"])

    # Export
    filename = f"nfl_playoff_players_squads_{LEAGUE_ID}.csv"
    df.to_csv(filename, index=False)
    print(f"\nSuccess! Exported stats for {len(df)} players to {filename}")


if __name__ == "__main__":
    main()