import os
from uuid import uuid4


POSTERS_DIR = "posters"
os.makedirs(POSTERS_DIR, exist_ok=True)

def save_poster(filename: str, contents: bytes) -> str:

    ext = os.path.splitext(filename)[1]
    new_filename = f"{uuid4()}{ext}"
    filepath = os.path.join(POSTERS_DIR, new_filename)

    with open(filepath, "wb") as f:
        f.write(contents)


    return f"/{POSTERS_DIR}/{new_filename}"