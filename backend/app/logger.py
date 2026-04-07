import logging
import sys


def setup_logging() -> None:
    """Configure structured JSON logging."""
    # For now, we will configure a simple standard logger.
    # In a real production environment, we'd use python-json-logger or structlog here.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
