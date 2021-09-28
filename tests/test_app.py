import pathlib

from telliot.utils.app import default_homedir


def test_homedir():
    """ Test default home directory """
    hd = default_homedir()
    assert isinstance(hd, pathlib.Path)
    assert hd.exists()
