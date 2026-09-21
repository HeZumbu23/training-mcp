using System.ComponentModel;
using ModelContextProtocol.Server;

namespace DummyMcpServer.Tools;

[McpServerToolType]
public static class EchoTool
{
    [McpServerTool, Description("Gibt den uebergebenen Text unveraendert zurueck. Dient als einfache Test-Operation fuer die MCP-Integration.")]
    public static string Echo([Description("Der Text, der zurueckgegeben werden soll.")] string message)
    {
        return $"Echo: {message}";
    }

    [McpServerTool, Description("Addiert zwei ganze Zahlen und gibt das Ergebnis zurueck.")]
    public static int Add(
        [Description("Erster Summand.")] int a,
        [Description("Zweiter Summand.")] int b)
    {
        return a + b;
    }
}
