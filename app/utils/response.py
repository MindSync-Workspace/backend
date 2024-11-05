from fastapi.responses import JSONResponse
from datetime import datetime

def serialize_data(data):
    if isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    return data

def create_response(status_code: int, message: str, data: dict = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "meta": {
                "status": status_code,
                "message": message
            },
            "data": serialize_data(data) if data else {}
        }
    )
