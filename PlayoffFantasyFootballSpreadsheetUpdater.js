// ==========================================
// CONFIGURATION
// ==========================================
const LEAGUE_ID = "1181338081349599232";
const SEASON = "2025";

const PLAYOFF_TEAMS = [
  "DEN", "NE", "JAX", "PIT", "HOU", "BUF", "LAC",  // AFC
  "SEA", "CHI", "PHI", "CAR", "LAR", "SF", "GB"    // NFC
];

const POSITION_MAPPING = {
  "DE": "DL", "WR": "WR", "DB": "DB", "DL": "DL", "OL": null,
  "DT": "DL", "LS": null, "RB": "RB", "LB": "LB", "CB": "DB",
  "TE": "TE", "QB": "QB", "FB": "RB", "OT": null, "G": null,
  "T": null, "P": null, "C": null, "K": "K", "S": "DB",
  "ILB": "LB", "OLB": "LB", "SS": "DB", "OG": null, "FS": "DB",
  "NT": "DL", "DEF": "D/ST"
};

const TEAM_MAPPING = {
  "ARI": "Arizona Cardinals", "ATL": "Atlanta Falcons", "BAL": "Baltimore Ravens",
  "BUF": "Buffalo Bills", "CAR": "Carolina Panthers", "CHI": "Chicago Bears",
  "CIN": "Cincinnati Bengals", "CLE": "Cleveland Browns", "DAL": "Dallas Cowboys",
  "DEN": "Denver Broncos", "DET": "Detroit Lions", "GB": "Green Bay Packers",
  "HOU": "Houston Texans", "IND": "Indianapolis Colts", "JAX": "Jacksonville Jaguars",
  "KC": "Kansas City Chiefs", "LAC": "Los Angeles Chargers", "LAR": "Los Angeles Rams",
  "LV": "Las Vegas Raiders", "MIA": "Miami Dolphins", "MIN": "Minnesota Vikings",
  "NE": "New England Patriots", "NO": "New Orleans Saints", "NYG": "New York Giants",
  "NYJ": "New York Jets", "PHI": "Philadelphia Eagles", "PIT": "Pittsburgh Steelers",
  "SEA": "Seattle Seahawks", "SF": "San Francisco 49ers", "TB": "Tampa Bay Buccaneers",
  "TEN": "Tennessee Titans", "WAS": "Washington Commanders"
};

// ==========================================
// FUNCTION 1: INITIALIZE ROSTER (Run Once)
// ==========================================
function updatePlayoffRoster() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let dbSheet = ss.getSheetByName("DB_Players");
  if (!dbSheet) {
    dbSheet = ss.insertSheet("DB_Players");
    dbSheet.hideSheet();
  }

  console.log("Fetching player database...");
  const playersData = fetchJson("https://api.sleeper.app/v1/players/nfl");

  // DB Columns: [ID, Name, Position, Team Abbr, Team Full Name]
  const output = [];
  output.push(["Player ID", "Team", "Position", "Full Name"]);

  const playerIds = Object.keys(playersData);

  playerIds.forEach(pid => {
    const p = playersData[pid];

    // Check if player is in playoff teams
    if (PLAYOFF_TEAMS.includes(p.team)) {

      const positionsToCheck = p.fantasy_positions || [p.position];

      positionsToCheck.forEach(pos => {
        const mappedPos = POSITION_MAPPING[pos];
        const mappedTeam = TEAM_MAPPING[p.team];

        if (mappedPos && mappedTeam) {
           // Use Team Name if position is D/ST
           const fullName = mappedPos == "D/ST" ? mappedTeam : p.full_name;

           output.push([
            pid,
            mappedTeam,
            mappedPos,
            fullName
          ]);
        }
      });
    }
  });

  dbSheet.clear();
  if (output.length > 0) {
    dbSheet.getRange(1, 1, output.length, output[0].length).setValues(output);
  }
  console.log(`Success! Saved ${output.length - 1} entries to DB_Players.`);
}

// ==========================================
// FUNCTION 2: CALCULATE STATS (Run Daily)
// ==========================================
function calculatePlayoffStats() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // 1. Get Settings & Data
  const leagueData = fetchJson(`https://api.sleeper.app/v1/league/${LEAGUE_ID}`);
  const scoringSettings = leagueData.scoring_settings || {};

  const dbSheet = ss.getSheetByName("DB_Players");
  if (!dbSheet) {
    Browser.msgBox("Error: Please run 'updatePlayoffRoster' first!");
    return;
  }

  const rosterData = dbSheet.getDataRange().getValues();
  rosterData.shift(); // Remove header

  // 2. Fetch All Stats First
  const statsCache = {};

  for (let w = 1; w <= 4; w++) {
    console.log(`Fetching stats for Week ${w}...`);
    try {
      const weeklyStats = fetchJson(`https://api.sleeper.app/v1/stats/nfl/post/${SEASON}/${w}`);

      Object.keys(weeklyStats).forEach(pid => {
        if (!statsCache[pid]) statsCache[pid] = {1:0, 2:0, 3:0, 4:0};
        const score = calculateScore(weeklyStats[pid], scoringSettings);
        statsCache[pid][w] = score;
      });

    } catch (e) {
      console.log(`Week ${w} stats not available yet.`);
    }
  }

  // 3. Build Output (With User Defined Column Order)
  const output = [];

  // HEADERS
  output.push(["ID", "Team", "Position", "Player Name", "Week 1", "Week 2", "Week 3", "Week 4", "Total"]);

  rosterData.forEach(row => {
    // Mapping from DB_Players sheet
    const pid = row[0];
    const name = row[3];
    const pos = row[2];
    // row[3] is Team Abbr (e.g. BUF)
    const teamFull = row[1]; // Team Full Name (e.g. Buffalo Bills)

    const pStats = statsCache[pid] || {1:0, 2:0, 3:0, 4:0};
    const total = pStats[1] + pStats[2] + pStats[3] + pStats[4];

    // ROWS
    output.push([
      pid,        // ID
      teamFull,   // Full Team Name
      pos,        // Position
      name,       // Player Name
      pStats[1],
      pStats[2],
      pStats[3],
      pStats[4],
      total
    ]);
  });

  // 4. Write to Sheet
  let statsSheet = ss.getSheetByName("Playoff_Stats");
  if (!statsSheet) statsSheet = ss.insertSheet("Playoff_Stats");

  statsSheet.clear();
  statsSheet.getRange(1, 1, output.length, output[0].length).setValues(output);

  SpreadsheetApp.getActiveSpreadsheet().toast("Playoff stats updated!", "Success", 5);
}

function calculateScore(stats, rules) {
  let score = 0;

  for (const [key, value] of Object.entries(stats)) {
    if (rules[key]) score += value * rules[key];
  }

  return Number(score.toFixed(2));
}

function fetchJson(url) {
  const params = {muteHttpExceptions: true};
  const response = UrlFetchApp.fetch(url, params);
  if (response.getResponseCode() !== 200) return {};
  return JSON.parse(response.getContentText());
}