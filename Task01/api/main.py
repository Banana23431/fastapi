from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import math

app = FastAPI()

class DeveloperInfo(BaseModel):
    full_name: str
    group: str

@app.get("/about", response_model=DeveloperInfo)
async def get_about():
    return DeveloperInfo(full_name="Акентьев Василий Юрьевич", group="Группа T-323901")

@app.get("/rnd")
async def get_random_number():
    return {"random_number": random.randint(1, 10)}

@app.get("/t_square")
async def calculate_triangle(a: float, b: float, c: float):

    if a <= 0 or b <= 0 or c <= 0:
        raise HTTPException(status_code=400, detail="Стороны треугольника должны быть больше 0")

    if a + b <= c or a + c <= b or b + c <= a:
        raise HTTPException(status_code=400, detail="Такой треугольник не существует")

    perimeter = a + b + c

    s = perimeter / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    return {"perimeter": perimeter, "area": area}
