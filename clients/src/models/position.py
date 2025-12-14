from pydantic import BaseModel
from typing import Optional


class Position(BaseModel):
    date: str
    driver_number: int
    meeting_key: int
    position: int
    session_key: int