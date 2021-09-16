""" Feeder database module

This module creates a database with a model to store off-chain data.
"""
import databases
import sqlalchemy  # type: ignore


DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

offchain = sqlalchemy.Table(
    "offchain",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("uid", sqlalchemy.String),
    sqlalchemy.Column("value", sqlalchemy.String),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
