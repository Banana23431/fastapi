from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, constr, condecimal
from typing import List, Optional

app = FastAPI()
class Item(BaseModel):
    id: int
    name: constr(min_length=2, max_length=100)
    price: condecimal(gt=0)
    description: Optional[constr(max_length=500)] = None

    
items_db = [
    Item(id=1, name="Phone", price=700,description="Описание"),
    Item(id=2, name="Banana", price=300,description="Описание"),
    Item(id=3, name="Apple", price=200,description="Описание"),
    Item(id=4, name="Table", price=1000,description="Описание"),
    Item(id=5, name="Orange", price=260,description="Описание"),
    Item(id=6, name="Computer", price=1300,description="Описание"),
    Item(id=7, name="Dish", price=100,description="Описание"),
    Item(id=8, name="Fork", price=80,description="Описание"),
]

current_id = 8

@app.get("/items/", response_model=List[Item])
async def get_items(
    name: Optional[constr(min_length=2)] = Query(None),
    min_price: Optional[condecimal(gt=0)] = Query(None),
    max_price: Optional[condecimal(gt=0)] = Query(None),
    limit: Optional[int] = Query(10, ge=1, le=100)
):
    filtered_items = items_db

    if name:
        filtered_items = [item for item in filtered_items if name.lower() in item.name.lower()]
    
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]
    
    if max_price is not None:
        if min_price is not None and max_price < min_price:
            raise HTTPException(status_code=400, detail="Максимальная цена должна быть выше минимальной")
        filtered_items = [item for item in filtered_items if item.price <= max_price]
    
    return filtered_items[:limit]

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id:int):
    if item_id <= 0:
        raise HTTPException(status_code=400,detail="Идентификатор должен быть положительным")
    
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404,detail="Объект не найден")

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    global current_id
    new_item = Item(id=current_id, **item.dict())
    items_db.append(new_item)
    current_id += 1
    return new_item