import requests
import json

# data processing
from functools import reduce
from .data_processing import group_reducer

def fetch_fixtures(url: str) -> dict:
  try:
    world_cup_results_data: requests = requests.get(url=url, timeout=30)
    return world_cup_results_data.json()
  except:
    return None

def write_data_to_file(data: dict, file_name: str) -> None:
  try:
    with open(f"./{file_name}", "w", encoding="utf-8") as file: #TODO:: error handling
      json.dump(data, file, indent=2)
  except:
    print("[Error]: unable to create file")
    
def read_file_to_data(file_name: str) -> dict:
  file = open(f"./{file_name}")
  return json.load(file)

def group_teams(data: dict) -> dict:
  groups = reduce(group_reducer, data, {})
  return groups
