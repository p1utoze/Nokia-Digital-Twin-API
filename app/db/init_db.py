from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app import crud, schemas, PROJECT_ROOT
from app.core.config import settings
from app.models.user import Role  # noqa: F401
import csv
from app.models import Station


# from app.db.session import engine
# from app.db import base

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly

def create_station_data(session: Session):
    data_path = PROJECT_ROOT / "data" / "Telecom Sites Dummy Data(Sites).csv"
    with open(data_path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for i, row in enumerate(reader):
            # print(row, row.__len__())
            coords = row[5].strip()[1:-1].split(", ")
            print(coords, coords.__len__() == 2)
            station = schemas.item.StationBase(
                name=row[1],
                type=row[2],
                customer=row[3],
                project=row[4],
                coordinates=coords if coords.__len__() == 2 else None,
                country=row[6],  # noqa: E231
                geo_region=row[7]
            )
            session.add(Station(**station.model_dump()))

        session.commit()


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # base.Base.metadata.create_all(bind=engine)
    # pass

    if not db.execute(select(Station)).all():
        create_station_data(db)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if user is None:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            country="USA",
            customer="NAM_AT_1",
        )
        user = crud.user.create(db, obj_in=user_in, role=Role.ADMIN)  # noqa: F841
