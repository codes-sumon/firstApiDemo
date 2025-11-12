from pydantic import BaseModel

class WorkStationBase(BaseModel):
    name: str
    location: str

class WorkStationCreate(WorkStationBase):
    pass

class WorkStationUpdate(BaseModel):
    name: str | None = None
    location: str | None = None

class WorkStationResponse(WorkStationBase):
    id: int
    model_config = {"from_attributes": True}
