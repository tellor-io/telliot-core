import asyncio
from typing import Any
from typing import Optional

import aiohttp


class ClientSessionManager:
    """Session Manager

    Manage a single `aiohttp.ClientSession` for efficient
    handling of telliot requests for http access.
    """

    @property
    def s(self) -> Optional[aiohttp.ClientSession]:
        """Returns the client session or None"""
        return self._s

    _s: Optional[aiohttp.ClientSession]

    def __init__(self) -> None:
        self._s = None

    async def start(self) -> None:
        """Create the client session"""
        self._s = aiohttp.ClientSession()

    async def fetch_json(self, url: str) -> Any:
        """Fetch JSON response from URL"""
        assert self.s
        async with self.s.get(url) as resp:
            if resp.status == 200:
                json_obj = await resp.json()
                return json_obj
            else:
                return await None

    async def close(self) -> None:
        """Close the client session."""
        if self.s:
            await self.s.close()

    def __del__(self) -> None:
        """Make sure the client session is closed when this object is deleted."""
        if self.s:
            if not self.s.closed:
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        loop.create_task(self.close())
                    else:
                        loop.run_until_complete(self.close())
                except Exception:
                    pass
