import json
import os

from dotenv import load_dotenv
from utils.validators import AllMatchesStatistics
from utils import fetch_fixtures, write_data_to_file, read_file_to_data, group_teams

load_dotenv()

PY_ENV = os.getenv('PY_ENV')
LOCAL_ENV = PY_ENV == 'local'

url = "http://fixturedownload.com/feed/json/fifa-world-cup-2022"
file_name = "world-cup-2022.json"

error_message = "[Error]: unable for fetch data"

def print_groups(data: dict):
  if data:
    write_data_to_file(data, file_name) if LOCAL_ENV else None

    # validate data
    validated_data = AllMatchesStatistics(data=data).data

    groups = group_teams(validated_data)
    # print(json.dumps(groups['Group A']['team_standings']))
    print(json.dumps(groups['team_standings']))
    print('group_teams(data):: -)')
  else:
    print(error_message)

if LOCAL_ENV:
  try:
    data = read_file_to_data(file_name)
  except:
    data = fetch_fixtures(url)

  print_groups(data)

else:
  data = fetch_fixtures(url)
  print_groups(data)
