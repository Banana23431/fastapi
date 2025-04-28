from pydantic import BaseModel, Field


class CreateProduct(BaseModel):
    name: str = Field(min_length=2, max_length=100, example="Яблоко")
    price: float = Field(gt=0, example=20)
    category_id: int = Field(gt=0, example=1)
