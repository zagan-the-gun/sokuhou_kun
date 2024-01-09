from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/games/", response_model=schemas.GameCreateSchema)
def create_game(
    game: schemas.GameCreateSchema, db: Session = Depends(get_db)
):
    return crud.create_game(db=db, game=game)

@app.get("/games/", response_model=List[schemas.GameSchema])
def read_games(skip: int = 0, limit: int = 100, is_sent: bool = False, db: Session = Depends(get_db)):
    games = crud.get_games(db, skip=skip, limit=limit, is_sent=is_sent)
    return games

@app.put('/games/{id}', response_model=schemas.GameUpdateSchema)
def update_game(
    id: int,
    game: schemas.GameUpdateSchema,
    db: Session = Depends(get_db)
):
    return crud.update_game(db=db, game=game,id=id)

