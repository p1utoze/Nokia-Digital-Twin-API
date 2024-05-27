from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.exceptions import HTTPItemNotFound, HTTPNotEnoughPermissions

router = APIRouter()


@router.get("/country", response_model=List[schemas.StationOut])
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

@router.get("/country/{country}", response_model=List[schemas.StationOut])
def get_country(
    *,
    db: Session = Depends(deps.get_db),
    country: str,
) -> Any:
    """
    Get item by ID.
    """
    data = crud.station.get_by_country(db, country=country)
    if not data:
        raise HTTPException(status_code=404, detail="Item not found")

    return data


@router.get("/customers", response_model=List[schemas.StationOut])
def get_customer_stations(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get item by ID.
    """
    data = crud.station.get_by_customer(db, customer=current_user.customer)
    if not data:
        raise HTTPItemNotFound(current_user.language)
    if not current_user.is_admin and not current_user.customer:
        raise HTTPNotEnoughPermissions(current_user.language)

    return data

@router.get("/customers/{customer}", response_model=List[schemas.StationOut])
def get_customer_stations(
    *,
    db: Session = Depends(deps.get_db),
    customer: str,
) -> Any:
    """
    Get item by ID.
    """
    data = crud.station.get_by_customer(db, customer=customer)
    if not data:
        raise HTTPException(status_code=404, detail="Item not found")

    return data
