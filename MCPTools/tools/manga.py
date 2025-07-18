from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Optional, Union
from pydantic import BaseModel
from datetime import datetime
import openai
import os
from ..loader import open_router_open_api_client
# from dotenv import load_dotenv

# load_dotenv()
# openai.api_key = os.getenv("OPENROUTER")

from ..server import mcp

def get_mangadex_status():
    url = "https://status.mangadex.org"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    result = soup.find_all("span", class_="component-status")
    result2 = soup.find_all("span", class_="name")
    
    # Clean up the text by stripping whitespace
    website_status = result[0].text.strip()
    website_name = result2[0].text.strip()
    api_status = result[1].text.strip()
    api_name = result2[1].text.strip()
    cdn_status = result[2].text.strip()
    cdn_name = result2[2].text.strip()
    core_status = result[3].text.strip()
    core_name = result2[3].text.strip()
    
    print("--------------------------------")
    print(f"Website: {website_name} - {website_status}")
    print(f"API: {api_name} - {api_status}")
    print(f"CDN: {cdn_name} - {cdn_status}")
    print(f"Core: {core_name} - {core_status}")
    print("--------------------------------")

class TagAttributes(BaseModel):
    name: Dict[str, str]
    description: Dict[str, str] = {}
    group: str
    version: int

class Tag(BaseModel):
    id: str
    type: str
    attributes: TagAttributes
    relationships: List[Dict] = []

class Relationship(BaseModel):
    id: str
    type: str
    related: Optional[str] = None

class MangaAttributes(BaseModel):
    title: Dict[str, str]
    altTitles: List[Dict[str, str]]
    description: Dict[str, str]
    isLocked: bool
    links: Dict[str, str] = {}
    originalLanguage: str
    lastVolume: Optional[str] = None
    lastChapter: Optional[str] = None
    publicationDemographic: Optional[str] = None
    status: str
    year: Optional[int] = None
    contentRating: str
    tags: List[Tag]
    state: str
    chapterNumbersResetOnNewVolume: bool
    createdAt: str
    updatedAt: str
    version: int
    availableTranslatedLanguages: List[str]
    latestUploadedChapter: Optional[str] = None

class Manga(BaseModel):
    id: str
    type: str
    attributes: MangaAttributes
    relationships: List[Relationship]

def store_manga_data(manga_data: List[dict]) -> List[Manga]:
    """
    Convert raw manga data into Pydantic models
    """
    return [Manga(**manga) for manga in manga_data]

def print_manga_info(mangas: List[Manga]):
    """
    Print formatted manga information
    """
    for manga in mangas:
        print("\n=== Manga Information ===")
        print(f"Title: {manga.attributes.title.get('en', '')}")
        print(f"ID: {manga.id}")
        print(f"Description: {manga.attributes.description.get('en', '')}")
        print(f"Status: {manga.attributes.status}")
        print(f"Year: {manga.attributes.year}")
        print(f"Content Rating: {manga.attributes.contentRating}")
        print("\nAlternative Titles:")
        for alt in manga.attributes.altTitles:
            for lang, title in alt.items():
                print(f"  {lang}: {title}")
        print("\nTags:")
        for tag in manga.attributes.tags:
            print(f"  - {tag.attributes.name.get('en', '')}")
        print("=====================")

# @mcp.tool()
def get_manga_info_json(title: List[Manga], tags: bool = False) -> Dict[str, str]:
    """
    Get manga information in JSON format
    Args:
        title: str -> The title of the manga
        tags: bool -> Whether to include tags in the output
    Returns:
        Dict[str, str]: A dictionary with the manga information
        {"result": str -> The manga information}
    """
    base_url = "https://api.mangadex.org"
    # title = "Rising of the Shield Hero"
    r = requests.get(
        f"{base_url}/manga",
        params={"title": title}
    )
    # print([manga for manga in r.json()["data"]])
    response = r.json()['result']
    if response != "ok":
        print(f"Error: {response}")
        exit()
    manga_data = r.json()["data"]
    # id = manga_data[0]['id']
    # print(manga_data)
    mangas = store_manga_data(manga_data)
    data = []
    def convert_to_bool(tags: Union[bool, str]) -> bool:
        if isinstance(tags, bool):
            return True if tags else False
        elif tags.lower() == "true":
            return True
        elif tags.lower() == "false":
            return False
        else:
            return False
    tags = convert_to_bool(tags)
    if tags:
        for manga in mangas:
            tags = []
            for tag in manga.attributes.tags:
                tags.append(tag.attributes.name.get('en', ''))
            # if title.lower() == manga.attributes.title.get('en', '').lower():
            data.append(
                f"id:{manga.id} title:{manga.attributes.title.get('en', '')},"
                f"description:{manga.attributes.description.get('en', '').replace('\n\n', ' ').replace('\n', ' ')},"
                f"status:{manga.attributes.status},year:{manga.attributes.year},"
                f"contentRating:{manga.attributes.contentRating},tags:{','.join(tags)}"
            )
    else:
        for manga in mangas:
            # if title.lower() == manga.attributes.title.get('en', '').lower():
                data.append(
                    f"id:{manga.id} title:{manga.attributes.title.get('en', '')},"
                    f"description:{manga.attributes.description.get('en', '').replace('\n\n', ' ').replace('\n', ' ')},"
                    f"status:{manga.attributes.status},year:{manga.attributes.year},"
                    f"contentRating:{manga.attributes.contentRating}"
                )
    return {
        "result": "\n".join(data)
        }
@mcp.tool()
def get_summarized_manga_info(title: str, tags: bool = False) -> Dict[str, str]:
    """
    Get summarized Manga, Manhwa, Manhua information from Mangadex
    Args:
        title: str -> The title of the manga to search for
        tags: bool -> Whether to include tags in the manga info
    Returns:
        Dict[str, str]: A dictionary containing the summarized manga information
    """
    # Get manga info using the existing function
    manga_info = get_manga_info_json(title, tags)
    
    # Prepare system message for OpenAI
    system_message = """You are a manga information summarizer. Your task is to:
    1. Take the raw manga data, clean itand create a concise summary with *description*
    2. Focus on the most important details (title, main themes, genre)
    3. If multiple manga are found, summarize each briefly 
    4. Keep the summary under 100 words per manga
    5. Format in a clean, readable way
    6. Return the string with all information in one string as small as possible. Make it limit 300 tokens
    """

    try:
        # Call OpenAI API through OpenRouter
        response = open_router_open_api_client.chat.completions.create(
            model="x-ai/grok-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Please summarize this manga information: {manga_info['result']}"}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        
        summary = response.choices[0].message.content
        return {
            "title": title,
            "summary": summary,
            # "raw_data": manga_info['result']
        }
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}

# Example usage
if __name__ == "__main__":
    result = get_summarized_manga_info("Chainsaw Man", tags=True)
    print(result)









