from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.limiter import limiter
from app.crud import dashboard as crud_dashboard
from app.schemas.dashboard import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
@limiter.limit("60/minute")
def get_dashboard(request: Request, db: Session = Depends(get_db)):
    return crud_dashboard.get_dashboard_data(db)
