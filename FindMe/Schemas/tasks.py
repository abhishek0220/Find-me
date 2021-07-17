from pydantic import BaseModel, validator


class TaskBase(BaseModel):
    title: str
    image_url: str
    city: str
    country: str


class TaskOverview(TaskBase):
    class Config:
        orm_mode = True


class SingleTask(TaskBase):
    hints: str
    description: str


class GetSingleTask(SingleTask):
    class Config:
        orm_mode = True


class TasksAdd(SingleTask):
    latitude: str
    longitude: str


    @validator('latitude')
    def latitude_check(cls, v: str):
        try:
            float(v)
        except ValueError:
            raise ValueError("Invalid latitude")
        return v

    @validator('longitude')
    def longitude_check(cls, v: str):
        try:
            float(v)
        except ValueError:
            raise ValueError("Invalid longitude")
        return v
