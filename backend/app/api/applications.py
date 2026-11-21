from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.enums import ApplicationStatus
from app.schemas.application import (
    ApplicationCreate,
    ApplicationList,
    ApplicationOut,
    ApplicationUpdate,
    StatusUpdate,
)
from app.services import application_service

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationOut, status_code=201)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return application_service.create_application(db, current_user.id, payload.model_dump())


@router.get("", response_model=ApplicationList)
def list_applications(
    status_filter: ApplicationStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    items, total = application_service.list_applications(
        db, current_user.id, status_filter, limit, offset
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return application_service.get_application(db, current_user.id, application_id)


@router.patch("/{application_id}", response_model=ApplicationOut)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    changes = payload.model_dump(exclude_unset=True)
    return application_service.update_application(db, current_user.id, application_id, changes)


@router.patch("/{application_id}/status", response_model=ApplicationOut)
def change_status(
    application_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return application_service.change_status(
        db, current_user.id, application_id, payload.status
    )


@router.delete("/{application_id}", status_code=204)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    application_service.delete_application(db, current_user.id, application_id)
    return Response(status_code=204)