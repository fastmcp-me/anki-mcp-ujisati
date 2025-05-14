import pytest
import pytest_asyncio
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport

from src.anki_mcp import anki_mcp, setup


@pytest_asyncio.fixture
async def anki():
    await setup(run_server=False)
    transport = FastMCPTransport(mcp=anki_mcp)
    client = Client(transport)
    yield client


@pytest.mark.asyncio
async def test_list_tools(anki: Client):
    async with anki:
        result = await anki.list_tools()

    tool_names = {tool.name for tool in result}

    expected_tools = {
        # Deck Service
        "deck_deckNamesAndIds",
        "deck_getDeckConfig",
        "deck_deckNames",
        "deck_createDeck",
        "deck_deleteDecks",
        "deck_changeDeck",
        "deck_saveDeckConfig",
        # Note Service
        "note_findNotes",
        "note_notesInfo",
        "note_getNoteTags",
        "note_addNote",
        "note_updateNoteFields",
        "note_deleteNotes",
        "note_addNotes",
        "note_addTags",
        "note_removeTags",
        "note_updateNote",
        # Card Service
        "card_findCards",
        "card_cardsInfo",
        "card_cardsToNotes",
        "card_areSuspended",
        "card_cardsModTime",
        "card_suspended",
        "card_suspend",
        "card_unsuspend",
        "card_setSpecificValueOfCard",
        # Model Service
        "model_modelNamesAndIds",
        "model_findModelsByName",
        "model_modelFieldNames",
        "model_modelTemplates",
        "model_modelStyling",
        "model_createModel",
        "model_updateModelTemplates",
        "model_updateModelStyling",
        "model_modelFieldAdd",
        "model_modelFieldRemove",
        # Media Service
        "media_retrieveMediaFile",
        "media_getMediaFilesNames",
        "media_storeMediaFile",
        "media_deleteMediaFile",
    }

    assert tool_names == expected_tools, (
        f"Mismatch in tools. Missing: {expected_tools - tool_names}, Unexpected: {tool_names - expected_tools}"
    )
