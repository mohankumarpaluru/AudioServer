#! /usr/bin/env python3.8
"""
AUTHOR : MOHAN KUMAR PALURU
Description : DB Models Handler Service
"""

from sqlalchemy import Column, Integer, String, func, DateTime

from core.db import Base


class Song(Base):
    """
    Model for the Song
    """

    __tablename__ = "song"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    duration = Column(Integer, nullable=False)
    uploaded_time = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Podcast(Base):
    """
    Model for the podcast
    """

    __tablename__ = "podcast"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    duration = Column(Integer, nullable=False)
    uploaded_time = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    host = Column(String(100), index=True, nullable=False)
    participants = Column(String(1000), nullable=True)


class Audiobook(Base):
    """
    Model for the AudioBook
    """

    __tablename__ = "audiobook"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    title = Column(String(100), index=True, nullable=False)
    author = Column(String(100), index=True, nullable=False)
    narrator = Column(String(100), index=True, nullable=False)
    duration = Column(Integer, nullable=False)
    uploaded_time = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
