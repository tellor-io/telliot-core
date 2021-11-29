import pathlib
from pathlib import Path
from typing import Optional
from typing import Union

TELLIOT_CORE_ROOT = Path(__file__).parent.parent


def default_homedir() -> pathlib.Path:
    """Return default home directory, creating it if necessary

    Returns:
        pathlib.Path : Path to home directory
    """
    homedir = Path.home() / ("telliot")
    homedir = homedir.resolve().absolute()
    if not homedir.is_dir():
        homedir.mkdir()

    return homedir


def telliot_homedir(homedir: Optional[Union[str, Path]] = None) -> Path:
    """Telliot home directory

    Returns the telliot_core home Path, using a default if none is provided.
    The default directory is created if it does not exist.
    A homedir that is provided must exist
    """
    if homedir is None:
        # Set default homedir and create if necessary
        result = default_homedir()
        if not result.exists():
            result.mkdir(parents=True)
    else:
        # Use specified home directory
        if isinstance(homedir, str):
            homedir = Path(homedir)
        result = homedir.resolve().absolute()
        if not result.exists():
            raise FileExistsError("Directory does not exist: {}".format(homedir))

    return result
