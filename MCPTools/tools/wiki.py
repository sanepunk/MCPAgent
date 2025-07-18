import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# from MCPTools.server import mcp
# from MCPTools.loader.loader import *

from ..server import mcp
from ..loader.loader import *
from typing import Dict, Any
import requests

@mcp.tool() 
def wikipedia_search(query: str, search_limit: str = "5") -> Dict[str, str]:
    """
    This function takes a search query and returns a list of search results.
    It uses the Wikipedia API to get the search results.
    Args:
        query (str): The search query to be used.
        search_limit (str): The number of search results to return.
        example: "Donald Trump" "5"
    Returns:
        str: A string of the search results.
    """
    # query = quote_plus(query)
    # url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
    # response = requests.get(url)
    # with open("wikipedia_search_results.json", "w") as f:
    #     json.dump(response.json(), f, indent=4)
    # return {
    #     "results_string": response.json()
    # }
    search_limit = int(search_limit)
    URL = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'srlimit': search_limit
    }
    r = requests.get(URL, params=params)
    # with open("wikipedia_search_results.json", "w") as f:
    #     json.dump(r.json(), f, indent=4)
    results = r.json()['query']['search']

    titles = [r['title'] for r in results]
    page_ids = [r['pageid'] for r in results]
    d = []
    q = []
    for title, page_id in zip(titles, page_ids):
        p = requests.get(URL, params={
            'action': 'query',
            'format': 'json',
            'prop': 'extracts|info',
            'explaintext': True,
            'exintro': True,
            'titles': title,
            'inprop': 'url'
        }).json()
        # q.append(p)
        # page = next(iter(p['query']['pages'].values()))
        page = p['query']['pages'][str(page_id)]
        data = f"{page['title']} ({page['fullurl']}): {page['extract']}"
        # data = p.get('')
        d.append(data)
        # print(page['title'], page['extract'], page['fullurl'])
    # with open("wikipedia_search_results33.json", "w") as f:
    #     json.dump(q, f, indent=4)
    return {
        "results_string": "\n".join(d)
    }