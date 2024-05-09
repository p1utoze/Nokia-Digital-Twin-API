from sqlalchemy import Column, ForeignKey, String, ARRAY, VARCHAR, Float
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

from .archivable import Archivable


class Item(Base, Archivable):
    name = Column(String)
    description = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("person.id"))


class Station(Base, Archivable):
    __tablename__ = "station"
    name = Column(String)
    type = Column(String)
    customer = Column(String)
    project = Column(String)
    coordinates = Column(ARRAY(Float))
    country = Column(String)
    geo_region = Column(VARCHAR)
