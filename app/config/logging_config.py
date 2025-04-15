import logging
from rich.logging import RichHandler

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(message)s",handlers=[RichHandler(rich_tracebacks=True, markup=True)])
    logger = logging.getLogger(__name__)
    return logger
