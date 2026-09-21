# DummyMcpServer

Ein minimaler Model Context Protocol (MCP) Server in C#/.NET 8, gedacht zum
Ausprobieren und Analysieren des MCP-Einsatzes in Visual Studio.

Der Server kommuniziert über stdio und stellt zwei einfache Tools bereit:

- **Echo(message)** – gibt den übergebenen Text unverändert zurück.
- **Add(a, b)** – addiert zwei ganze Zahlen.

## Projektstruktur

```
DummyMcpServer/
  DummyMcpServer.csproj
  Program.cs
  Tools/
    EchoTool.cs
```

## Build & lokaler Start

```bash
cd DummyMcpServer
dotnet build
dotnet run
```

Der Server wartet danach auf stdio-Eingaben gemäß MCP-Protokoll.

## Einbindung in Visual Studio

1. Projekt in Visual Studio 2022 (17.10+) öffnen bzw. `DummyMcpServer.csproj`
   laden.
2. Projekt bauen (`dotnet build` bzw. Build-Menü), damit die ausführbare
   Datei unter `DummyMcpServer/bin/Debug/net8.0/DummyMcpServer.dll` bzw.
   `.exe` entsteht.
3. In der MCP-Server-Konfiguration des jeweiligen Visual-Studio-Features
   (z. B. GitHub Copilot Chat / Agent Mode) einen neuen stdio-MCP-Server
   eintragen, der den Server startet, z. B.:

   ```json
   {
     "servers": {
       "dummy-mcp-server": {
         "type": "stdio",
         "command": "dotnet",
         "args": [
           "run",
           "--project",
           "<pfad-zum-repo>/DummyMcpServer/DummyMcpServer.csproj"
         ]
       }
     }
   }
   ```

   Alternativ auf die bereits gebaute DLL zeigen:

   ```json
   {
     "servers": {
       "dummy-mcp-server": {
         "type": "stdio",
         "command": "dotnet",
         "args": [
           "<pfad-zum-repo>/DummyMcpServer/bin/Debug/net8.0/DummyMcpServer.dll"
         ]
       }
     }
   }
   ```

4. Nach dem Verbinden sollten die Tools `Echo` und `Add` im MCP-Client
   sichtbar sein und aufgerufen werden können.

## Hinweis

Dieses Projekt dient ausschließlich zu Test- und Analysezwecken (z. B. um
den Traffic/Verhalten eines MCP-Servers innerhalb von Visual Studio zu
untersuchen) und implementiert bewusst nur minimale, ungefährliche
Operationen.
