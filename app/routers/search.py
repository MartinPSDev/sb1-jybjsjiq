from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..schemas import SearchCreate, SearchResponse
from ..services.search_service import SearchService
from .auth import get_current_user
from ..models import User

router = APIRouter()
search_service = SearchService()

@router.post("/", response_model=SearchResponse)
async def search_travel(
    search: SearchCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Search for travel options across multiple platforms.
    """
    try:
        search_params = search.model_dump()
        if current_user:
            search_params["user_id"] = current_user.id
        
        results = await search_service.search_all(db, search_params)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))