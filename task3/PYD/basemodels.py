from pydantic import BaseModel, Field


class BaseCategoy(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(example="Еда")


class BaseProduct(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=100, example="Яблоко")
    img: str | None
    price: float = Field(gt=0, example=20)
