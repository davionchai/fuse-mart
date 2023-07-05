import logging
import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from structs.pgconfig import PGConfigStruct

logger: logging.Logger = logging.getLogger(__name__)


class PGConnector:
    def __init__(self, pg_config: PGConfigStruct):
        try:
            self.conn: psycopg2.connection = psycopg2.connect(**pg_config.__dict__)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            logger.debug(
                f"Successfully connected to postgresdb [{pg_config.host}/{pg_config.port}]!"
            )
        except Exception as e:
            logger.error(e)
            logger.error(
                f"Cannot connect to postgresdb with hostname: [{pg_config.host}/{pg_config.port}]! Exiting script."
            )
            raise e

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.close()
