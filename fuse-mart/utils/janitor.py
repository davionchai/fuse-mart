import logging

from pathlib import Path
from typing import Union


logger = logging.getLogger(__name__)


def clean_path(path: Union[str, Path]):
    _path: Path = Path(path)
    for subpath in _path.iterdir():
        if subpath.is_file():
            logger.info(f"Removing file - [{subpath}].")
            subpath.unlink()
        else:
            clean_path(subpath)
            logger.info(f"Removing dir - [{subpath}].")
            subpath.rmdir()


def init_path(output_path: Union[str, Path]):
    # Clean output path
    _output_path: Path = Path(output_path)
    try:
        if _output_path.exists():
            logger.info(f"Cleaning paath - [{_output_path}].")
            clean_path(_output_path)
        else:
            logger.info(
                f"Dir - [{_output_path}] not found. Proceeding to create the dir."
            )
            _output_path.mkdir(parents=True, exist_ok=True)
    except Exception as error:
        logger.exception(f"Error while cleaning [{_output_path}] - [{error}].")
