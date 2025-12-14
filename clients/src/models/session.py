from pydantic import BaseModel, model_validator, field_validator
from src.config.session_config import SessionName, SessionType, CircuteShortName


class Session(BaseModel):
    circuit_key:int
    circuit_short_name: str
    country_code: str
    country_key: int
    date_end: str
    date_start: str
    gmt_offset: str
    location: str
    meeting_key: int
    session_key: int
    session_name: str
    session_type: str
    year: int

    @model_validator(mode='after')
    def validate_session_type(self):
        if self.session_type not in [ session_type.value for session_type in SessionType]:
            raise ValueError(f"Unknow Session Name: {self.session_type}")
        
        if self.session_name not in [ session_name.value for session_name in SessionName]:
            raise ValueError(f"Unknow Session Name: {self.session_name}")
        

    

