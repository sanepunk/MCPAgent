import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# from MCPTools.server import mcp
# from MCPTools.loader.loader import *

from ..server import mcp
from ..loader import *
from typing import Dict, Any
import requests
from urllib.parse import quote_plus

@mcp.tool()
def internet_search(query: str, depth: str = "basic") -> dict[str, Any]:
    """
    Performs a web search using Tavily.

    Args:
        query (str): Search query.
        depth (str): "basic" or "advanced".
            - "basic": Fast and lightweight (default)
            - "advanced": Slower, more thorough search with broader context
    Returns:
        dict: Search results from Tavily.
    """
    response = client.search(query, search_depth=depth)
    return response

@mcp.tool()
def google_search(query: str) -> Dict[str, str]:
    """
    This function takes a search query and returns a list of search results.
    It uses the Google Custom Search API to get the search results.
    Args:
        query (str): The search query to be used.
        example: "Donald Trump"
    Returns:
        str: A string of the search results.
    """
    query = quote_plus(query)

    url = f"https://www.googleapis.com/customsearch/v1?key={search_api}&cx={programmable_search_engine_id}&q={query}"
    response = requests.get(url)
    # with open("google_search_results3.json", "w") as f:
    #     json.dump(response.json(), f, indent=4)

    search_results = response.json()['items']
    results_list = []
    for i, result in enumerate(search_results, 1):
        title = result.get('title', 'Untitled')
        display_link = result.get('displayLink', '')
        
        # Safely get the description from various possible locations
        context = ''
        if 'pagemap' in result:
            pagemap = result['pagemap']
            if 'metatags' in pagemap and pagemap['metatags']:
                context = pagemap['metatags'][0].get('og:description', '')
            
        # If no og:description found, fall back to the snippet
        if not context:
            context = result.get('snippet', 'No description available')
            
        results_list.append(f"{i}. {title} ({display_link}): {context}")

    results_string = "\n".join(results_list)
    return {
        "results_string": results_string
    }



@mcp.tool()
def search_firecrawl(query: str, limit: int = 5) -> Dict[str, str]:
    """
    Web Search Tool
    This tool is used to search the web for information.
    It uses the Firecrawl API to get the search results.
    Args:
        query (str): The search query to be used.
        limit (int): The number of search results to return.
        example: "Donald Trump" "5"
    Returns:
        str: A string of the search results.
    """
    limit = int(limit)
    response = firecrawl_web_search_app.search(query=query, limit=limit)
    status = response['success']
    if status:
        data = []
        for result in response['data']:
            data.append(
                f"{result['title']} "
                f"({result['url']}): "
                f"{result['description']} "
            )
        return {
            "search_result": "\n".join(data)
        }
    else:
        return {
            "error": response['error']
        }


@mcp.tool()
def deep_research(query: str, max_depth: int = 3) -> Dict[str, str]:
    """
    Deep Web Research Tool
    This tool is used to research the deep web for information.
    It uses the Firecrawl API to get the search results.
    Args:
        query (str): The search query to be used.
        max_depth (int): The maximum depth of the search.
        example: "Donald Trump" "3"
    Returns:
        dict: A dictionary of the search results.
        {"finalAnalysis": str}
    """
    max_depth = int(max_depth)
    response = firecrawl_web_search_app.deep_research(
        query=query,
        max_depth=max_depth,
        system_prompt="When presenting the finalAnalysis, strictly limit the total combined tokens (input + your output) to **no more than 1024 tokens**. Focus on delivering **high-density**, **information-rich feedback**: eliminate redundancy, shrink filler words, and favor compact expressions. Structure content with brief headings, bullet points, equations, or tables where appropriate. Prioritize clarity, precision, and relevance—if a detail isn't essential, omit it. Ensure every sentence adds substantive value."
    )
    if response['success']:
        return {
            "finalAnalysis": response['data']['finalAnalysis'],
        }
    else:
        return {
            "error": response['error']
        }