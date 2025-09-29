import os
from shutil import get_terminal_size
from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger, configure_logging

from typing import Literal, Any
import logging
from rich.logging import RichHandler
from rich.console import Console

import fastmcp
import fastmcp.utilities.logging

logger = get_logger(__name__)


def get_handlers_from_logger() -> list[RichHandler]:
    logger = logging.getLogger("fastmcp")
    return [hdlr for hdlr in logger.handlers if isinstance(hdlr, RichHandler)]


logger.info("Starting program")

mcp = FastMCP(__name__)

@mcp.tool()
def shutil_terminal_size():
    return get_terminal_size()

@mcp.tool()
def os_terminal_size():
    return os.get_terminal_size()

@mcp.tool()
def cause_traceback():
    configure_logging()
    logger.info("Causing traceback")
    rich_handler: RichHandler = get_handlers_from_logger()[0]
    logger.info(str(rich_handler))
    logger.info(str(rich_handler.console))
    raise Exception("Test exception")

@mcp.tool()
def set_rich_handler_width(width: int):
    rich_handler: RichHandler = get_handlers_from_logger()[0]
    rich_handler.tracebacks_code_width = width
    rich_handler.console.width = width
    rich_handler.tracebacks_width = width
    return str(rich_handler)

@mcp.tool()
def get_environment():
    return {k: v for k, v in os.environ.items()}

@mcp.tool()
def get_columns():
    return os.environ.get("COLUMNS")

@mcp.tool()
def get_logger_handlers():
    return get_handlers_from_logger()

@mcp.tool()
def get_console():
    rich_handler: RichHandler = get_handlers_from_logger()[0]
    return str(rich_handler.console)



def configure_logging(
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | int = "INFO",
    logger: logging.Logger | None = None,
    enable_rich_tracebacks: bool | None = None,
    **rich_kwargs: Any,
) -> None:
    """
    Configure logging for FastMCP.

    Args:
        logger: the logger to configure
        level: the log level to use
        rich_kwargs: the parameters to use for creating RichHandler
    """
    import pydantic
    import mcp
    import fastmcp
    # Check if logging is disabled in settings
    if not fastmcp.settings.log_enabled:
        return

    # Use settings default if not specified
    if enable_rich_tracebacks is None:
        enable_rich_tracebacks = fastmcp.settings.enable_rich_tracebacks

    if logger is None:
        logger = logging.getLogger("fastmcp")

    formatter = logging.Formatter("%(message)s")

    # Only configure the FastMCP logger namespace
    handler = RichHandler(
        console=Console(stderr=True),
        rich_tracebacks=enable_rich_tracebacks,
        **rich_kwargs,
    )
    handler.setFormatter(formatter)

    # filter to exclude tracebacks
    handler.addFilter(lambda record: record.exc_info is None)

    traceback_handler = RichHandler(
        console=Console(stderr=True),
        show_path=False,
        show_level=False,
        rich_tracebacks=enable_rich_tracebacks,
        tracebacks_max_frames=3,
        tracebacks_suppress=[fastmcp,mcp,pydantic],
        **rich_kwargs,
    )
    traceback_handler.setFormatter(formatter)

    # filter to include tracebacks
    traceback_handler.addFilter(lambda record: record.exc_info is not None)

    logger.setLevel(level)

    # Remove any existing handlers to avoid duplicates on reconfiguration
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)

    logger.addHandler(handler)
    logger.addHandler(traceback_handler)

    # Don't propagate to the root logger
    logger.propagate = False

fastmcp.utilities.logging.configure_logging = configure_logging


if __name__ == "__main__":
    mcp.run(transport="sse",port=5000)