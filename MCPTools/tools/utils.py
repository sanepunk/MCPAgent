import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# from MCPTools.server import mcp
# from MCPTools.loader.loader import *

from ..server import mcp
from ..loader import *
from typing import Dict, Any
import os
from datetime import datetime

@mcp.tool()
def get_datetime() -> dict[str, Any]:
    """
    Returns the current local date and time.

    Returns:
        dict: {"datetime": "YYYY-MM-DD HH:MM:SS"}
    """
    return {"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

@mcp.tool()
def get_project_structure() -> dict[str, Any]:
    """
    Returns the file/folder structure of the current directory.

    Returns:
        dict: Folder and file structure.
    """
    project_structure = {}
    try:
        for root, dirs, files in os.walk("."):
            for name in files:
                project_structure.setdefault(root, {})[name] = "File"
            for name in dirs:
                project_structure.setdefault(root, {})[name] = "Directory"
    except Exception as e:
        return {"error": str(e)}
    return project_structure