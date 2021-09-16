"""API Models

This module builds Pydantic models used for
enforcing data types when creating and reading
with the datafeed api.
"""
import datetime

from pydantic import BaseModel


class DataIn(BaseModel):
    """Ingested data model.

    Standardize data ingested to database using typing.
    Ingested data does not include auto-generated ids.
    """

    uid: str
    value: str
    timestamp: datetime.datetime


class Data(BaseModel):
    """Retrieved data model.

    Standardize data queried from the database using typing.
    Retrieved data includes the auto-generated id for the row.
    """

    id: int
    uid: str
    value: str
    timestamp: datetime.datetime
