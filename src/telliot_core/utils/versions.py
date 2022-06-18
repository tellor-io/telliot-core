from typing import Any
from typing import Callable

import telliot_core

# from telliot_core.plugin.discover import telliot_plugins


def show_telliot_versions(caller: Callable[[Any], None] = print) -> None:  # , include_plugins: bool = True) -> None:
    caller(f"telliot-core {telliot_core.__version__}")
    # if include_plugins:
    #     for name, pkg in telliot_plugins.items():
    #         if name != "telliot_core":
    #             try:
    #                 caller(f"{name} (plugin): Version {pkg.__version__}")
    #             except AttributeError:
    #                 caller(f"{name} (plugin): Version UNKNOWN")
