import asyncio

from fastmcp import FastMCP

from .card_service import card_mcp
from .deck_service import deck_mcp
from .media_service import media_mcp
from .model_service import model_mcp
from .note_service import note_mcp


anki_mcp = FastMCP(
    name="AnkiConnectMCP",
    instructions="""
    This MCP provides a programmatic interface to Anki flashcard functionality through the AnkiConnect API.
    It allows AI assistants to interact with Anki decks, cards, notes, models, and media
    without needing to understand the underlying API details. All interactions are through tools.
    """,
)


async def setup(run_server: bool = True):
    await anki_mcp.import_server("deck", deck_mcp)
    await anki_mcp.import_server("note", note_mcp)
    await anki_mcp.import_server("card", card_mcp)
    await anki_mcp.import_server("model", model_mcp)
    await anki_mcp.import_server("media", media_mcp)
    if run_server:
        await anki_mcp.run_async()


def main():
    asyncio.run(setup(run_server=True))


if __name__ == "__main__":
    main()
