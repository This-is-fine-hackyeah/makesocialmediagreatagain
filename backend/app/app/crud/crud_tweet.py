from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tweet import Tweet
from app.schemas.tweet import TweetCreate


class CRUDTweet(CRUDBase[Tweet, TweetCreate, TweetCreate]):
    def get_by_id(self, db: Session, id: str) -> Optional[Tweet]:
        return db.query(Tweet).filter(Tweet.tweet_id == id).first()

    def get_by_status(self, db: Session, status: str) -> Optional[List[Tweet]]:
        return db.query(Tweet).filter(Tweet.status == status).count()

    def get_by_text(self, db: Session, text: str) -> Optional[List[Tweet]]:
        return db.query(Tweet).filter(Tweet.text == text).first()

    def get_by_prediction(self, db: Session, prediction: float) -> Optional[List[Tweet]]:
        return db.query(Tweet).filter(Tweet.prediction >= prediction).count()

    def create_if_not_exists(self, db: Session, obj_in: TweetCreate) -> Tweet:
        tweet = self.get_by_id(db, obj_in.tweet_id)
        if tweet is not None:
            return None

        tweet = self.get_by_text(db, obj_in.text)
        if tweet is not None:
            return None

        return self.create(db, obj_in)


tweet = CRUDTweet(Tweet)