"""Minimaler MCP-Server zum Testen der MCP-Integration in Visual Studio.

Stellt zwei einfache Tools bereit (Echo, Add) und protokolliert jeden
Tool-Aufruf inklusive Parametern und Ergebnis auf der Konsole (stderr).

Standardmaessig laeuft der Server ueber stdio. Optional kann er ueber
--transport streamable-http|sse als HTTP-Endpoint gestartet werden, z. B.:

    python server.py --transport streamable-http --host 127.0.0.1 --port 8000

Der Endpoint ist dann unter http://127.0.0.1:8000/mcp erreichbar
(bei --transport sse unter http://127.0.0.1:8000/sse).
"""

import argparse
import logging
import sys

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("dummy-mcp-server")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="dummy-mcp-server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
        help="Transport-Art: stdio (Default, fuer Visual Studio) oder "
        "streamable-http/sse (HTTP-Endpoint zum Testen z. B. mit MCP Inspector).",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host, an den gebunden wird (nur bei --transport http/sse).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port, an den gebunden wird (nur bei --transport http/sse).",
    )
    return parser.parse_args()


args = parse_args()

mcp = FastMCP("dummy-mcp-server", host=args.host, port=args.port)


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
    if args.transport == "stdio":
        logger.info("Starte dummy-mcp-server (stdio transport)...")
    else:
        path = "/mcp" if args.transport == "streamable-http" else "/sse"
        logger.info(
            "Starte dummy-mcp-server (%s transport) auf http://%s:%s%s ...",
            args.transport,
            args.host,
            args.port,
            path,
        )
    mcp.run(transport=args.transport)
