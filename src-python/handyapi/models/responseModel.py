from pydantic import BaseModel, Field

class ResponseModel(BaseModel):
    """Base response model for API responses"""
    
    code: int = Field(default=200, description="Response status code")
    status: str = Field(default="success", description="Response status message")
    message: str = Field(default="Operation completed successfully", description="Detailed message about the response")
    # data: any = Field(default=None, description="Optional data payload for the response")

class NoDataResponseModel(ResponseModel):
    """Response model without data payload"""
    data: None = Field(default=None, description="No data payload")
