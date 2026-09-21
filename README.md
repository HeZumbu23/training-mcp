# dummy-mcp-server

Ein minimaler Model Context Protocol (MCP) Server in Python, gedacht zum
Ausprobieren und Analysieren des MCP-Einsatzes in Visual Studio.

Der Server kommuniziert über stdio und stellt zwei einfache Tools bereit:

- **echo(message)** – gibt den übergebenen Text unverändert zurück.
- **add(a, b)** – addiert zwei ganze Zahlen.

Jeder Tool-Aufruf (inkl. Parameter und Ergebnis) wird protokolliert und auf
der Konsole (stderr) ausgegeben. stdout bleibt dabei ausschließlich für das
MCP-Protokoll reserviert.

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
Hinweis unten) und startet den Server.

## Transport / Endpoint beim Start angeben

Standardmäßig läuft der Server über **stdio** (für die Einbindung in
Visual Studio, siehe unten). Optional kann er auch als HTTP-Endpoint
gestartet werden, z. B. zum Testen mit dem
[MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
./run.sh --transport streamable-http --host 127.0.0.1 --port 8000
# Endpoint: http://127.0.0.1:8000/mcp

./run.sh --transport sse --host 127.0.0.1 --port 8000
# Endpoint: http://127.0.0.1:8000/sse
```

Parameter:

| Flag          | Default     | Beschreibung                                   |
|---------------|-------------|-------------------------------------------------|
| `--transport` | `stdio`     | `stdio`, `streamable-http` oder `sse`           |
| `--host`      | `127.0.0.1` | Bind-Adresse (nur bei http/sse)                 |
| `--port`      | `8000`      | Port (nur bei http/sse)                         |

## Setup & lokaler Start (mit venv, optional)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

Der Server wartet danach auf stdio-Eingaben gemäß MCP-Protokoll; die
Log-Ausgaben erscheinen auf der Konsole (stderr).

## Einbindung in Visual Studio

1. Abhängigkeiten installieren, z. B. mit `./run.sh` einmal ausführen
   (oder `pip install -r requirements.txt`, optional in einem venv).
2. In der MCP-Server-Konfiguration des jeweiligen Visual-Studio-Features
   (z. B. GitHub Copilot Chat / Agent Mode) einen neuen stdio-MCP-Server
   eintragen, der den Server startet, z. B.:

   ```json
   {
     "servers": {
       "dummy-mcp-server": {
         "type": "stdio",
         "command": "python3",
         "args": [
           "<pfad-zum-repo>/server.py"
         ]
       }
     }
   }
   ```

   (Unter Windows `python` bzw. den Pfad zur `.venv\Scripts\python.exe`,
   falls ein venv verwendet wird.)

3. Nach dem Verbinden sollten die Tools `echo` und `add` im MCP-Client
   sichtbar sein und aufgerufen werden können; jeder Aufruf wird in der
   Konsole protokolliert.

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
