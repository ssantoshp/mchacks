from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

from .database import Base


class FoodSnap(Base):
    __tablename__ = "food_snaps"

    id = Column(Integer, primary_key=True, index=True)
    food_pic = image_attachment("FoodPicture", uselist=False, back_populates="snap")
    food_entries = relationship("IntakeEntry", uselist=True, back_populates="snap")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FoodPicture(Base, Image):
    __tablename__ = "food_pictures"

    snap_id = Column(Integer, ForeignKey("food_snaps.id"), primary_key=True)
    snap = relationship("FoodSnap", back_populates="food_pic")


class FoodSegmentation(Base, Image):
    __tablename__ = "food_segmentations"

    intake_entry_id = Column(Integer, ForeignKey("intake_entries.id"), primary_key=True)
    intake_entry = relationship("IntakeEntry", back_populates="food_seg")


class IntakeEntry(Base):
    __tablename__ = "intake_entries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serving_size = Column(Float, nullable=False, default=0)
    calories = Column(Float, nullable=False, default=0)
    carbs = Column(Float, nullable=False, default=0)
    proteins = Column(Float, nullable=False, default=0)
    fat = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    snap_id = Column(Integer, ForeignKey("food_snaps.id"))
    snap = relationship("FoodSnap", back_populates="food_entries")
    food_seg = image_attachment("FoodSegmentation", uselist=False, back_populates="intake_entry")