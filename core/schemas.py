#! /usr/bin/env python3.8
"""
AUTHOR : MOHAN KUMAR PALURU
Description : Schemas Handler for all the Audio Services
"""


from datetime import datetime
from typing import Union, Optional, NewType
from typing_extensions import Literal
from pydantic import BaseModel, constr, conint, root_validator

AudioFileType = NewType("AudioFileType", Literal["song", "podcast", "audiobook"])


class AudioSchema(BaseModel):
    """
    Base AudioSchema Class with Common MetaData between the types
    """

    id: int
    duration: conint(gt=0)
    uploaded_time: datetime


class SongSchema(AudioSchema):
    """
    SongSchema Class with additional Metadata than common ones
    """

    name: constr(min_length=1, max_length=100)

    class Config:
        orm_mode = True


class PodcastSchema(AudioSchema):
    """
    Podcast Class with additional Metadata than common ones
    """

    name: constr(min_length=1, max_length=100)
    host: constr(min_length=1, max_length=100)
    participants: Optional[constr(min_length=1, max_length=1000)]

    class Config:
        orm_mode = True


class AudiobookSchema(AudioSchema):
    """
    AudiobookSchema Class with additional Metadata than common ones
    """

    title: constr(min_length=1, max_length=100)
    author: constr(min_length=1, max_length=100)
    narrator: constr(min_length=1, max_length=100)

    class Config:
        orm_mode = True


class SongCreateSchema(BaseModel):
    """
    Schema of Metadata required to create a Song
    """

    id: conint(gt=0)
    name: constr(min_length=1, max_length=100)
    duration: conint(gt=0)


class PodcastCreateSchema(BaseModel):
    """
    Schema of Metadata required to create a Podcast
    """

    id: conint(gt=0)
    name: constr(min_length=1, max_length=100)
    duration: conint(gt=0)
    host: constr(min_length=1, max_length=100)
    participants: constr(min_length=1, max_length=1000)


class AudiobookCreateSchema(BaseModel):
    """
    Schema of Metadata required to create an AudioBook
    """

    id: conint(gt=0)
    title: constr(min_length=1, max_length=100)
    author: constr(min_length=1, max_length=100)
    narrator: constr(min_length=1, max_length=100)
    duration: conint(gt=0)


AudioTypeSchemas = Union[SongSchema, PodcastSchema, AudiobookSchema]
AudioCreateTypeSchemas = Union[
    SongCreateSchema, PodcastCreateSchema, AudiobookCreateSchema,
]



type_to_create_schema_map = {
    "song": SongCreateSchema,
    "podcast": PodcastCreateSchema,
    "audiobook": AudiobookCreateSchema,
}


class AudioCreate(BaseModel):
    """
    Verifier class to assert the Metadata received during the request
    matches with the AudioType's Required Metadata.
    """

    audioFileType: AudioFileType
    audioFileMetaData: AudioCreateTypeSchemas

    @root_validator
    def validate_audio_file_metadata_type(cls, values):
        audio_type = values.get("audioFileType")
        audio_file_metadata = values.get("audioFileMetaData")

        expected_type = type_to_create_schema_map.get(audio_type)
        assert (
            isinstance(audio_file_metadata, expected_type) is True
        ), "Invalid data not matching the audio file type"
        return values
