using System.ComponentModel;
using Microsoft.Extensions.Logging;
using ModelContextProtocol.Server;

namespace DummyMcpServer.Tools;

[McpServerToolType]
public static class EchoTool
{
    [McpServerTool, Description("Gibt den uebergebenen Text unveraendert zurueck. Dient als einfache Test-Operation fuer die MCP-Integration.")]
    public static string Echo(
        ILogger<EchoTool> logger,
        [Description("Der Text, der zurueckgegeben werden soll.")] string message)
    {
        logger.LogInformation("Tool-Aufruf: Echo(message=\"{Message}\")", message);

        var result = $"Echo: {message}";

        logger.LogInformation("Tool-Ergebnis: Echo -> \"{Result}\"", result);

        return result;
    }

    [McpServerTool, Description("Addiert zwei ganze Zahlen und gibt das Ergebnis zurueck.")]
    public static int Add(
        ILogger<EchoTool> logger,
        [Description("Erster Summand.")] int a,
        [Description("Zweiter Summand.")] int b)
    {
        logger.LogInformation("Tool-Aufruf: Add(a={A}, b={B})", a, b);

        var result = a + b;

        logger.LogInformation("Tool-Ergebnis: Add -> {Result}", result);

        return result;
    }
}
