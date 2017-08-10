import json
import sqlalchemy
import io

def read_db_configs(config_file):
    if isinstance(config_file, io.TextIOWrapper):
        return json.load(config_file)
    elif isinstance(config_file, str):
        with open(config_file, 'r') as f:
            return json.load(f)


def create_engine_from_config_file(config_file):
    db_config = read_db_configs(config_file)
    return sqlalchemy.create_engine('postgresql://',
                                    connect_args=db_config)
