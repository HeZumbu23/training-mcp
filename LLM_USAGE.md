# dummy-mcp-server – Nutzungsanleitung für LLM/Agent-Clients

Diese Datei richtet sich an ein LLM bzw. einen MCP-Client (z. B. Visual
Studio / GitHub Copilot Agent Mode), das diesen Server ansteuert. Sie
beschreibt, wie verbunden wird und welche Tools zur Verfügung stehen.

## Verbindung

- **Protokoll:** Model Context Protocol (MCP) über JSON-RPC 2.0.
- **Transport (Default):** `streamable-http`.
- **Endpoint:** `http://127.0.0.1:8000/mcp` (Host/Port ggf. abweichend,
  siehe Startkommando des Servers).
- **Es gibt genau einen Endpoint.** Es existieren KEINE separaten
  REST-Pfade pro Tool (also kein `/tools/<name>`). Jeder Tool-Aufruf
  läuft über eine JSON-RPC-Nachricht mit Methode `tools/call` gegen den
  einen `/mcp`-Endpoint.
- Vor dem ersten `tools/call` muss – wie bei MCP üblich – die
  `initialize`-Handshake-Sequenz durchgeführt werden; die meisten
  MCP-Client-Bibliotheken (inkl. der in Visual Studio genutzten)
  erledigen das automatisch.
- Alternative Transporte (nur falls der Client das explizit braucht):
  `sse` (`http://127.0.0.1:8000/sse`) oder `stdio` (Server wird dann vom
  Client selbst als Kindprozess gestartet, Flag `--transport stdio`).

## Server-Identität

- **Name:** `dummy-mcp-server`
- **Zweck:** Test-/Demo-Server ohne echte Fachlogik. Alle Tools sind
  bewusst simpel und ungefährlich (reine Berechnungen, kein Datei- oder
  Netzwerkzugriff, keine Secrets).

## Verfügbare Tools

### `echo`
Gibt den übergebenen Text unverändert (mit Präfix) zurück.

- **Parameter:**
  - `message: string` (Pflicht)
- **Rückgabe:** `string`
- **Beispiel-Aufruf:** `echo(message="Hallo")` → `"Echo: Hallo"`

### `add`
Addiert zwei ganze Zahlen.

- **Parameter:**
  - `a: integer` (Pflicht)
  - `b: integer` (Pflicht)
- **Rückgabe:** `integer`
- **Beispiel-Aufruf:** `add(a=2, b=3)` → `5`

### `reverse_text`
Dreht einen String zeichenweise um.

- **Parameter:**
  - `text: string` (Pflicht)
- **Rückgabe:** `string`
- **Beispiel-Aufruf:** `reverse_text(text="abc")` → `"cba"`

### `current_time`
Gibt die aktuelle Uhrzeit in UTC zurück.

- **Parameter:** keine
- **Rückgabe:** `string` (ISO-8601, z. B. `"2026-09-21T12:14:31.227000+00:00"`)
- **Beispiel-Aufruf:** `current_time()` → `"2026-09-21T12:14:31.227000+00:00"`

### `roll_dice`
Würfelt eine oder mehrere Würfel.

- **Parameter:**
  - `sides: integer` (optional, Default `6`, muss ≥ 2 sein)
  - `count: integer` (optional, Default `1`, muss zwischen 1 und 100 liegen)
- **Rückgabe:** `array<integer>` – ein Wert pro Würfel
- **Fehlerfälle:** ungültige `sides`/`count` lösen einen Tool-Fehler
  (`ValueError`) aus, der als MCP-Fehlerantwort zurückkommt.
- **Beispiel-Aufruf:** `roll_dice(sides=20, count=3)` → `[14, 2, 19]`

## Beobachtbarkeit

Jeder Tool-Aufruf (Parameter + Ergebnis) wird auf der Konsole geloggt,
in der der Server läuft (stderr). Das dient ausschließlich der
menschlichen Analyse während der Visual-Studio-Integrationstests und
ist für den Client selbst nicht relevant.
