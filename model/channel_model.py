from pydantic import BaseModel, Field
from typing import Optional, Dict
from enum import Enum
from bson import ObjectId

class ChannelType(str, Enum):
    EMAIL = "EMAIL"
    SLACK = "SLACK"
    SMS = "SMS"

class EmailConfig(BaseModel):
    from_address: Optional[str] = None

class SlackConfig(BaseModel):
    webhook_url: Optional[str] = None
    bot_access_token: Optional[str] = None

class ChannelConfig(BaseModel):
    email: Optional[EmailConfig] = None
    slack: Optional[SlackConfig] = None

class Channel(BaseModel):
    id: Optional[str] 
    name: str
    type: ChannelType
    config: ChannelConfig

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
