""" Database API Server

This module provides API access to the datafeed database through
a local server port.
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional

from fastapi import FastAPI
from telliot.datasource_db import db
from telliot.datasource_db import schemas

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    """Connect database.

    Connects to local postgresql database on server startup.
    """
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Disconnect database.

    Disconnects local postgresql database on server shutdown.
    """
    await db.database.disconnect()


@app.post("/data/", response_model=schemas.Data)
async def create_data(data: schemas.DataIn) -> Dict[str, Any]:
    """Add data.

    Store new data in connected postgresql database.
    """
    query = db.offchain.insert().values(
        uid=data.uid, value=data.value, timestamp=data.timestamp
    )
    last_record_id = await db.database.execute(query)
    return {**data.dict(), "id": last_record_id}  # type: ignore


@app.get("/data/", response_model=List[schemas.Data])
async def get_all() -> List[Mapping[str, Any]]:
    """Get all data.

    Retrieves all off-chain data stored in connected database.
    """
    query = db.offchain.select()
    return await db.database.fetch_all(query)


@app.get("/data/latest/", response_model=schemas.Data)
async def get_latest_by_uid(uid: str) -> Optional[Mapping[str, Any]]:
    """Get last entry for specified data.

    Retrieves one data entry based on given name.
    """
    query = f"""
    select * from offchain
    where uid = "{uid}"
    order by timestamp desc limit 1
    """
    return await db.database.fetch_one(query)
