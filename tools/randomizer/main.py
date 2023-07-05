import os
import time
import random
from pathlib import Path
from datetime import datetime

from structs.dataschema import DataSchemaStruct
from structs.pgconfig import PGConfigStruct
from utils.connectors import PGConnector
from utils.dotdict import DotDict
from utils.generator import generate_random_data
from utils.logger import log_setup
from utils.runner import PGRunner


def main():
    schema_name: str = "hydaelyn"
    table_name: str = "eorzea_population"
    column_definition: str = (
        "uid serial primary key,"
        "race varchar(20),"
        "name varchar(20),"
        "birthday date,"
        "gil bigint,"
        "created_at timestamp,"
        "updated_at timestamp"
    )
    index_key: str = "race, name, birthday"
    pg_config: PGConfigStruct = PGConfigStruct()

    with PGConnector(pg_config=pg_config) as conn:
        pg_runner: PGRunner = PGRunner(conn)
        pg_runner.create_schema(schema_name=schema_name)
        pg_runner.create_table(
            schema_name=schema_name,
            table_name=table_name,
            column_definition=column_definition,
            index_key=index_key,
        )

    while True:
        current_datetime: datetime = datetime.now()
        for _ in range(random.randint(10, 15)):
            with PGConnector(pg_config=pg_config) as conn:
                pg_runner: PGRunner = PGRunner(conn)
                random_data: DataSchemaStruct = DotDict(generate_random_data())
                gil: int = 0
                uid: int = 0
                race: str = random_data.race.replace("'", "''")
                name: str = random_data.name.replace("'", "''")
                # check uid exist & get existing gil
                with conn.cursor() as cur:
                    query: str = (
                        f"select uid, gil from {schema_name}.{table_name} "
                        "where true "
                        f"and race = '{race}' "
                        f"and name = '{name}' "
                        f"and birthday = '{random_data.birthday.date()}'::date"
                        ";"
                    )
                    cur.execute(query)
                    result = cur.fetchone()
                    if result:
                        uid = result[0]
                        gil = result[1]

                if uid:
                    gil = max(gil + random_data.gil, 0)
                    logger.info(f"updating {random_data.__dict__}")
                    pg_runner.update_data(
                        schema_name=schema_name,
                        table_name=table_name,
                        data={
                            "gil": f"{gil}",
                            "updated_at": current_datetime,
                        },
                        condition={
                            "uid": uid,
                        },
                    )
                else:
                    gil = 0 if random_data.gil < 0 else random_data.gil
                    logger.info(f"inserting {random_data.__dict__}")
                    pg_runner.insert_data(
                        schema_name=schema_name,
                        table_name=table_name,
                        data={
                            "race": race,
                            "name": name,
                            "birthday": random_data.birthday.date(),
                            "gil": f"{gil}",
                            "created_at": current_datetime,
                            "updated_at": current_datetime,
                        },
                    )
        time.sleep(10)


if __name__ == "__main__":
    PARENT_DIR: Path = Path(__file__).resolve().parent

    logger = log_setup(
        parent_dir=f"{PARENT_DIR}",
        log_filename=f"{PARENT_DIR.name}",
        logger_level=os.environ.get("LOGGER_LEVEL").upper()
        if os.environ.get("LOGGER_LEVEL")
        else None,
    )
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping randomizer")
