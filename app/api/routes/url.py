from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.url import URL
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import create_short_url


# API Router
router = APIRouter(
    prefix="/api/v1/urls",
    tags=["URLs"]
)


# Create Short URL
@router.post("/", response_model=URLResponse)
def create_url(
    data: URLCreate,
    db: Session = Depends(get_db)
):
    url = create_short_url(
        db=db,
        original_url=str(data.original_url)
    )

    return URLResponse(
        original_url=url.original_url,
        short_code=url.short_code,
        short_url=f"{settings.BASE_URL}/{url.short_code}",
        clicks=url.clicks
    )


# Redirect Router
redirect_router = APIRouter(
    tags=["Redirect"]
)


# Redirect Short URL
@redirect_router.get("/{short_code}")
def redirect_short_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    url = (
        db.query(URL)
        .filter(URL.short_code == short_code)
        .first()
    )

    if not url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    # Increase click count
    url.clicks += 1

    db.commit()

    # Redirect to original URL
    return RedirectResponse(
        url=url.original_url,
        status_code=307
    )