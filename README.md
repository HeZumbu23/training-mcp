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
dummy_mcp_server/
  server.py
  requirements.txt
  run.sh
  run.bat
```

## Schnellstart (ein Befehl)

```bash
./dummy_mcp_server/run.sh
```

Windows:

```bat
dummy_mcp_server\run.bat
```

Das Skript installiert die Abhängigkeiten (`mcp`) und startet den Server.

## Setup & lokaler Start (mit venv, optional)

```bash
cd dummy_mcp_server
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

Der Server wartet danach auf stdio-Eingaben gemäß MCP-Protokoll; die
Log-Ausgaben erscheinen auf der Konsole (stderr).

## Einbindung in Visual Studio

1. Python-Umgebung wie oben beschrieben einrichten (venv + `pip install -r requirements.txt`).
2. In der MCP-Server-Konfiguration des jeweiligen Visual-Studio-Features
   (z. B. GitHub Copilot Chat / Agent Mode) einen neuen stdio-MCP-Server
   eintragen, der den Server startet, z. B.:

   ```json
   {
     "servers": {
       "dummy-mcp-server": {
         "type": "stdio",
         "command": "<pfad-zum-repo>/dummy_mcp_server/.venv/bin/python",
         "args": [
           "<pfad-zum-repo>/dummy_mcp_server/server.py"
         ]
       }
     }
   }
   ```

   (Unter Windows entsprechend `...\.venv\Scripts\python.exe`.)

3. Nach dem Verbinden sollten die Tools `echo` und `add` im MCP-Client
   sichtbar sein und aufgerufen werden können; jeder Aufruf wird in der
   Konsole protokolliert.

## Hinweis

Dieses Projekt dient ausschließlich zu Test- und Analysezwecken (z. B. um
den Traffic/das Verhalten eines MCP-Servers innerhalb von Visual Studio zu
untersuchen) und implementiert bewusst nur minimale, ungefährliche
Operationen.
