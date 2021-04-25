#! /usr/bin/env python3.8
"""
AUTHOR : MOHAN KUMAR PALURU
Description : Crud Operation Handler for AudioServer
"""


from sqlalchemy.orm import Session

from .. import models
from .exceptions import AudioDoesNotExist, UpdateError, DeleteError
from core.schemas import AudioFileType, AudioCreateTypeSchemas

type_model_map = {
    "song": models.Song,
    "podcast": models.Podcast,
    "audiobook": models.Audiobook,
}


def get_audio_model(audio_type: AudioFileType):
    """
    To read the audio model type
    Parameters
    ----------
    audio_type

    Returns
    -------
    Audio Type Model
    """
    return type_model_map[audio_type]


def get_audio_file(db: Session, audio_type: AudioFileType, audio_id: int):
    """
    To Read A single AudioFile from AudioType through ID
    Parameters
    ----------
    db
    audio_type
    audio_id

    Returns
    -------
    Returns Audio File MetaData
    """
    audio_model = get_audio_model(audio_type)
    audio_object = db.query(audio_model).get(audio_id)

    if audio_object is None:
        raise AudioDoesNotExist()

    return audio_object


def get_audio_files(
    db: Session, audio_type: AudioFileType, skip: int = 0, limit: int = 100
):
    """
    TO Read all AudioFiles in the a Particular AudioType
    Parameters
    ----------
    db
    audio_type
    skip
    limit

    Returns
    -------
    Returns a List of all AudioFiles in an AudioType

    """
    audio_model = get_audio_model(audio_type)
    return db.query(audio_model).offset(skip).limit(limit).all()


def create_audio_file(
    db: Session,
    audio_type: AudioFileType,
    audio_file_metadata: AudioCreateTypeSchemas,
):
    """
    Creates an AudioFile through AudioType
    Parameters
    ----------
    db
    audio_type
    audio_file_metadata

    Returns
    -------
    Returns Error Message if Audio_ID already exists
     else Success Message
    """
    audio_model = get_audio_model(audio_type)
    audio_object = audio_model(**audio_file_metadata.dict())

    db.add(audio_object)
    db.commit()
    db.refresh(audio_object)
    return audio_object


def update_audio_file(
    db: Session,
    audio_type: AudioFileType,
    audio_id: int,
    audio_file_metadata: AudioCreateTypeSchemas,
):
    """
    Update the MetaData of an AudioFile by Audio_ID
    Parameters
    ----------
    db
    audio_type
    audio_id
    audio_file_metadata

    Returns
    -------
    Returns a Success Message
    """

    audio_model = get_audio_model(audio_type)
    audio_object_id = (
        db.query(audio_model).filter_by(id=audio_id).update(audio_file_metadata.dict())
    )

    if not audio_object_id:
        raise AudioDoesNotExist()

    if audio_object_id != audio_id:
        raise UpdateError()

    db.commit()
    return audio_object_id


def delete_audio_file(db: Session, audio_type: AudioFileType, audio_id: int):
    """
    Delete the selected AUdioFile From Audiotype DB through ID
    Parameters
    ----------
    db
    audio_type
    audio_id

    Returns
    -------
    Error Message if AudioFile Not Found
    else a Success Message
    """
    audio_model = get_audio_model(audio_type)
    audio_object_id = db.query(audio_model).filter_by(id=audio_id).delete()

    if not audio_object_id:
        raise AudioDoesNotExist()

    if audio_object_id != audio_id:
        raise DeleteError()

    db.commit()
    return audio_object_id
