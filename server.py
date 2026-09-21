"""Minimaler MCP-Server zum Testen der MCP-Integration in Visual Studio.

Stellt zwei einfache Tools bereit (Echo, Add) und protokolliert jeden
Tool-Aufruf inklusive Parametern und Ergebnis.

Standardmaessig laeuft der Server ueber stdio, da Visual Studio den
Prozess dabei selbst startet und verwaltet:

    python server.py

Da VS bei stdio die Konsole des Servers nicht direkt zeigt, wird
zusaetzlich immer in eine Log-Datei (logs/server.log) geschrieben, die
sich unabhaengig davon mitlesen laesst, z. B.:

    tail -f logs/server.log

Optional kann der Server auch als HTTP-Endpoint gestartet werden, z. B.
zum manuellen Testen mit dem MCP Inspector:

    python server.py --transport streamable-http --host 127.0.0.1 --port 8000
"""

import argparse
import logging
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.fastmcp import FastMCP

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIR / "server.log"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="dummy-mcp-server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default="stdio",
        help="Transport-Art: stdio (Default, fuer Visual Studio) oder "
        "streamable-http/sse (HTTP-Endpoint zum manuellen Testen).",
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
    parser.add_argument(
        "--log-file",
        default=str(LOG_FILE),
        help=f"Pfad der Log-Datei (Default: {LOG_FILE}).",
    )
    return parser.parse_args()


args = parse_args()

log_path = Path(args.log_file)
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger("dummy-mcp-server")
logger.info("Log-Datei: %s", log_path)

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


@mcp.tool()
def reverse_text(text: str) -> str:
    """Gibt den uebergebenen Text rueckwaerts zurueck."""
    logger.info("Tool-Aufruf: reverse_text(text=%r)", text)
    result = text[::-1]
    logger.info("Tool-Ergebnis: reverse_text -> %r", result)
    return result


@mcp.tool()
def current_time() -> str:
    """Gibt die aktuelle Uhrzeit (UTC, ISO-8601) zurueck."""
    logger.info("Tool-Aufruf: current_time()")
    result = datetime.now(timezone.utc).isoformat()
    logger.info("Tool-Ergebnis: current_time -> %s", result)
    return result


@mcp.tool()
def roll_dice(sides: int = 6, count: int = 1) -> list[int]:
    """Wuerfelt 'count' Wuerfel mit je 'sides' Seiten und gibt die Ergebnisse zurueck."""
    logger.info("Tool-Aufruf: roll_dice(sides=%s, count=%s)", sides, count)
    if sides < 2:
        raise ValueError("sides muss mindestens 2 sein.")
    if not (1 <= count <= 100):
        raise ValueError("count muss zwischen 1 und 100 liegen.")
    result = [random.randint(1, sides) for _ in range(count)]
    logger.info("Tool-Ergebnis: roll_dice -> %s", result)
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
    try:
        mcp.run(transport=args.transport)
    except KeyboardInterrupt:
        logger.info("Server durch Strg+C beendet.")
