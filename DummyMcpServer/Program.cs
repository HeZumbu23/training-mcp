using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = Host.CreateApplicationBuilder(args);

// MCP-Server-Logs muessen auf stderr gehen, da stdout fuer das MCP-Protokoll
// (stdio transport) reserviert ist.
builder.Logging.AddConsole(options =>
{
    options.LogToStandardErrorThreshold = Microsoft.Extensions.Logging.LogLevel.Trace;
});

builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();

await builder.Build().RunAsync();
