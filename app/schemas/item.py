from typing import Optional, Tuple

from pydantic import BaseModel, ConfigDict
from pydantic.types import UUID4

from app.schemas.archivable import Archivable


# Shared properties
class ItemBase(BaseModel):
    name: Optional[str] = "New Item"
    description: Optional[str] = "A great description for a great item"


# Properties to receive via API on creation
class ItemCreate(ItemBase):
    pass


# Properties to receive via API on update
class ItemUpdate(ItemBase):
    pass


class ItemInDBBase(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4


# Additional properties to return via API
class Item(ItemInDBBase):
    pass


# Additional properties stored in DB
class ItemInDB(ItemInDBBase, Archivable):
    user_id: Optional[UUID4] = None

class StationBase(BaseModel):
    name: Optional[str]
    type: Optional[str]
    customer: Optional[str]
    project: Optional[str]
    coordinates: Optional[Tuple[float, float]]
    country: Optional[str]
    geo_region: Optional[str]


class StationOut(StationBase):
    pass

class StationCreate(StationBase):
    pass

class StationUpdate(StationBase):
    pass
