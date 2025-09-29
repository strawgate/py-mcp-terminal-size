import os
from shutil import get_terminal_size
from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger, configure_logging

from typing import Literal, Any
import logging
from rich.logging import RichHandler
from rich.console import Console

import fastmcp

logger = get_logger(__name__)

console = Console(stderr=True)

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
    # Check if logging is disabled in settings
    if not fastmcp.settings.log_enabled:
        return

    # Use settings default if not specified
    if enable_rich_tracebacks is None:
        enable_rich_tracebacks = fastmcp.settings.enable_rich_tracebacks

    if logger is None:
        logger = logging.getLogger("fastmcp")

    # Only configure the FastMCP logger namespace
    handler = RichHandler(
        console=console,
        rich_tracebacks=enable_rich_tracebacks,
        **rich_kwargs,
    )
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    logger.setLevel(level)

    # Remove any existing handlers to avoid duplicates on reconfiguration
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)

    logger.addHandler(handler)

    # Don't propagate to the root logger
    logger.propagate = False

configure_logging()

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
    logger.info(str(console))
    raise Exception("Test exception")

@mcp.tool()
def get_environment():
    return {k: v for k, v in os.environ.items()}

@mcp.tool()
def get_columns():
    return os.environ.get("COLUMNS")

@mcp.tool()
def get_console():
    return str(console)

if __name__ == "__main__":
    mcp.run(transport="sse",port=5000)