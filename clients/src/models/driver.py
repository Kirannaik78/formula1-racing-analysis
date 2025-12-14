from pydantic import BaseModel, AnyUrl
from typing import Optional


class Driver(BaseModel):
    broadcast_name: str
    country_code: Optional[str]
    driver_number: int
    first_name: str
    full_name: str
    headshot_url: Optional[AnyUrl]
    last_name: str
    meeting_key: int
    name_acronym: str
    session_key: int
    team_colour: str
    team_name: str
