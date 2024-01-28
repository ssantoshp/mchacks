import datetime

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
    serving_size: float
    calories: float
    proteins: float
    fat: float
    carbs: float

class IntakeEntryCreate(IntakeEntryBase):
    food_seg: FoodSegmentation

class IntakeEntry(IntakeEntryBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    snap_id: int
    class Config:
        orm_mode = True

class IntakeEntryResponse(IntakeEntry):
    food_seg: str


class FoodSnapBase(BaseModel):
    pass

class FoodSnapCreate(FoodSnapBase):
    food_pic: str

class FoodSnap(FoodSnapBase):
    id: int
    created_at: datetime.datetime
    food_entries: list[IntakeEntry] = []
    class Config:
        orm_mode = True

class FoodSnapResponse(FoodSnap):
    food_pic: str
    food_entries: list[IntakeEntryResponse] = []
