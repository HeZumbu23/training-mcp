# dummy-mcp-server

Ein minimaler Model Context Protocol (MCP) Server in Python, gedacht zum
Ausprobieren und Analysieren des MCP-Einsatzes in Visual Studio.

Der Server läuft standardmäßig als **HTTP-Endpoint** (streamable-http) und
stellt zwei einfache Tools bereit:

- **echo(message)** – gibt den übergebenen Text unverändert zurück.
- **add(a, b)** – addiert zwei ganze Zahlen.
- **reverse_text(text)** – gibt den Text rückwärts zurück.
- **current_time()** – gibt die aktuelle Uhrzeit (UTC, ISO-8601) zurück.
- **roll_dice(sides=6, count=1)** – würfelt `count` Würfel mit je `sides` Seiten.

Jeder Tool-Aufruf (inkl. Parameter und Ergebnis) wird protokolliert und auf
der Konsole (stderr) ausgegeben.

Eine kompakte Referenz speziell für den MCP-Client/das LLM (Verbindungsdaten,
Tool-Signaturen, Beispiel-Aufrufe) steht in [`LLM_USAGE.md`](./LLM_USAGE.md).

## Projektstruktur

```
server.py
requirements.txt
run.sh
run.bat
```

## Schnellstart (ein Befehl)

```bash
./run.sh
```

Windows:

```bat
run.bat
```

Das Skript installiert die Abhängigkeit (`mcp`, Version < 2.0 – siehe
Hinweis unten) und startet den Server. Der Endpoint ist danach unter
**http://127.0.0.1:8000/mcp** erreichbar; die Konsole zeigt live jeden
Tool-Aufruf.

## Transport / Endpoint beim Start angeben

Default ist `streamable-http` auf `127.0.0.1:8000`. Host/Port lassen sich
anpassen, und alternative Transporte sind möglich:

```bash
./run.sh --host 0.0.0.0 --port 9000
# Endpoint: http://0.0.0.0:9000/mcp

./run.sh --transport sse --host 127.0.0.1 --port 8000
# Endpoint: http://127.0.0.1:8000/sse

./run.sh --transport stdio
# fuer Clients, die den Prozess selbst starten (siehe unten)
```

Parameter:

| Flag          | Default            | Beschreibung                          |
|---------------|--------------------|-----------------------------------------|
| `--transport` | `streamable-http`  | `streamable-http`, `sse` oder `stdio`   |
| `--host`      | `127.0.0.1`        | Bind-Adresse (nur bei http/sse)         |
| `--port`      | `8000`             | Port (nur bei http/sse)                 |

## Setup & lokaler Start (mit venv, optional)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

## Einbindung in Visual Studio

Als HTTP-Server trägst du nur den Endpoint ein, Visual Studio startet den
Prozess **nicht** selbst – der Server muss also vorher laufen (z. B. via
`./run.sh` in einem eigenen Terminal):

```json
{
  "servers": {
    "dummy-mcp-server": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

Falls dein MCP-Client stattdessen stdio erwartet (er startet den Server
dann selbst als Kindprozess), lässt sich der Server weiterhin so
konfigurieren:

```json
{
  "servers": {
    "dummy-mcp-server": {
      "type": "stdio",
      "command": "python3",
      "args": ["<pfad-zum-repo>/server.py", "--transport", "stdio"]
    }
  }
}
```

Nach dem Verbinden sollten die Tools `echo` und `add` im MCP-Client
sichtbar sein und aufgerufen werden können; jeder Aufruf wird auf der
Konsole protokolliert, in der der Server läuft.

## Hinweis zur `mcp`-Paketversion

Das Paket `mcp` auf PyPI hat ab Version 2.0 seine interne Modulstruktur
geändert; `mcp.server.fastmcp` existiert dort nicht mehr in der gewohnten
Form, was zu `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`
führen kann. `requirements.txt` pinnt deshalb bewusst auf
`mcp>=1.2.0,<2.0.0`. Falls bereits eine 2.x-Version installiert ist:

```bash
pip install "mcp>=1.2.0,<2.0.0" --force-reinstall
```

## Hinweis

Dieses Projekt dient ausschließlich zu Test- und Analysezwecken (z. B. um
den Traffic/das Verhalten eines MCP-Servers innerhalb von Visual Studio zu
untersuchen) und implementiert bewusst nur minimale, ungefährliche
Operationen.
