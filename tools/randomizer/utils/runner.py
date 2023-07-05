import logging

from psycopg2.extensions import connection

logger = logging.getLogger(__name__)


class PGRunner:
    def __init__(self, conn: connection):
        self.conn: connection = conn

    def create_schema(self, schema_name: str):
        with self.conn.cursor() as cur:
            logger.info(f"checking if schema {schema_name} exists else creating")
            cur.execute(f"create schema if not exists {schema_name};")

    def create_table(
        self,
        schema_name: str,
        table_name: str,
        column_definition: str,
        index_key: str,
    ):
        with self.conn.cursor() as cur:
            logger.info(
                f"checking if table {schema_name}.{table_name} exists else creating"
            )
            cur.execute(
                f"create table if not exists {schema_name}.{table_name} ({column_definition});"
            )
            logger.info(
                f"checking if index key [{index_key}] exists for {schema_name}.{table_name}"
                f" else creating"
            )
            for column in index_key.split(","):
                cur.execute(
                    f"create index if not exists idx_{column.strip()} on {schema_name}.{table_name} ({column.strip()});"
                )

    def insert_data(self, schema_name: str, table_name: str, data: dict):
        with self.conn.cursor() as cur:
            logger.debug(f"inserting data to [{schema_name}.{table_name}]")

            data_keys: list[str] = []
            data_values: list[str] = []
            for data_key, data_value in data.items():
                data_keys.append(data_key)
                data_values.append(f"'{data_value}'")

            column_names: str = ",".join(data_keys)
            values: str = ",".join(data_values)
            query = f"insert into {schema_name}.{table_name} ({column_names}) values ({values})"
            cur.execute(query)

    def update_data(
        self, schema_name: str, table_name: str, data: dict, condition: dict
    ):
        with self.conn.cursor() as cur:
            logger.debug(f"updating data for [{schema_name}.{table_name}]")

            values: list[str] = [
                f"{data_key}='{data_value}'" for data_key, data_value in data.items()
            ]
            conditions: list[str] = [
                f"{conditions_key}={conditions_value}"
                for conditions_key, conditions_value in condition.items()
            ]

            query: str = (
                f"update {schema_name}.{table_name} "
                f"set {', '.join(values)} "
                f"where {' and '.join(conditions)}; "
            )
            cur.execute(query)
