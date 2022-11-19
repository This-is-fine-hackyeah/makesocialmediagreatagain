from sqlalchemy import Column, Integer, String, Float

from app.db.base_class import Base


class Tweet(Base):
    id = Column(Integer, primary_key=True, index=True)

    tweet_id = Column(String, unique=True, index=True, nullable=False)
    author_name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    prediction = Column(Float, nullable=False)
    status = Column(String, nullable=False)
