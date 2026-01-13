from loguru import logger
import sys


def get_logger(name: str = "medrisk-features"):
    """
    Configure and return a Loguru logger instance.

    Parameters
    ----------
    name : str
        Logical name of the logger (used in logs).

    Returns
    -------
    logger
        Configured Loguru logger.
    """

    # Remove default Loguru handler
    logger.remove()

    # Console handler (notebook / Kaggle / local)
    logger.add(
        sys.stderr,
        level="INFO",
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{extra[logger_name]}</cyan> | "
            "<level>{message}</level>"
        ),
    )

    # Bind contextual name
    return logger.bind(logger_name=name)