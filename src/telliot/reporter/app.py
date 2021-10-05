from typing import Optional

from telliot.reporter.config import ReporterConfig
from telliot.utils.app import Application


class ReporterApplication(Application):
    config: Optional[ReporterConfig]
