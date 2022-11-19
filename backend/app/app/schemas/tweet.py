from pydantic import BaseModel


class TweetCreate(BaseModel):
    tweet_id: str
    text: str
    author_name: str
    prediction: float
    status: str