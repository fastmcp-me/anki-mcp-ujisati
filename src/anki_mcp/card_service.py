from typing import Annotated, Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import Field

from .common import anki_call

card_mcp = FastMCP(name="AnkiCardService")


@card_mcp.tool(
    name="findCards",
    description="Returns an array of card IDs for a given Anki search query.",
)
async def find_cards_tool(
    query: Annotated[
        str, Field(description="Anki search query (e.g., 'deck:current is:new').")
    ],
) -> List[int]:
    return await anki_call("findCards", query=query)


@card_mcp.tool(
    name="cardsInfo",
    description="Returns a list of objects containing information for each card ID provided.",
)
async def get_cards_info_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs.")],
) -> List[Dict[str, Any]]:
    return await anki_call("cardsInfo", cards=cards)


@card_mcp.tool(
    name="cardsToNotes",
    description="Returns an unordered array of note IDs for the given card IDs.",
)
async def convert_cards_to_notes_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs.")],
) -> List[int]:
    return await anki_call("cardsToNotes", cards=cards)


@card_mcp.tool(
    name="areSuspended",
    description="Returns an array indicating whether each given card is suspended. Each item is boolean or null if the card doesn't exist.",
)
async def check_cards_suspended_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs.")],
) -> List[Optional[bool]]:
    return await anki_call("areSuspended", cards=cards)


@card_mcp.tool(
    name="cardsModTime",
    description="Returns modification time for each card ID provided. Result is a list of objects with 'cardId' and 'modTime' (timestamp).",
)
async def get_cards_modification_time_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs.")],
) -> List[Dict[str, Any]]:                                                  
    return await anki_call("cardsModTime", cards=cards)


@card_mcp.tool(
    name="suspended",
    description="Checks if a single card is suspended by its ID. Returns true if suspended, false otherwise.",
)
async def check_card_suspended_tool(
    card: Annotated[int, Field(description="The ID of the card.")],
) -> bool:
    return await anki_call("suspended", card=card)


@card_mcp.tool(
    name="suspend", description="Suspends the specified cards. Returns true on success."
)
async def suspend_cards_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs to suspend.")],
) -> bool:
    return await anki_call("suspend", cards=cards)


@card_mcp.tool(
    name="unsuspend",
    description="Unsuspends the specified cards. Returns true on success.",
)
async def unsuspend_cards_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs to unsuspend.")],
) -> bool:
    return await anki_call("unsuspend", cards=cards)


@card_mcp.tool(
    name="setSpecificValueOfCard",
    description="Sets specific values of a single card. Use with caution. Returns list of booleans indicating success for each key.",
)
async def set_specific_card_value_tool(
    card: Annotated[int, Field(description="The ID of the card to modify.")],
    keys: Annotated[
        List[str],
        Field(
            description="List of card property keys to change (e.g., 'flags', 'odue')."
        ),
    ],
    newValues: Annotated[
        List[Any],                                                             
        Field(description="List of new values corresponding to the keys."),
    ],
    warning_check: Annotated[
        Optional[bool],
        Field(description="Set to True for potentially risky operations."),
    ] = None,
) -> List[bool]:
    params: Dict[str, Any] = {"card": card, "keys": keys, "newValues": newValues}
    if warning_check is not None:
        params["warning_check"] = warning_check
    return await anki_call("setSpecificValueOfCard", **params)
