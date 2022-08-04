import asyncio

import pytest

from telliot_core.apps.session_manager import ClientSessionManager


# ---------------------------------------------------------------------------------------
# BEGIN Asyncio windows bug workaround
#
# The first solution silences the exception that is raised on windows
#   https://github.com/aio-libs/aiohttp/issues/4324#issuecomment-733884349
# The second adds a delay before closing the event_loop (see event_loop below)
#   https://github.com/encode/httpx/issues/914#issuecomment-780023632
# Should only need to do one of these.
# ---------------------------------------------------------------------------------------
# def silence_event_loop_closed(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         try:
#             return func(self, *args, **kwargs)
#         except RuntimeError as e:
#             if str(e) != 'Event loop is closed':
#                 raise
#
#     return wrapper
#
#
# import platform
# from asyncio.proactor_events import _ProactorBasePipeTransport
# if platform.system() == 'Windows':
#     _ProactorBasePipeTransport.__del__ =
#              silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


@pytest.fixture(scope="module")
def event_loop():
    """Override event loop

    Reason 1: Override scope to match client_session scope
    Reason 2: Add delay before closing
            https://github.com/encode/httpx/issues/914#issuecomment-780023632
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()


@pytest.fixture(scope="module")
async def client_session():
    """Reusable client session"""
    cm = ClientSessionManager()
    await cm.open()
    yield cm
    await asyncio.sleep(0)
    await cm.close()


#   E       AttributeError: 'async_generator' object has no attribute 'fetch_json'
@pytest.mark.skip("Does aiottp have support for async generators?")
@pytest.mark.asyncio
async def test_session(client_session):
    """Test the ClientSessionManager class"""
    result = await client_session.fetch_json(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    )
    assert "bitcoin" in result
