from fastapi import APIRouter
from .globalSetings import get_global_settings
from .models.globalSettingsModel import GlobalSettings

from pydantic import Field
from models.responseModel import ResponseModel

router = APIRouter(prefix="/settings", tags=["Settings"])


class SettingsResponse(ResponseModel):
    """Response model for settings retrieval"""
    
    data: GlobalSettings = Field(description="Current settings data")


@router.get("/", summary="get settings", response_model=SettingsResponse)
def get_settings():
    """
    获取当前设置

    Returns:
        dict: 包含当前设置的响应
    """
    return SettingsResponse(data=get_global_settings())
