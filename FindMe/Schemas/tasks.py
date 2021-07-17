from pydantic import BaseModel, validator


class TaskORMBase(BaseModel):
    id: str


class TaskBase(BaseModel):
    title: str
    image_url: str
    city: str
    country: str


class TaskOverview(TaskBase, TaskORMBase):

    class Config:
        orm_mode = True


class SingleTask(TaskBase):
    hints: str
    description: str


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


class TasksComplete(BaseModel):
    latitude: str
    longitude: str
    image: str
