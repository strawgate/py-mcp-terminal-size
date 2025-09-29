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

if __name__ == "__main__":
    mcp.run(transport="sse",port=5000)