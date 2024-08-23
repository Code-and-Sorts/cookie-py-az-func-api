import uuid
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

def generate_utc_timestamp():
    return str(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

class BaseMeow(BaseModel):
    name: str
    type: Optional[str] = None

class MeowIdValidation(BaseModel):
    id: UUID

class Meow(BaseMeow):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    isDeleted: bool = Field(default=False)
    createdDate: str = Field(default_factory=lambda: generate_utc_timestamp())
    updatedDate: str = generate_utc_timestamp()

class MeowResponse(BaseMeow):
    id: str
