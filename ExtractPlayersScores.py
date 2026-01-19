import requests
import pandas as pd

# CONFIGURATION
LEAGUE_ID = "1181338081349599232"
SEASON = "2025"
# The 14 NFL teams that reached the 2025-26 Playoffs
PLAYOFF_TEAMS = [
    "DEN", "NE", "JAX", "PIT", "HOU", "BUF", "LAC",  # AFC
    "SEA", "CHI", "PHI", "CAR", "LAR", "SF", "GB"  # NFC
]
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


def calculate_score(stats, scoring_map):
    """Multiplies weekly stats by league scoring rules."""
    score = 0
    for stat_name, value in stats.items():
        if stat_name in scoring_map:
            score += value * scoring_map[stat_name]
    return round(score, 2)


def main():
    print("Step 1: Fetching league settings and player database...")
    league = get_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}")
    scoring_settings = league.get("scoring_settings", {})
    all_players = get_json("https://api.sleeper.app/v1/players/nfl")

    # Filter only players on NFL playoff teams
    playoff_player_map = {
        p_id: info for p_id, info in all_players.items()
        if info.get("team") in PLAYOFF_TEAMS
    }

    # Initialize data structure
    # { player_id: { "Name": ..., "Week 1": 0, ... } }
    results = {}
    for p_id, info in playoff_player_map.items():
        team = info.get("team")
        mapped_team = team_mapping.get(team)
        if mapped_team is None:
            continue
        position = info.get("position", [])
        if position is None:
            continue
        mapped_position = position_mapping.get(position)
        if mapped_position is not None:
            results[p_id] = {
                "Player Name": info.get("full_name"),
                "Position": mapped_position,
                "Team": mapped_team,
            }
            for w in range(1, 5):
                results[p_id][f"Week {w}"] = 0.0

    print("Step 2: Calculating league-specific scores for Weeks 19-22...")
    for week in range(1, 5):
        print(f"  Processing Week {week}...")
        # stats endpoint provides raw data (pass_yd, rush_td, etc)
        weekly_stats = get_json(f"https://api.sleeper.app/v1/stats/nfl/post/{SEASON}/{week}")

        for p_id, stats in weekly_stats.items():
            if p_id in results:
                # Apply your league's specific scoring to this player's stats
                results[p_id][f"Week {week}"] = calculate_score(stats, scoring_settings)

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(results, orient='index')

    # Clean up: Remove rows with no names (e.g. empty IDs) and sort
    df = df.dropna(subset=["Player Name"])
    cols = ["Player Name", "Position", "Team"] + [f"Week {i}" for i in range(1, 5)]
    df = df[cols]

    # Export
    filename = f"nfl_playoff_players_scores_{LEAGUE_ID}.csv"
    df.to_csv(filename, index=False)
    print(f"\nSuccess! Exported stats for {len(df)} players to {filename}")


if __name__ == "__main__":
    main()