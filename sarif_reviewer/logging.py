from logging import INFO, DEBUG, ERROR, CRITICAL, getLogger, StreamHandler, Formatter
from sarif_reviewer.config import default_config

logging_map = {
    "DEBUG": DEBUG,
    "INFO": INFO,
    "ERROR": ERROR,
    "CRITICAL": CRITICAL
}

def get_logger(name: str, level=default_config.logging_level):
    logger = getLogger(name)
    logging_level = logging_map.get(level, INFO)
    logger.setLevel(logging_level)

    handler = StreamHandler()
    handler.setLevel(logging_level)

    formatter = Formatter(
        "%(asctime)s - %(levelname)s - [%(pathname)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger