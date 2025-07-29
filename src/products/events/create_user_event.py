from datetime import datetime

from pydantic import BaseModel


class UserRegisterEvent(BaseModel):
    login: str
    password: str
    # event_time: datetime
