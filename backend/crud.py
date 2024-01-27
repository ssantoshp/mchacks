from sqlalchemy.orm import Session
from sqlalchemy.types import Date, DateTime

from . import models, schemas


def get_food_snap(db: Session, snap_id: int):
    return db.query(models.FoodSnap).filter(models.FoodSnap.id == snap_id).first()


def get_food_snaps_by_dt(db: Session, datetime: DateTime, limit = 100):
    return db.query(models.FoodSnap) \
            .filter(models.FoodSnap.created_at >= datetime) \
            .limit(limit) \
            .all()
