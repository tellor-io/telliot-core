import asyncio
from typing import Any
from typing import Optional

import aiohttp


class ClientSessionManager:
    """Session Manager

    Manage a single `aiohttp.ClientSession` for efficient
    handling of user requests for http access.
    """

    @property
    def session(self) -> aiohttp.ClientSession:
        """Returns the client session"""
        if self._session:
            return self._session
        else:
            raise Exception("Client session does not exist.  Use ClientSessionManager.open().")

    _session: Optional[aiohttp.ClientSession]

    def __init__(self) -> None:
        self._session = None

    async def open(self) -> None:
        """Create the client session."""
        self._session = aiohttp.ClientSession()

    async def close(self) -> None:
        """Close the client session."""
        if self.session:
            await self.session.close()

    async def fetch_json(self, url: str) -> Any:
        """Fetch JSON response from URL"""
        async with self.session.get(url) as resp:
            if resp.status == 200:
                json_obj = await resp.json()
                return json_obj
            else:
                return await None

    def __del__(self) -> None:
        """Make sure the client session is closed when this object is deleted."""
        if self._session:
            if not self._session.closed:
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        loop.create_task(self.close())
                    else:
                        loop.run_until_complete(self.close())
                except Exception:
                    pass
