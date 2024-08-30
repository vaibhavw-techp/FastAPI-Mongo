from pydantic import BaseModel, Field
from typing import Optional
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

class ChannelRequest(BaseModel):
    name: str
    type: ChannelType
    config: ChannelConfig

class ChannelUpdateRequest(BaseModel):
    name: Optional[str] = None
    config: Optional[ChannelConfig] = None

class ChannelResponse(BaseModel):
    id: str
    name: str
    type: ChannelType
    config: ChannelConfig

    class Config:
        orm_mode = True
