import logging
from . import __name__ as pkg_name
from ..config import settings

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL, logging.INFO))
logger = logging.getLogger("sentinel_delta")
