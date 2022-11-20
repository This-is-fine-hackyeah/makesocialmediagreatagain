import json
from typing import Any, List
import os

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import crud, schemas
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
    new_tweets = []
    for one_tweet in all_tweets:
        # ML tutaj
        # prediction = get_prediction_from_model(one_tweet)
        prediction = 0.5 #jeden rabin powie tak, drugi rabin powie nie
        result = crud.tweet.create_if_not_exists(
            db, schemas.TweetCreate(tweet_id=one_tweet["id"], text=one_tweet["text"], author_name=one_tweet["author_at"], prediction=0.5, status="initial", media=one_tweet["media_url"])
        )
        if result is not None:
            # ML tutaj
            # prediction = get_prediction_from_model(one_tweet)
            # result.prediction = prediction
            db.commit()
            new_tweets.append({"id": result.tweet_id, "prediction": result.prediction})
    return json.dumps(new_tweets)


@router.post("/change")
async def update_item(
    request: Request,
    db: Session = Depends(get_db),
) -> Any:
    """
    Update a tweet.
    """
    payload = await request.form()
    tweet = crud.tweet.get_by_id(db, payload["id"])
    tweet.status = payload["status"]
    db.commit()
    return 200


@router.get("/get-statistics")
def get_recent_tweets(
    db: Session = Depends(get_db),
) -> Any:
    tweet_positive = crud.tweet.get_by_status(db, "accepted")
    tweet_negative = crud.tweet.get_by_status(db, "declined")
    tweet_initial = crud.tweet.get_by_status(db, "initial")
    prediction_scam = crud.tweet.get_by_prediction(db, 0.5)
    sum_of_tweets = tweet_positive + tweet_negative + tweet_initial
    results = {"accepted": tweet_positive, "declined": tweet_negative, "initial": tweet_initial, "scam_pred": prediction_scam,
               "sum": sum_of_tweets}
    return json.dumps(results)