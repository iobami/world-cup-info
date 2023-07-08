def get_team_stats(data: dict) -> dict:
  gs = data['goals_scored']
  gc = data['goals_conceded']
  gd = gs - gc

  win, loss, draw  = 0, 0, 0
  points = 0

  if gs > gc:
    win = 1
    points = 3

  if gs < gc:
    loss = 1
    points = 0

  if gs == gc:
    draw = 1
    points = 1

  stats = {
    "country": data['country'],
    "played": 1,
    "wins": win,
    "loses": loss,
    "draws": draw,
    "goals_scored": gs,
    "goals_conceded": gc,
    "goal_difference": gd,
    "points": points
  }

  return stats

def update_team_stats(previous_team_stats: dict, team_stats: dict) -> dict:
  return {
    'played': previous_team_stats['played'] + team_stats['played'],
    'wins': previous_team_stats['wins'] + team_stats['wins'],
    'loses': previous_team_stats['loses'] + team_stats['loses'],
    'draws': previous_team_stats['draws'] + team_stats['draws'],
    'goals_scored': previous_team_stats['goals_scored'] + team_stats['goals_scored'],
    'goals_conceded': previous_team_stats['goals_conceded'] + team_stats['goals_conceded'],
    'goal_difference': previous_team_stats['goal_difference'] + team_stats['goal_difference'],
    'points': previous_team_stats['points'] + team_stats['points']
  }

def get_team_standings(next_state: dict, current_match: dict) -> dict:
  current_team_standings = next_state if next_state else {}

  home_team = current_match['HomeTeam']
  home_team_score = current_match['HomeTeamScore']
  away_team = current_match['AwayTeam']
  away_team_score = current_match['AwayTeamScore']

  if home_team in current_team_standings:
    previous_team_stats = current_team_standings[home_team]
    team_stats = get_team_stats({ 'country': home_team, 'goals_scored': home_team_score, 'goals_conceded': away_team_score })
    
    current_team_standings[home_team] = update_team_stats(previous_team_stats, team_stats)
  else:
    current_team_standings[home_team] = get_team_stats({ 'country': home_team, 'goals_scored': home_team_score, 'goals_conceded': away_team_score })

  if away_team in current_team_standings:
    previous_team_stats = current_team_standings[away_team]
    team_stats = get_team_stats({ 'country': away_team, 'goals_scored': away_team_score, 'goals_conceded': home_team_score })
    
    current_team_standings[away_team] = update_team_stats(previous_team_stats, team_stats)
  else:
    current_team_standings[away_team] = get_team_stats({ 'country': away_team, 'goals_scored': away_team_score, 'goals_conceded': home_team_score })

  return current_team_standings
