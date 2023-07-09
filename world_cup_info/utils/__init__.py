import requests
import json

# data processing
from functools import cmp_to_key, reduce
from .data_processing import group_reducer

def fetch_fixtures(url: str) -> dict:
  try:
    world_cup_results_data: requests = requests.get(url=url, timeout=30)
    return world_cup_results_data.json()
  except:
    return None

def write_data_to_file(data: dict, file_name: str) -> None:
  try:
    with open(f"./{file_name}", "w", encoding="utf-8") as file:
      json.dump(data, file, indent=2)
  except:
    print("[Error]: unable to create file")
    
def read_file_to_data(file_name: str) -> dict:
  file = open(f"./{file_name}")
  return json.load(file)

def compare_teams(item, nextItem):
  points_difference = item['points'] - nextItem['points']

  # if both teams have the same points, compare goals_difference
  if points_difference == 0:
    return item['goals_difference'] - nextItem['goals_difference']

  return points_difference

def group_teams(data: dict) -> dict:
  groups = reduce(group_reducer, data, {})

  team_standings = {}

  for key, values in groups.items():
    group = values if key != 'knockout_stage' else None
    
    if group:
      team_standings[key] = sorted(group['team_standings'].values(), key=cmp_to_key(compare_teams), reverse=True)

  groups['team_standings'] = team_standings

  return groups
