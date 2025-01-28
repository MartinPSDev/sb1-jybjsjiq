from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    searches = relationship("Search", back_populates="user")

class Search(Base):
    __tablename__ = "searches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    destination = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    guests = Column(Integer)
    budget = Column(Float)
    origin = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="searches")
    results = relationship("SearchResult", back_populates="search")

class SearchResult(Base):
    __tablename__ = "search_results"
    
    id = Column(Integer, primary_key=True, index=True)
    search_id = Column(Integer, ForeignKey("searches.id"))
    site = Column(String)
    type = Column(String)  # 'flight' or 'accommodation'
    price = Column(Float)
    currency = Column(String)
    title = Column(String)
    description = Column(String)
    link = Column(String)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)
    amenities = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    search = relationship("Search", back_populates="results")