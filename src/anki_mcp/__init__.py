import asyncio
from typing import Annotated, Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP
from pydantic import Field

url = "http://127.0.0.1:8765"


async def _call(action: str, **params: Any) -> Any:
    async with httpx.AsyncClient() as client:
        result = await client.post(
            url, json={"action": action, "version": 6, "params": params}
        )
        result_json = result.json()
        error = result_json.get("error")
        if error:
            raise Exception(error)
        response = result_json.get("result")
        if response:
            return response
        return result_json


# --- Deck MCP Server ---
deck_mcp = FastMCP(name="AnkiDeckService")


@deck_mcp.resource(
    uri="deck://deck_names_and_ids",
    name="GetDeckNamesAndIds",
    description="Gets the complete list of deck names and their respective IDs.",
    mime_type="application/json",
)
async def get_deck_names_and_ids_resource() -> Dict[str, int]:
    return await _call("deckNamesAndIds")


@deck_mcp.resource(
    uri="deck://{deck_name}/config",
    name="GetDeckConfig",
    description="Gets the configuration group object for the given deck name.",
    mime_type="application/json",
)
async def get_deck_config_resource(deck_name: str) -> Dict[str, Any]:
    return await _call("getDeckConfig", deck=deck_name)


@deck_mcp.resource(
    uri="deck://deck_names",
    name="GetDeckNames",
    description="Gets the complete list of deck names for the current user.",
    mime_type="application/json",
)
async def get_deck_names_resource() -> List[str]:
    return await _call("deckNames")


@deck_mcp.tool(
    description="Creates a new empty deck. Will not overwrite an existing deck with the same name."
)
async def create_deck_tool(
    deck: Annotated[
        str,
        Field(description="The name of the deck to create (e.g., 'Japanese::Tokyo')."),
    ],
) -> int:
    return await _call("createDeck", deck=deck)


@deck_mcp.tool(
    description="Deletes decks with the given names. The 'cardsToo' argument must be specified and set to true."
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
    return await _call("deleteDecks", decks=decks, cardsToo=cardsToo)


@deck_mcp.tool(
    description="Moves cards with the given IDs to a different deck, creating the deck if it doesn't exist yet."
)
async def change_deck_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs to move.")],
    deck: Annotated[str, Field(description="The target deck name.")],
) -> None:
    return await _call("changeDeck", cards=cards, deck=deck)


@deck_mcp.tool(description="Saves the given configuration group.")
async def save_deck_config_tool(
    config: Annotated[
        Dict[str, Any],
        Field(
            description="The deck configuration object to save. Must include an 'id'."
        ),
    ],
) -> bool:
    return await _call("saveDeckConfig", config=config)


# --- Note MCP Server ---
note_mcp = FastMCP(name="AnkiNoteService")


@note_mcp.resource(
    uri="note://find?query={query_string}",
    name="FindNotes",
    description="Returns an array of note IDs for a given Anki search query.",
    mime_type="application/json",
)
async def find_notes_resource(query_string: str) -> List[int]:
    return await _call("findNotes", query=query_string)


@note_mcp.resource(
    uri="note://info_by_ids?note_ids={note_ids_csv}",
    name="GetNotesInfo",
    description="Returns a list of objects containing information for each note ID provided (comma-separated).",
    mime_type="application/json",
)
async def get_notes_info_resource(note_ids_csv: str) -> List[Dict[str, Any]]:
    note_ids = [int(nid.strip()) for nid in note_ids_csv.split(",")]
    return await _call("notesInfo", notes=note_ids)


@note_mcp.resource(
    uri="note://{note_id}/tags",
    name="GetNoteTags",
    description="Gets the tags for a specific note ID.",
    mime_type="application/json",
)
async def get_note_tags_resource(note_id: int) -> List[str]:
    return await _call("getNoteTags", note=note_id)


@note_mcp.tool(
    description="Creates a new note using the given deck, model, fields, and tags. Returns the ID of the created note."
)
async def add_note_tool(
    note: Annotated[
        Dict[str, Any],
        Field(
            description="A dictionary representing the note to add. Should include 'deckName', 'modelName', 'fields', and optionally 'tags', 'options', 'audio', 'video', 'picture'."
        ),
    ],
) -> int:
    return await _call("addNote", note=note)


@note_mcp.tool(description="Modifies the fields of an existing note.")
async def update_note_fields_tool(
    note: Annotated[
        Dict[str, Any],
        Field(
            description="A dictionary representing the note to update. Must include 'id' and 'fields'. Optionally 'audio', 'video', or 'picture'."
        ),
    ],
) -> None:
    return await _call("updateNoteFields", note=note)


@note_mcp.tool(description="Deletes notes with the given IDs.")
async def delete_notes_tool(
    notes: Annotated[List[int], Field(description="A list of note IDs to delete.")],
) -> None:
    return await _call("deleteNotes", notes=notes)


@note_mcp.tool(
    description="Creates multiple notes. See 'addNote' for the structure of each note object in the list."
)
async def add_notes_tool(
    notes: Annotated[
        List[Dict[str, Any]], Field(description="A list of note objects to add.")
    ],
) -> List[Optional[int]]:  # Returns list of new note IDs, or null for errors.
    return await _call("addNotes", notes=notes)


@note_mcp.tool(description="Adds tags to the specified notes.")
async def add_tags_tool(
    notes: Annotated[
        List[int], Field(description="A list of note IDs to add tags to.")
    ],
    tags: Annotated[
        str,
        Field(
            description="A space-separated string of tags to add (e.g., 'tag1 tag2')."
        ),
    ],
) -> None:
    return await _call("addTags", notes=notes, tags=tags)


@note_mcp.tool(description="Removes tags from the specified notes.")
async def remove_tags_tool(
    notes: Annotated[
        List[int], Field(description="A list of note IDs to remove tags from.")
    ],
    tags: Annotated[
        str, Field(description="A space-separated string of tags to remove.")
    ],
) -> None:
    return await _call("removeTags", notes=notes, tags=tags)


@note_mcp.tool(description="Modifies the fields and/or tags of an existing note.")
async def update_note_tool(
    note: Annotated[
        Dict[str, Any],
        Field(
            description="Note object to update. Must include 'id'. Can include 'fields', 'tags', 'audio', 'video', 'picture'."
        ),
    ],
) -> None:
    return await _call("updateNote", note=note)


# --- Card MCP Server ---
card_mcp = FastMCP(name="AnkiCardService")


@card_mcp.resource(
    uri="card://find?query={query_string}",
    name="FindCards",
    description="Returns an array of card IDs for a given Anki search query.",
    mime_type="application/json",
)
async def find_cards_resource(query_string: str) -> List[int]:
    return await _call("findCards", query=query_string)


@card_mcp.resource(
    uri="card://info?cards={card_ids_csv}",
    name="GetCardsInfo",
    description="Returns a list of objects containing information for each card ID provided (comma-separated).",
    mime_type="application/json",
)
async def get_cards_info_resource(card_ids_csv: str) -> List[Dict[str, Any]]:
    card_ids = [int(cid.strip()) for cid in card_ids_csv.split(",")]
    return await _call("cardsInfo", cards=card_ids)


@card_mcp.resource(
    uri="card://to_notes?cards={card_ids_csv}",
    name="ConvertCardsToNotes",
    description="Returns an unordered array of note IDs for the given card IDs (comma-separated).",
    mime_type="application/json",
)
async def cards_to_notes_resource(card_ids_csv: str) -> List[int]:
    card_ids = [int(cid.strip()) for cid in card_ids_csv.split(",")]
    return await _call("cardsToNotes", cards=card_ids)


@card_mcp.resource(
    uri="card://are_suspended?cards={card_ids_csv}",
    name="AreCardsSuspended",
    description="Returns an array indicating whether each given card (comma-separated IDs) is suspended.",
    mime_type="application/json",
)
async def are_cards_suspended_resource(card_ids_csv: str) -> List[Optional[bool]]:
    card_ids = [int(cid.strip()) for cid in card_ids_csv.split(",")]
    return await _call("areSuspended", cards=card_ids)


@card_mcp.resource(
    uri="card://mod_time?cards={card_ids_csv}",
    name="GetCardsModificationTime",
    description="Returns modification time for each card ID provided (comma-separated).",
    mime_type="application/json",
)
async def get_cards_mod_time_resource(card_ids_csv: str) -> List[Dict[str, Any]]:
    card_ids = [int(cid.strip()) for cid in card_ids_csv.split(",")]
    return await _call("cardsModTime", cards=card_ids)


@card_mcp.resource(
    uri="card://{card_id}/suspended",
    name="IsCardSuspended",
    description="Checks if a single card is suspended by its ID.",
    mime_type="application/json",
)
async def is_card_suspended_resource(card_id: int) -> bool:
    return await _call("suspended", card=card_id)


@card_mcp.tool(description="Suspends the specified cards.")
async def suspend_cards_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs to suspend.")],
) -> bool:
    return await _call("suspend", cards=cards)


@card_mcp.tool(description="Unsuspends the specified cards.")
async def unsuspend_cards_tool(
    cards: Annotated[List[int], Field(description="A list of card IDs to unsuspend.")],
) -> bool:
    return await _call("unsuspend", cards=cards)


@card_mcp.tool(description="Sets specific values of a single card. Use with caution.")
async def set_specific_card_value_tool(
    card: Annotated[int, Field(description="The ID of the card to modify.")],
    keys: Annotated[
        List[str],
        Field(
            description="List of card property keys to change (e.g., 'flags', 'odue')."
        ),
    ],
    newValues: Annotated[
        List[str], Field(description="List of new values corresponding to the keys.")
    ],
    warning_check: Annotated[
        Optional[bool],
        Field(description="Set to True for potentially risky operations."),
    ] = None,
) -> List[bool]:
    params = {"card": card, "keys": keys, "newValues": newValues}
    if warning_check is not None:
        params["warning_check"] = warning_check
    return await _call("setSpecificValueOfCard", **params)


# --- Model (Note Type) MCP Server ---
model_mcp = FastMCP(name="AnkiModelService")


@model_mcp.resource(
    uri="model://names_and_ids",
    name="GetModelNamesAndIds",
    description="Gets the complete list of model names and their IDs.",
    mime_type="application/json",
)
async def get_model_names_and_ids_resource() -> Dict[str, int]:
    return await _call("modelNamesAndIds")


@model_mcp.resource(
    uri="model://find_by_name?model_names={model_names_csv}",
    name="FindModelsByName",
    description="Gets a list of model definitions for the provided model names (comma-separated).",
    mime_type="application/json",
)
async def find_models_by_name_resource(model_names_csv: str) -> List[Dict[str, Any]]:
    model_names = [name.strip() for name in model_names_csv.split(",")]
    return await _call("findModelsByName", modelNames=model_names)


@model_mcp.resource(
    uri="model://{model_name}/field_names",
    name="GetModelFieldNames",
    description="Gets the list of field names for the provided model name.",
    mime_type="application/json",
)
async def get_model_field_names_resource(model_name: str) -> List[str]:
    return await _call("modelFieldNames", modelName=model_name)


@model_mcp.resource(
    uri="model://{model_name}/templates",
    name="GetModelTemplates",
    description="Returns an object indicating the template content for each card of the specified model.",
    mime_type="application/json",
)
async def get_model_templates_resource(model_name: str) -> Dict[str, Any]:
    return await _call("modelTemplates", modelName=model_name)


@model_mcp.resource(
    uri="model://{model_name}/styling",
    name="GetModelStyling",
    description="Gets the CSS styling for the provided model name.",
    mime_type="application/json",
)
async def get_model_styling_resource(model_name: str) -> Dict[str, Any]:
    return await _call("modelStyling", modelName=model_name)


@model_mcp.tool(description="Creates a new model (note type).")
async def create_model_tool(
    modelName: Annotated[str, Field(description="The name for the new model.")],
    inOrderFields: Annotated[
        List[str], Field(description="List of field names in order.")
    ],
    cardTemplates: Annotated[
        List[Dict[str, Any]],
        Field(
            description="List of card template definitions. Each dict needs 'Name', 'Front', 'Back'."
        ),
    ],
    css: Annotated[
        Optional[str], Field(description="Optional CSS for the model.")
    ] = None,
    isCloze: Annotated[
        Optional[bool], Field(description="Set to true if this is a Cloze model.")
    ] = False,
) -> Dict[str, Any]:
    params = {
        "modelName": modelName,
        "inOrderFields": inOrderFields,
        "cardTemplates": cardTemplates,
        "isCloze": isCloze,
    }
    if css is not None:
        params["css"] = css
    return await _call("createModel", **params)


@model_mcp.tool(description="Modifies the templates of an existing model by name.")
async def update_model_templates_tool(
    model: Annotated[
        Dict[str, Any],
        Field(
            description="Model object. Must include 'name' (model name) and 'templates' (dict of template name to Front/Back definitions)."
        ),
    ],
) -> None:
    return await _call("updateModelTemplates", model=model)


@model_mcp.tool(description="Modifies the CSS styling of an existing model by name.")
async def update_model_styling_tool(
    model: Annotated[
        Dict[str, Any],
        Field(
            description="Model object. Must include 'name' (model name) and 'css' (the new CSS string)."
        ),
    ],
) -> None:
    return await _call("updateModelStyling", model=model)


@model_mcp.tool(description="Adds a new field to an existing model.")
async def model_field_add_tool(
    modelName: Annotated[str, Field(description="Name of the model to modify.")],
    fieldName: Annotated[str, Field(description="Name of the new field to add.")],
    index: Annotated[
        Optional[int],
        Field(description="Optional 0-based index to insert the field at."),
    ] = None,
) -> None:
    params = {"modelName": modelName, "fieldName": fieldName}
    if index is not None:
        params["index"] = index
    return await _call("modelFieldAdd", **params)


@model_mcp.tool(description="Removes a field from an existing model.")
async def model_field_remove_tool(
    modelName: Annotated[str, Field(description="Name of the model to modify.")],
    fieldName: Annotated[str, Field(description="Name of the field to remove.")],
) -> None:
    return await _call("modelFieldRemove", modelName=modelName, fieldName=fieldName)


# --- Media MCP Server ---
media_mcp = FastMCP(name="AnkiMediaService")


@media_mcp.resource(
    uri="media://files/{filename}",
    name="RetrieveMediaFile",
    description="Retrieves the base64-encoded contents of the specified media file.",
    mime_type="text/plain",  # Anki-Connect returns base64 string
)
async def retrieve_media_file_resource(filename: str) -> str:
    return await _call("retrieveMediaFile", filename=filename)


@media_mcp.resource(
    uri="media://list_files?pattern={pattern}",
    name="GetMediaFileNames",
    description="Gets the names of media files matching the glob pattern.",
    mime_type="application/json",
)
async def get_media_files_names_resource(pattern: str) -> List[str]:
    return await _call("getMediaFilesNames", pattern=pattern)


@media_mcp.tool(
    description="Stores a media file in Anki's media folder. Provide one of 'data' (base64), 'path', or 'url'."
)
async def store_media_file_tool(
    filename: Annotated[
        str, Field(description="The desired filename in Anki's media collection.")
    ],
    data: Annotated[
        Optional[str], Field(description="Base64-encoded file content.")
    ] = None,
    path: Annotated[
        Optional[str], Field(description="Absolute local path to the file.")
    ] = None,
    url: Annotated[
        Optional[str], Field(description="URL to download the file from.")
    ] = None,
    deleteExisting: Annotated[
        Optional[bool],
        Field(
            description="Whether to delete an existing file with the same name. Default is true."
        ),
    ] = True,
) -> str:
    params: Dict[str, Any] = {"filename": filename, "deleteExisting": deleteExisting}
    if data:
        params["data"] = data
    elif path:
        params["path"] = path
    elif url:
        params["url"] = url
    else:
        raise ValueError(
            "One of 'data', 'path', or 'url' must be provided for storeMediaFile."
        )
    return await _call("storeMediaFile", **params)


@media_mcp.tool(description="Deletes the specified file from Anki's media folder.")
async def delete_media_file_tool(
    filename: Annotated[
        str,
        Field(description="The name of the file to delete from the media collection."),
    ],
) -> None:
    return await _call("deleteMediaFile", filename=filename)


anki_mcp = FastMCP(name="AnkiConnectMCP")


async def setup():
    await anki_mcp.import_server("deck", deck_mcp)
    await anki_mcp.import_server("note", note_mcp)
    await anki_mcp.import_server("card", card_mcp)
    await anki_mcp.import_server("model", model_mcp)
    await anki_mcp.import_server("media", media_mcp)
    await anki_mcp.run_async()


def main():

    asyncio.run(setup())


if __name__ == "__main__":
    main()
