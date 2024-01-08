from sqlalchemy.orm import Session

from . import models, schemas


def create_game(db: Session, game: schemas.GameCreateSchema):
    count = db.query(models.Game).filter_by(url = game.url, deadline = game.deadline).count()
    if count > 0:
        print("Duplicate game data")
        return

    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def get_games(db: Session, skip: int = 0, limit: int = 100, is_sent: bool = False):
#    return db.query(models.Game).filter_by(is_sent=is_sent).offset(skip).limit(limit).all()
    return db.query(models.Game).all()

def update_game(db: Session, id: int, game: schemas.GameUpdateSchema):
    db_game = db.query(models.Game).filter_by(id=id).first()
    """
    db_game.update({
        delivery: game.delivery,
    })
    db_game.commit()
    return db_game
    """

#    db_game.is_sent = game.is_sent

    db.commit()
    db.refresh(db_game)
    return db_game

