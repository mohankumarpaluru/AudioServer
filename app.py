#! /usr/bin/env python3.8
"""
AUTHOR : MOHAN KUMAR PALURU
Description : Audio Server API EndPoints Handler
"""


from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, Response, Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from core.db import SessionLocal, engine
from core import models
from core.db import crud
from core.db.exceptions import AudioDoesNotExist, UpdateError, DeleteError
from core.schemas import AudioFileType, AudioTypeSchemas, AudioCreate

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db(request: Request):
    return request.state.db


# ---- Beginning API of Routes ----#
@app.post("/", response_model=AudioTypeSchemas)
def create_audio_file(
    audio: AudioCreate, db: Session = Depends(get_db)
):
    """
    Api Route to create any of the three AudioFile Types
    """
    try:
        read_audio_file(
            audio_type=audio.audio_type, audio_id=audio.audioFileMetaData.id, db=db
        )
    except AudioDoesNotExist:
        return crud.create_audio_file(
            db=db,
            audio_type=audio.audio_type,
            audio_file_metadata=audio.audioFileMetaData,
        )
    raise HTTPException(status_code=400, detail="AudioFile ID already Exists !")


@app.get(
    "/{audio_type}",
    response_model=List[AudioTypeSchemas],
    description="Do not pass 'audio_id', to get all files",
    name="Read all files in an Audio Type",
)
@app.get("/{audio_type}/{audio_id}", response_model=AudioTypeSchemas)
def read_audio_file(

    audio_type: AudioFileType,
    audio_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
      Api Route to Read any of the three AudioFile Types
        and also read any specific file from a AudioType by id
    """

    # retrieves a list of audio objects
    if audio_id is None:
        return crud.get_audio_files(db, audio_type=audio_type)

    # retrieves specific audio file
    try:
        return crud.get_audio_file(
            db, audio_type=audio_type, audio_id=audio_id
        )

    except AudioDoesNotExist:
        raise HTTPException(status_code=404, detail="AudioFile not found!")


@app.put("/{audio_type}/{audio_id}")
def update_audio_file(
    audio_type: AudioFileType,
    audio_id: int,
    audio: AudioCreate,
    db: Session = Depends(get_db),
):
    """
    Api Route to Update any of the three AudioFile Types by id
    """
    try:
        crud.update_audio_file(
            db=db,
            audio_type=audio_type,
            audio_id=audio_id,
            audio_file_metadata=audio.audioFileMetaData,
        )

        return JSONResponse({"detail": "Audio file updated successfully!"})

    except UpdateError:
        raise HTTPException(status_code=500, detail="AudioFile was not updated!")

    except AudioDoesNotExist:
        raise HTTPException(status_code=404, detail="AudioFile not found!")


@app.delete("/{audio_type}/{audio_id}")
def delete_audio_file(
    audio_type: AudioFileType, audio_id: int, db: Session = Depends(get_db)
):
    """
    Api Route to Delete any of the three AudioFile Types by id
    """
    try:
        crud.delete_audio_file(
            db=db, audio_type=audio_type, audio_id=audio_id
        )
        return JSONResponse({"detail": "Audio file deleted successfully!"})

    except DeleteError:
        raise HTTPException(status_code=500, detail="AudioFile was not deleted!")

    except AudioDoesNotExist:
        raise HTTPException(status_code=404, detail="AudioFile not found!")


# ---- END API of Routes ----#


# middleware
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    API Middleware to Handle DB Session per request
    """
    response = None

    try:
        request.state.db = SessionLocal()
        response = await call_next(request)

    finally:
        request.state.db.close()

        if not response:
            response = Response("Internal server error", status_code=500)

    return response
