from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tweet import Tweet
from app.schemas.tweet import TweetCreate


class CRUDTweet(CRUDBase[Tweet, TweetCreate, TweetCreate]):
    def get_by_id(self, db: Session, id: str) -> Optional[Tweet]:
        return db.query(Tweet).filter(Tweet.tweetl_id == id).first()

    def get_by_status(self, db: Session, id: str) -> Optional[List[Tweet]]:
        return db.query(Tweet).filter(Tweet.tweetl_id == id).first()

    def create_if_not_exists(self, db: Session, obj_in: TweetCreate) -> Tweet:
        tweet = self.get_by_external_id(db, obj_in.external_id)
        if tweet is not None:
            return tweet

        return self.create(db, obj_in)


tweet = CRUDTweet(Tweet)