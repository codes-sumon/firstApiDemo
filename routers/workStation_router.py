from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.workStation import WorkStation
from schemas.workStation import WorkStationCreate, WorkStationUpdate, WorkStationResponse
from utils.dependencies import get_current_user, get_db

router = APIRouter(prefix="/workstations", tags=["WorkStations"])

# Create
@router.post("/", response_model=WorkStationResponse)
def create_workstation(workstation: WorkStationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_ws = db.query(WorkStation).filter(WorkStation.name == workstation.name).first()
    if db_ws:
        raise HTTPException(status_code=400, detail="WorkStation already exists")
    new_ws = WorkStation(name=workstation.name, location=workstation.location)
    db.add(new_ws)
    db.commit()
    db.refresh(new_ws)
    return new_ws

# Read all
@router.get("/", response_model=list[WorkStationResponse])
def read_workstations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    workstations = db.query(WorkStation).offset(skip).limit(limit).all()
    return workstations

# Read single
@router.get("/{ws_id}", response_model=WorkStationResponse)
def read_workstation(ws_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ws = db.query(WorkStation).filter(WorkStation.id == ws_id).first()
    if not ws:
        raise HTTPException(status_code=404, detail="WorkStation not found")
    return ws

# Update
@router.put("/{ws_id}", response_model=WorkStationResponse)
def update_workstation(ws_id: int, ws_update: WorkStationUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ws = db.query(WorkStation).filter(WorkStation.id == ws_id).first()
    if not ws:
        raise HTTPException(status_code=404, detail="WorkStation not found")
    if ws_update.name:
        ws.name = ws_update.name
    if ws_update.location:
        ws.location = ws_update.location
    db.commit()
    db.refresh(ws)
    return ws

# Delete
@router.delete("/{ws_id}")
def delete_workstation(ws_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ws = db.query(WorkStation).filter(WorkStation.id == ws_id).first()
    if not ws:
        raise HTTPException(status_code=404, detail="WorkStation not found")
    db.delete(ws)
    db.commit()
    return {
        "deleted": {
            "id": ws.id,
            "name": ws.name,
            "location": ws.location
        },
        "detail": "WorkStation deleted successfully"
    }
