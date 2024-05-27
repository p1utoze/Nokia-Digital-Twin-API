from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Item, User, Station
from app.schemas import ItemCreate, ItemUpdate, StationBase, StationCreate, StationUpdate
from .base import apply_changes


class CRUDStation(CRUDBase[Station, StationCreate, StationUpdate]):
    def get_by_country(
        self, db: Session, *, country: str
    ) -> Optional[Station]:
        return db.query(self.model).filter(Station.country == country).all()

    def get_by_customer(
            self, db: Session, *, customer: str
    ) -> Optional[Station]:
        return db.query(self.model).filter(Station.customer == customer).all()


station = CRUDStation(Station)
