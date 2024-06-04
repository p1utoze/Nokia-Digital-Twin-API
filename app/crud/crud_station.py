from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Item, User, Station
from app.schemas import ItemCreate, ItemUpdate, StationBase, StationCreate, StationUpdate
from .base import apply_changes


class CRUDStation(CRUDBase[Station, StationCreate, StationUpdate]):
    def get_by_country(
        self, db: Session, *, country: str, station_name: str = None
    ) -> Optional[Station]:
        query = db.query(self.model).filter(Station.country == country)
        if station_name:
            query = query.filter(Station.name == station_name)
        return query.all()

    def get_by_customer(
            self, db: Session, *, customer: str
    ) -> Optional[Station]:
        return db.query(self.model).filter(Station.customer == customer).all()

    def get_by_customer_and_country(
            self, db: Session, *, customer: str, country: str
    ) -> Optional[Station]:
        return db.query(self.model).filter(Station.customer == customer, Station.country == country).all()


station = CRUDStation(Station)
