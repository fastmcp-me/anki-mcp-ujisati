from typing import Annotated, Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import Field

from .common import anki_call

note_mcp = FastMCP(name="AnkiNoteService")


@note_mcp.tool(
    name="findNotes",
    description="Returns an array of note IDs for a given Anki search query.",
)
async def find_notes_tool(
    query: Annotated[
        str, Field(description="Anki search query (e.g., 'deck:current card:1').")
    ],
) -> List[int]:
    return await anki_call("findNotes", query=query)


@note_mcp.tool(
    name="notesInfo",
    description="Returns a list of objects containing information for each note ID provided.",
)
async def get_notes_info_tool(
    notes: Annotated[List[int], Field(description="A list of note IDs.")],
) -> List[Dict[str, Any]]:
    return await anki_call("notesInfo", notes=notes)


@note_mcp.tool(
    name="getNoteTags",
    description="Gets the tags for a specific note ID. Returns a list of tags.",
)
async def get_note_tags_tool(
    note: Annotated[int, Field(description="The ID of the note.")],
) -> List[str]:
    return await anki_call("getNoteTags", note=note)


@note_mcp.tool(
    name="addNote",
    description="Creates a new note using the given deck, model, fields, and tags. Returns the ID of the created note or null if the note could not be created.",
)
async def add_note_tool(
    note: Annotated[
        Dict[str, Any],
        Field(
            description="A dictionary representing the note to add. Should include 'deckName', 'modelName', 'fields', and optionally 'tags', 'options', 'audio', 'video', 'picture'."
        ),
    ],
) -> Optional[int]:
    return await anki_call("addNote", note=note)


@note_mcp.tool(
    name="updateNoteFields", description="Modifies the fields of an existing note."
)
async def update_note_fields_tool(
    note: Annotated[
        Dict[str, Any],
        Field(
            description="A dictionary representing the note to update. Must include 'id' and 'fields'. Optionally 'audio', 'video', or 'picture'."
        ),
    ],
) -> None:
    return await anki_call("updateNoteFields", note=note)


@note_mcp.tool(name="deleteNotes", description="Deletes notes with the given IDs.")
async def delete_notes_tool(
    notes: Annotated[List[int], Field(description="A list of note IDs to delete.")],
) -> None:
    return await anki_call("deleteNotes", notes=notes)


@note_mcp.tool(
    name="addNotes",
    description="Creates multiple notes. See 'addNote' for the structure of each note object in the list. Returns a list of new note IDs, or null for notes that couldn't be created.",
)
async def add_notes_tool(
    notes: Annotated[
        List[Dict[str, Any]], Field(description="A list of note objects to add.")
    ],
) -> List[Optional[int]]:
    return await anki_call("addNotes", notes=notes)


@note_mcp.tool(name="addTags", description="Adds tags to the specified notes.")
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
    return await anki_call("addTags", notes=notes, tags=tags)


@note_mcp.tool(name="removeTags", description="Removes tags from the specified notes.")
async def remove_tags_tool(
    notes: Annotated[
        List[int], Field(description="A list of note IDs to remove tags from.")
    ],
    tags: Annotated[
        str, Field(description="A space-separated string of tags to remove.")
    ],
) -> None:
    return await anki_call("removeTags", notes=notes, tags=tags)


@note_mcp.tool(
    name="updateNote",
    description="Modifies the fields and/or tags of an existing note.",
)
async def update_note_tool(
    note: Annotated[
        Dict[str, Any],
        Field(
            description="Note object to update. Must include 'id'. Can include 'fields', 'tags', 'audio', 'video', 'picture'."
        ),
    ],
) -> None:
    return await anki_call("updateNote", note=note)
