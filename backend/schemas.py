from typing import Union

from pydantic import BaseModel


class FoodSegmentationBase(BaseModel):
    pass

class FoodSegmentationCreate(FoodSegmentationBase):
    pass

class FoodSegmentation(FoodSegmentationBase):
    intake_entry_id: int
    class Config:
        orm_mode = True


class FoodPictureBase(BaseModel):
    pass

class FoodPictureCreate(FoodPictureBase):
    pass

class FoodPicture(FoodPictureBase):
    snap_id: int
    class Config:
        orm_mode = True


class IntakeEntryBase(BaseModel):
    name: str
    food_seg: FoodSegmentation
    serving_size: float
    calories: float
    protein: float
    fat: float
    carbs: float

class IntakeEntryCreate(IntakeEntryBase):
    pass

class IntakeEntry(IntakeEntryBase):
    id: int
    created_at: str
    updated_at: str
    snap_id: int
    class Config:
        orm_mode = True


class FoodSnapBase(BaseModel):
    pass

class FoodSnapCreate(FoodSnapBase):
    food_pic: FoodPicture

class FoodSnap(FoodSnapBase):
    id: int
    created_at: str
    food_entries: list[IntakeEntry] = []
    class Config:
        orm_mode = True
