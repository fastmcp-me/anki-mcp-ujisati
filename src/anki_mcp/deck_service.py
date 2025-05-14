from typing import Annotated, Any, Dict, List

from fastmcp import FastMCP
from pydantic import Field

from .common import anki_call

deck_mcp = FastMCP(name="AnkiDeckService")


@deck_mcp.tool(
    name="deckNamesAndIds",
    description="Gets the complete list of deck names and their respective IDs. Returns a dictionary mapping deck names to their IDs.",
)
async def list_deck_names_and_ids_tool() -> Dict[str, int]:
    return await anki_call("deckNamesAndIds")


@deck_mcp.tool(
    name="getDeckConfig",
    description="Gets the configuration group object for the given deck name. Returns the deck configuration object.",
)
async def get_deck_config_tool(
    deck: Annotated[str, Field(description="The name of the deck (e.g., 'Default').")],
) -> Dict[str, Any]:
    return await anki_call("getDeckConfig", deck=deck)


@deck_mcp.tool(
    name="deckNames",
    description="Gets the complete list of deck names for the current user. Returns a list of deck names.",
)
async def list_deck_names_tool() -> List[str]:
    return await anki_call("deckNames")


@deck_mcp.tool(
    name="createDeck",
    description="Creates a new empty deck. Will not overwrite an existing deck with the same name. Returns the ID of the created deck.",
)
async def create_deck_tool(
    deck: Annotated[
        str,
        Field(description="The name of the deck to create (e.g., 'Japanese::Tokyo')."),
    ],
) -> int:
    return await anki_call("createDeck", deck=deck)


@deck_mcp.tool(
    name="deleteDecks",
    description="Deletes decks with the given names. The 'cardsToo' argument must be specified and set to true.",
)
async def delete_decks_tool(
    decks: Annotated[List[str], Field(description="A list of deck names to delete.")],
    cardsToo: Annotated[
        bool,
        Field(
            description="Must be true to confirm deletion of cards within the decks."
        ),
    ],
) -> None:
    if not cardsToo:
        raise ValueError("cardsToo must be true to delete decks.")
    return await anki_call("deleteDecks", decks=decks, cardsToo=cardsToo)


@deck_mcp.tool(
    name="changeDeck",
    description="Moves cards with the given IDs to a different deck, creating the deck if it doesn't exist yet.",
)
async def change_deck_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs to move.")],
    deck: Annotated[str, Field(description="The target deck name.")],
) -> None:
    return await anki_call("changeDeck", cards=cards, deck=deck)


@deck_mcp.tool(
    name="saveDeckConfig",
    description="Saves the given configuration group. Returns true on success, false otherwise.",
)
async def save_deck_config_tool(
    config: Annotated[
        Dict[str, Any],
        Field(
            description="The deck configuration object to save. Must include an 'id'."
        ),
    ],
) -> bool:
    return await anki_call("saveDeckConfig", config=config)
