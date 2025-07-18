from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="mcp_tools",
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    # host="127.0.0.1",
    # port=8000
    # stateless_http=True
)

# Import all tools to register them with MCP
import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from .tools.ping import *
# from .tools.trade import *
# from .tools.utils import *
# from .tools.weather import *
# from .tools.web_search import *
# from .tools.wiki import *
# from .tools.manga import *
from .tools import *

def run_server(transport: str = 'stdio'):
    """
    Run the MCP server with all tools loaded
    Args:
        transport (str): The transport to use ('streamable-http' or 'stdio')
    """
    print("Starting MCP server with the following tools:")
    # tools = mcp.list_tools()
    # for tool in tools:
    #     print(f"- {tool.name}")
    
    mcp.run(transport=transport)

if __name__ == "__main__":
    run_server()