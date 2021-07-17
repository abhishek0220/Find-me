from pydantic import BaseModel, validator


class TasksAdd(BaseModel):
    latitude: str
    longitude: str
    title: str
    image_url: str
    hints: str
    description: str
    city: str
    country: str

    @validator('latitude')
    def latitude_check(cls, v: str):
        try:
            float(v)
        except ValueError:
            raise ValueError("Invalid latitude")

    @validator('longitude')
    def longitude_check(cls, v: str):
        try:
            float(v)
        except ValueError:
            raise ValueError("Invalid longitude")
