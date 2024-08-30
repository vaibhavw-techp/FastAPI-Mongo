from fastapi import APIRouter
from schema.channel_schema import ChannelRequest, ChannelUpdateRequest, ChannelResponse

router = APIRouter(prefix="/v1/channels", tags=["channels"])


