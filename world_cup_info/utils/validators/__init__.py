import datetime
from typing import List
from pydantic import BaseModel

class MatchStatistics(BaseModel):
  MatchNumber: int  
  RoundNumber: int  
  DateUtc: str
  Location: str
  HomeTeam: str
  AwayTeam: str
  Group: str | None
  HomeTeamScore: int  
  AwayTeamScore: int  

class AllMatchesStatistics(BaseModel):
  data: List[MatchStatistics]
