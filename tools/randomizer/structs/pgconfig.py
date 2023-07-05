import logging
import os

from dataclasses import dataclass, field

logger: logging.getLogger = logging.getLogger(__name__)


@dataclass
class PGConfigStruct:
    dbname: str = field(default_factory=lambda: os.environ.get("PG_DBNAME"))
    user: str = field(default_factory=lambda: os.environ.get("PG_USER"))
    password: str = field(default_factory=lambda: os.environ.get("PG_PASSWORD"))
    host: str = field(default_factory=lambda: os.environ.get("PG_HOST"))
    port: str = field(default_factory=lambda: os.environ.get("PG_PORT"))

    def __post_init__(self):
        objects = ["dbname", "user", "password", "host", "port"]
        for obj in objects:
            if getattr(self, obj) is None:
                error_msg: str = f"Missing value for {obj} from environment variable PG_{obj.upper()}"
                logger.error(error_msg)
                raise ValueError(error_msg)
