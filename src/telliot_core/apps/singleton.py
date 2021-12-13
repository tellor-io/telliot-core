from typing import ClassVar, Dict, Any


class Singleton(type):
    """ Metaclass for class that only allows a single instance

    """

    _instances: ClassVar[Dict[type, Any]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """ Return a new singleton instance of type cls

        If the singleton already exists, an exception will be raised
        """
        if cls in Singleton._instances:
            raise RuntimeError(f"{cls.__name__} already exists")
        else:
            self = super(Singleton, cls).__call__(*args, **kwargs)
            Singleton._instances[cls] = self

        return self

    def get(cls) -> Any:
        """ Get the singleton instance of type cls

        """
        if cls not in Singleton._instances:
            raise LookupError(f"{cls.__name__} does not exist")
        return Singleton._instances[cls]

    def destroy(cls) -> None:
        """ Destroy the singleton instance

        """
        Singleton._instances.pop(cls, None)
