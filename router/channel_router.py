from uuid import UUID
from fastapi import HTTPException, logger, status, APIRouter
from typing import List
from config.database import get_db
from schema.channel_schema import ChannelResponse, ChannelRequest, ChannelUpdateRequest
from service.channel_service import create_channel, fetch_all_channels, fetch_channel_by_id, delete_channel_by_id, update_channel_by_id

router = APIRouter(prefix="/v1/channels", tags=["channels"])


db = get_db()

@router.get("/", response_model=List[ChannelResponse])
def get_all_channels():
    channels = fetch_all_channels()
    return channels  

@router.get("/{id}", response_model=ChannelResponse)
def get_channel_by_id(id: UUID):
    try:
        channel = fetch_channel_by_id(channel_id=id)
        if not channel:
            logger.info(f"Channel with ID {id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
        return channel
    except HTTPException as e:
        raise e  
    except Exception as e:
        logger.error(f"Unexpected error while Get channel by Id: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        
@router.post("/", response_model=ChannelResponse)
def create_channel_route(channel_request: ChannelRequest):
    try:
        channel = create_channel(channel_request)
        return channel
    except Exception as e:
        logger.error(f"Error in create_channel_route: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@router.delete("/{id}", response_model=dict)
def delete_channel_route(id: UUID):
    response = delete_channel_by_id(channel_id=id)
    return response

@router.put("/{id}", response_model=ChannelResponse)
def update_channel_route(id: UUID, update_request: ChannelUpdateRequest):
    update_data = update_request.dict(exclude_unset=True)
    updated_channel = update_channel_by_id(channel_id=id, update_data=update_data)
    return updated_channel
