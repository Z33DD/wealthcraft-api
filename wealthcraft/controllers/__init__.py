from typing import Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    message: Optional[str] = "Done!"
