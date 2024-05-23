from typing import Any, List

from fastapi import APIRouter, Depends
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.exceptions import HTTPItemNotFound, HTTPNotEnoughPermissions

router = APIRouter()


@router.get("/", response_model=List[schemas.StationOut])
def get_country(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get item by ID.
    """
    data = crud.station.get_by_country(db, country=current_user.country)
    if not data:
        raise HTTPItemNotFound(current_user.language)
    if not current_user.is_admin and not current_user.country:
        raise HTTPNotEnoughPermissions(current_user.language)

    return data
