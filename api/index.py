from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import api.models as models
import api.schemas as schemas
from api.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/py")
def read_root():
    return {"message": "Welcome to the API"}


@app.post("/api/py/items/", response_model=schemas.Item, tags=["Items"])
def create_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
    db_item = models.Item(title=item.title, body=item.body)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/api/py/items/", response_model=list[schemas.Item], tags=["Items"])
def read_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()


@app.get("/api/py/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/api/py/api/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def update_item(item_id: int, updated_item: schemas.ItemBase, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.title = updated_item.title
    item.body = updated_item.body
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/py/items/{item_id}", tags=["Items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}
