from utils import fetch_fixtures, write_data_to_file, read_file_to_data, group_teams

LOCAL_ENV = True

url = "http://fixturedownload.com/feed/json/fifa-world-cup-2022"
file_name = "world-cup-2022.json"

response = fetch_fixtures(url)

if LOCAL_ENV: #TODO:: error handling
  data = read_file_to_data(file_name)
  group_teams(data)
else:
  write_data_to_file(response, file_name)
