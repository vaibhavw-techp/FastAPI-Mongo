from typing import List
from fastapi import HTTPException, logger, status
import uuid
from config.database import get_db
from schema.channel_schema import ChannelRequest, ChannelResponse
from model.channel_model import Channel

db = get_db()  

def create_channel(channel_request: ChannelRequest) -> ChannelResponse:
    try:
        channel_data = channel_request.dict()
        channel_id = uuid.uuid4()  # UUID generation
        channel_data["id"] = str(channel_id)  

        db.insert_one(channel_data)
        
        created_channel = db.find_one({"id": str(channel_id)})
        if not created_channel:
            raise ValueError("Failed to create a channel!")
            
        return map_channel_to_response(created_channel)

    except Exception as e:
        logger.error(f"Error creating channel: {e}")
        raise

def fetch_all_channels() -> List[ChannelResponse]:
    channels = db.find()
    result = []
    for channel_data in channels:
        channel = Channel(**channel_data)
        result.append(channel.to_response())
    return result

def fetch_channel_by_id(channel_id: uuid.UUID) -> ChannelResponse:
    try:
        channel = db.find_one({"id": str(channel_id)})
        if channel:
            return map_channel_to_response(channel)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    except Exception as e:
        logger.error(f"Error occurred while fetching channel by Id: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
def update_channel_by_id(channel_id: uuid.UUID, update_data: dict) -> ChannelResponse:
    try:
        existing_channel = db.find_one({"id": str(channel_id)})

        if not existing_channel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

        updated_data = {**existing_channel, **update_data}

        db.update_one({"id": str(channel_id)}, {"$set": updated_data})

        updated_channel = db.find_one({"id": str(channel_id)})

        return map_channel_to_response(updated_channel)
    
    except Exception as e:
        logger.error(f"Error occured while updating channel: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


def delete_channel_by_id(channel_id: uuid.UUID) -> dict:
    try:
        db.delete_one({"id": str(channel_id)})

        return {"detail": "Channel deleted successfully"}
    except Exception as e:
        logger.error(f"Error occured while deleting channel: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

def map_channel_to_response(channel_data: dict) -> ChannelResponse:
    return ChannelResponse(
        id=uuid.UUID(channel_data["id"]),
        name=channel_data["name"],
        type=channel_data["type"],
        config=channel_data["config"]
    )

