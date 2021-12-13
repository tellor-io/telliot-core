""" Telliot application helpers

"""
import logging
import threading
from dataclasses import dataclass
from dataclasses import field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ThreadedApplication:

    #: BaseApplication Name
    name: str = field(default="appname")

    #: Private thread storage
    _thread: Optional[threading.Thread] = None
    _shutdown: threading.Event = field(default_factory=threading.Event)

    def startup(self) -> None:
        """Startup BaseApplication

        Start the main application thread
        """
        logger.info("Starting {} BaseApplication".format(self.name))
        self._thread = threading.Thread(target=self.main, name=self.name)
        self._thread.start()

    def shutdown(self) -> None:
        """Startup BaseApplication

        Send a shutdown event to the main application thread and wait
        for it to terminate.
        """
        if self._thread:
            logger.info("Terminating {} BaseApplication".format(self.name))

            self._shutdown.set()

            #: Join worker thread
            self._thread.join()

            self._thread = None

    def main(self) -> None:
        """Main worker thread

        This method defined the main application processing.
        The main thread must monitor and respond to the self._shutdown event.

        This method *must* be overridded by subclasses.
        """
        seconds = 0
        while not self._shutdown.wait(1.0):
            logger.info("Main thread processing: {}".format(seconds))
            seconds += 1

        logger.info("BaseApplication {} received shutdown event".format(self.name))
        self._shutdown.clear()
