import requests
import json

# data processing
from functools import reduce
from .data_processing import get_team_standings

def fetch_fixtures(url: str) -> dict:
  world_cup_results_data: requests = requests.get(url=url, timeout=30) #TODO:: error handling
  return world_cup_results_data.json()

def write_data_to_file(data: dict, file_name: str) -> None:
  with open(f"./{file_name}", "w", encoding="utf-8") as file: #TODO:: error handling
    json.dump (data, file, indent=2)
    
def read_file_to_data(file_name: str) -> dict:
  file = open(f"./{file_name}")
  return json.load(file)

def reducer(prev, current) -> dict: #TODO:: error handling
  next_state = prev

  if current['Group']:
    group_name = current['Group']

    group_exists_in_next_state = next_state[group_name] if group_name in next_state else None
    group_games = [*group_exists_in_next_state['group_games'], current] if group_exists_in_next_state else [current]

    team_standings_exists_in_next_state = next_state[group_name]['team_standings'] if group_exists_in_next_state and 'team_standings' in next_state[group_name] else None
    new_team_standings = get_team_standings(team_standings_exists_in_next_state, current)
    team_standings = { **team_standings_exists_in_next_state, **new_team_standings } if team_standings_exists_in_next_state else new_team_standings

    next_state[group_name] = { 'group_games': group_games, 'team_standings': team_standings }
  else:
    next_stage_name = 'knockout_stage'

    group_exists_in_next_state = next_state[next_stage_name] if next_stage_name in next_state else None
    knockout_stage = [*group_exists_in_next_state, current] if group_exists_in_next_state else [current]
    
    next_state = { **next_state, next_stage_name: knockout_stage }

  return next_state

def group_teams(data: dict) -> dict:
  groups = reduce(reducer, data, {})
  print('grouped data dump')
  # print(json.dumps(groups))
  print(json.dumps(groups['Group A']['team_standings']))
  return groups
