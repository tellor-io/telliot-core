from telliot.reporter.config import ReporterConfig
from telliot.utils.app import Application

from typing import Optional


class ReporterApplication(Application):
    config: Optional[ReporterConfig]
