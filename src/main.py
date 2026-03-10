from fastapi import FastAPI
from classes.Item import Item

app = FastAPI()


@app.get("/")
def greet():
    return {"message": "Hello World!"}


@app.post("/greet")
def greet_user(name: str):
    return {"message": "Hello, " + name + "!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_price": item.price}
