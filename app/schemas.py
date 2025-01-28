from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class SearchBase(BaseModel):
    destination: str
    start_date: datetime
    end_date: datetime
    guests: int
    budget: float
    origin: Optional[str] = None

class SearchCreate(SearchBase):
    pass

class SearchResult(BaseModel):
    site: str
    type: str
    price: float
    currency: str
    title: str
    description: str
    link: str
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    image_url: Optional[str] = None
    amenities: Optional[str] = None
    location: Optional[str] = None

class SearchResponse(BaseModel):
    id: int
    best_flight: Optional[SearchResult] = None
    best_accommodation: Optional[SearchResult] = None
    all_flights: List[SearchResult]
    all_accommodations: List[SearchResult]
    total_found: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None