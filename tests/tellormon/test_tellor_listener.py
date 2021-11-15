from tellormon.events import TellorEventListener
import pytest
import asyncio

from telliot_core.directory.tellorx import tellor_directory
from tellormon.tellor_listener import tellor_listener

#@pytest.mark.asyncio
def test_tellor_listener(rinkeby_cfg):
    print(rinkeby_cfg)
    master_info = tellor_directory.find(name='master', chain_id=4)[0]

    async def run_listener():
        # Create a "cancel_me" Task

        task = asyncio.create_task(tellor_listener(url=rinkeby_cfg.get_endpoint().url, chain_id =4))

        # Wait for 1 second
        await asyncio.sleep(120)

        # task.cancel()

        # try:
        #     print("awaiting task")
        #     await task
        # except asyncio.CancelledError:
        #     print("main(): cancel_me is cancelled now")

    asyncio.run(run_listener())

#
# @pytest.mark.asyncio
# async def test_subscribe():
#     app = TellorEventListener()
#     await app.subscribe()
#     app.destroy()
#
# def test_app_constructor():
#     # Create a default application
#     app = TellorEventListener()
#
#     # Prevent creating two Applications
#     with pytest.raises(RuntimeError):
#         app = TellorEventListener()
#
#     # Destroy existing app
#     app.destroy()
#
#     app1 = TellorEventListener().get()
#
#     # Re-get existing app object
#     app2 = TellorEventListener.get()
#
#     assert app1 is app2
#
#     with pytest.raises(RuntimeError):
#         _ = TellorEventListener()
#
#     app1.destroy()
