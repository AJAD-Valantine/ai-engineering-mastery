from backend.core.config import get_settings
from backend.schemas import ToolException
from langchain_mcp_adapters.client import MultiServerMCPClient

settings = get_settings()

server_config = {}

server_config["tavily"] = {
    "transport": "streamable_http",
    "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={settings.tavily_api_key.get_secret_value()}",
}

server_config["custom_tools"] = {
    "transport": "stdio",
    "command": r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\.venv\Scripts\python.exe",
    "args": [
        r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\trip-planning-agent\backend\mcp_setup\server.py"
    ],
    "env": {
        "WEATHER_API_KEY": settings.weather_api_key.get_secret_value(),
        "AVIATIONSTACK_API_KEY": settings.aviationstack_api_key.get_secret_value(),
        "PYTHONPATH": r"C:\Users\HP\OneDrive\Documents\Repos\ai-engineering-mastery\trip-planning-agent",
    },
}

client = MultiServerMCPClient(server_config)


async def get_mcp_tools():
    """Retrieve all available tools across connected MCP servers with graceful error handling."""
    try:
        tools = await client.get_tools()
        return tools
    except (ToolException, Exception) as exc:  # noqa: BLE001
        print(
            f"[MCP] Warning: Failed to retrieve tools from MultiServerMCPClient: {exc}"
        )
        return []

async def get_tool(name: str):
    """
    Return a specific tool by name for direct invocation in agent nodes.

    Usage in an agent:
        tool = await get_tool("get_current_weather")
        result = await tool.ainvoke({"city": "Tokyo"})
    """
    tools = await get_mcp_tools()
    match = next((t for t in tools if t.name == name), None)
    if match is None:
        print(f"[MCP] Tool '{name}' not found. Available: {[t.name for t in tools]}")
    return match
