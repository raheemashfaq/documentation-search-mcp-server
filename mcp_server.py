
import os
import httpx

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from utils import clean_html_to_text

load_dotenv()

mcp = FastMCP("docs")

DOCS_URLS = {
    "langchain": "https://python.langchain.com/docs/",
    "llama-index": "https://docs.llamaindex.ai/",
    "openai": "https://platform.openai.com/docs/",
    "uv": "https://docs.astral.sh/uv/",
}


async def search_web(query: str) -> dict | None:
    url = "https://google.serper.dev/search"

    payload = {
        "q": query,
        "num": 2
    }

    headers = {
        "X-API-KEY": os.getenv("SERVER_API"),
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()


async def fetch_url(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return clean_html_to_text(response.text)


@mcp.tool()
async def get_docs(query: str, library: str) -> list:
    """
    Search the latest official documentation for a given query and library.
    Supports LangChain, OpenAI, LlamaIndex, and UV.
    Returns summarized documentation text with source links.
    """

    if library not in DOCS_URLS:
        raise ValueError(
            f"Unsupported library: {library}"
        )

    search_query = (
        f"site:{DOCS_URLS[library]} {query}"
    )

    results = await search_web(search_query)

    if not results or not results.get("organic"):
        return []

    text_parts = []

    for result in results["organic"][:2]:
        url = result.get("link")

        if not url:
            continue

        text = await fetch_url(url)

        text_parts.append({
            "source": url,
            "text": text
        })

    return text_parts


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()