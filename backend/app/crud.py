from sqlalchemy.orm import Session
from sqlalchemy.types import Date
from sqlalchemy_imageattach.context import store_context
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore

from . import models, schemas


def get_snap_resp(db: Session, snap_db: models.FoodSnap, fs_store: HttpExposedFileSystemStore) -> schemas.FoodSnapResponse:
    db_pic = get_food_pic_by_snap_id(db, snap_db.id, fs_store)
    db_intakes = get_intakes_resp_by_snap_id(db, snap_db.id, fs_store)
    return schemas.FoodSnapResponse(
        **snap_db.__dict__,
        food_pic=db_pic.locate(fs_store),
        food_entries=db_intakes
    )


def get_food_snap(db: Session, snap_id: int) -> models.FoodSnap:
    return db.query(models.FoodSnap).filter(models.FoodSnap.id == snap_id).first()


def get_food_snaps_by_dt(db: Session, datetime: Date, limit = 100, fs_store: HttpExposedFileSystemStore = None) -> list[schemas.FoodSnapResponse]:
    snap_dbs = db.query(models.FoodSnap) \
            .filter(models.FoodSnap.created_at >= datetime) \
            .order_by(models.FoodSnap.created_at.desc()) \
            .limit(limit) \
            .all()
    return [get_snap_resp(db, snap_db, fs_store) for snap_db in snap_dbs]

def get_food_pic_by_snap_id(db: Session, snap_id: int, fs_store: HttpExposedFileSystemStore):
    with store_context(fs_store):
        return db.query(models.FoodPicture) \
            .filter(models.FoodPicture.snap_id == snap_id) \
            .first()

def get_intakes_by_snap_id(db: Session, snap_id: int):
    return db.query(models.IntakeEntry) \
        .filter(models.IntakeEntry.snap_id == snap_id) \
        .order_by(models.IntakeEntry.updated_at.desc()) \
        .all()

def get_intakes_resp_by_snap_id(
    db: Session,
    snap_id: int,
    fs_store: HttpExposedFileSystemStore
) -> list[schemas.IntakeEntryResponse]:
    db_intakes = get_intakes_by_snap_id(db, snap_id)
    return [
        schemas.IntakeEntryResponse(
            **intake.__dict__,
            food_seg=intake.food_seg.locate(fs_store)
        )
        for intake in db_intakes
    ]

def create_dummy_food_snap(db: Session, fs_store: HttpExposedFileSystemStore):
    db_snap = models.FoodSnap()

    db_intake_entry_1 = models.IntakeEntry(
        name='apples',
        serving_size=1,
        calories=100,
        proteins=10,
        fat=10,
        carbs=10,
        snap=db_snap
    )

    db_intake_entry_2 = models.IntakeEntry(
        name='bananas',
        serving_size=1,
        calories=100,
        proteins=10,
        fat=10,
        carbs=10,
        snap=db_snap
    )

    with store_context(fs_store):
        with open('static/dummy/food_picture.png', 'rb') as f:
            db_snap.food_pic.from_file(f)

        with open('static/dummy/mask1.png', 'rb') as f:
            db_intake_entry_1.food_seg.from_file(f)
        
        with open('static/dummy/mask2.png', 'rb') as f:
            db_intake_entry_2.food_seg.from_file(f)

        db.add(db_snap)
        db.commit()
        db.refresh(db_snap)
    
    return db_snap

def create_segmentation(db: Session, segmentation: schemas.FoodSegmentationCreate):
    db_seg = models.FoodSegmentation(**segmentation.model_dump())
    db.add(db_seg)
    db.commit()
    db.refresh(db_seg)
    return db_seg

def create_food_pic(db: Session, food_pic: schemas.FoodPictureCreate):
    db_pic = models.FoodPicture(**food_pic.model_dump())
    db.add(db_pic)
    db.commit()
    db.refresh(db_pic)
    return db_pic