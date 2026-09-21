"""Minimaler MCP-Server (stdio) zum Testen der MCP-Integration in Visual Studio.

Stellt zwei einfache Tools bereit (Echo, Add) und protokolliert jeden
Tool-Aufruf inklusive Parametern und Ergebnis auf der Konsole (stderr).
stdout bleibt dabei ausschliesslich fuer das MCP-Protokoll reserviert.
"""

import logging
import sys

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("dummy-mcp-server")

mcp = FastMCP("dummy-mcp-server")


@mcp.tool()
def echo(message: str) -> str:
    """Gibt den uebergebenen Text unveraendert zurueck."""
    logger.info("Tool-Aufruf: echo(message=%r)", message)
    result = f"Echo: {message}"
    logger.info("Tool-Ergebnis: echo -> %r", result)
    return result


@mcp.tool()
def add(a: int, b: int) -> int:
    """Addiert zwei ganze Zahlen und gibt das Ergebnis zurueck."""
    logger.info("Tool-Aufruf: add(a=%s, b=%s)", a, b)
    result = a + b
    logger.info("Tool-Ergebnis: add -> %s", result)
    return result


if __name__ == "__main__":
    logger.info("Starte dummy-mcp-server (stdio transport)...")
    mcp.run(transport="stdio")
