import os
from shutil import get_terminal_size
from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger, configure_logging

logger = get_logger(__name__)

configure_logging()

logger.info("Starting program")
logger.info("shutil = %s", get_terminal_size())
logger.info("os = %s", os.get_terminal_size())

mcp = FastMCP(__name__)

@mcp.tool()
def shutil_terminal_size():
    return get_terminal_size()

@mcp.tool()
def os_terminal_size():
    return os.get_terminal_size()

@mcp.tool()
def cause_traceback():
    raise Exception("Test exception")

if __name__ == "__main__":
    mcp.run()