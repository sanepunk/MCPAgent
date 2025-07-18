import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# from MCPTools.server import mcp
# from MCPTools.loader.loader import *

from ..server import mcp
from ..loader import *

from typing import Dict
import requests


@mcp.tool()
def get_credits() -> Dict[str, str]:
    """
    This function returns the remaining credits for the Firecrawl API.
    Args:
        None
    Returns:
        str: A string of the remaining credits.
    """
    url = "https://api.firecrawl.dev/v1/team/credit-usage"
    headers = {
        "Authorization": f"Bearer {firecrawl_api_key}"
    }
    response = requests.get(url, headers=headers)
    return response.json()