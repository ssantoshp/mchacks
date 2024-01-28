from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import datetime

from functools import lru_cache
from typing_extensions import Annotated
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore

from . import crud, models, schemas, config
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# App config
@lru_cache
def get_settings():
    return config.Settings()


# Mount static files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
fs_store = HttpExposedFileSystemStore(
    path="static",
    prefix="static/",
    host_url_getter=lambda: get_settings().host_url
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoints
@app.get('/foodsnaps/{snap_id}', response_model=schemas.FoodSnapResponse)
def get_food_snap(snap_id: int, db: Session = Depends(get_db)):
    db_snap = crud.get_food_snap(db, snap_id)
    if db_snap is None:
        raise HTTPException(status_code=404, detail="Snap not found")
    return crud.get_snap_resp(db, db_snap, fs_store)


@app.get('/foodsnaps/', response_model=list[schemas.FoodSnapResponse])
def get_food_snaps(
    start_date: datetime.date = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if start_date is None:
        start_date = datetime.datetime.now().date()

    db_snaps = crud.get_food_snaps_by_dt(db, start_date, limit, fs_store)
    return db_snaps


@app.post('/foodsnaps/', response_model=int)
def create_food_snap(food_pic: schemas.FoodPictureCreate, db: Session = Depends(get_db)):
    """TODO
    1. Add logic to create segmentations from the food picture
    2. Add logic to create intake entries for each segmentation
    3. Create a new food snap with the intake entries and the food picture
    """

    # For now, I will just create a dummy food snap
    return crud.create_dummy_food_snap(db, fs_store).id


@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "host_url": settings.host_url,
    }