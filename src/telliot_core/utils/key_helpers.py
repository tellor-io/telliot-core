import getpass

from chained_accounts import ChainedAccount
from hexbytes import HexBytes


def ask_for_password(name: str) -> str:
    password1 = getpass.getpass(f"Enter encryption password for {name}: ")
    password2 = getpass.getpass("Confirm password: ")
    if password2 != password1:
        raise Exception(f"Passwords do not match: {name}")
    password = password1

    return password


def lazy_unlock_account(account: ChainedAccount) -> None:
    if account.is_unlocked:
        return
    else:
        # Try unlocking with no password
        try:
            account.unlock("")
        except ValueError:
            try:
                password = getpass.getpass(f"Enter encryption password for {account.name}: ")
                account.unlock(password)
            except ValueError:
                raise Exception(f"Invalid password for {account.name}")


def lazy_key_getter(account: ChainedAccount) -> HexBytes:

    lazy_unlock_account(account)

    return account.key  # type: ignore
