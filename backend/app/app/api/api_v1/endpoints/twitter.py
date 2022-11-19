from typing import Any, List
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.api.deps import get_db
from app.core.scrapper.train_scrapper import search_by_words, search_by_names

router = APIRouter()


@router.get("/get-recent-tweets")
def get_recent_tweets(
    db: Session = Depends(get_db),
) -> Any:
    consumer_key = settings.consumer_key
    consumer_secret = settings.consumer_secret
    access_token = settings.access_token
    access_token_secret = settings.access_token_secret

    print(os.getcwd())

    all_data = search_by_words("app/core/scrapper/Bag od words.xlsx")
    all_data2 = search_by_names("app/core/scrapper/Lista Podmiotów Nadzorowanych (Supervised Entities List) - HY2022.xlsx")
    print(len(all_data), len(all_data2))

    all_tweets = all_data + all_data2

    for one_tweet in all_tweets:
        # ML tutaj
        # prediction = get_prediction_from_model(one_tweet)
        prediction = 0.5 #jeden rabin powie tak, drugi rabin powie nie
        tweet = crud.tweet.create_if_not_exists(
            db, schemas.UserCreate(tweet_id=one_tweet["id"], text=one_tweet["text"], author_name=one_tweet["author_at"], prediction=prediction, status="initial")
        )
    return 200



@router.put("/{id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(get_db),
) -> Any:
    """
    Update an item.
    """
    pass
