import requests
import json

# data processing
from functools import reduce

def fetch_fixtures(url: str) -> dict:
  world_cup_results_data: requests = requests.get(url=url, timeout=30) #TODO:: error handling
  return world_cup_results_data.json()

def write_data_to_file(data: dict, file_name: str) -> None:
  with open(f"./{file_name}", "w", encoding="utf-8") as file: #TODO:: error handling
    json.dump (data, file, indent=2)
    
def read_file_to_data(file_name: str) -> dict:
  file = open(f"./{file_name}")
  return json.load(file)

# data processing
def group_teams(data: dict) -> dict:
  def reducer(prev, current) -> dict: #TODO:: error handling
    next_state = prev

    if current['Group']:
      group_name = current['Group']

      group_exists_in_next_state = next_state[group_name] if group_name in next_state else None
      group_games = [*group_exists_in_next_state, current] if group_exists_in_next_state else [current]

      next_state[group_name] = group_games
    else:
      next_stage_name = 'knockout_stage'

      group_exists_in_next_state = next_state[next_stage_name] if next_stage_name in next_state else None
      knockout_stage = [*group_exists_in_next_state, current] if group_exists_in_next_state else [current]
      
      next_state = { **next_state, next_stage_name: knockout_stage }

    return next_state

  groups = reduce(reducer, data, {})
  # print(json.dumps(groups))
  return groups
