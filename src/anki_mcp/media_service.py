from typing import Annotated, Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import Field

from .common import anki_call

media_mcp = FastMCP(name="AnkiMediaService")


@media_mcp.tool(
    name="retrieveMediaFile",
    description="Retrieves the base64-encoded contents of the specified media file. Returns the base64 string or false if not found.",
)
async def retrieve_media_file_tool(
    filename: Annotated[
        str, Field(description="The name of the media file in Anki's collection.")
    ],
) -> Any:                                          
    return await anki_call("retrieveMediaFile", filename=filename)


@media_mcp.tool(
    name="getMediaFilesNames",
    description="Gets the names of media files matching the glob pattern. Returns a list of filenames.",
)
async def list_media_files_names_tool(                                               
    pattern: Annotated[
        str, Field(description="A glob pattern to match filenames (e.g., '*.jpg').")
    ],
) -> List[str]:
    return await anki_call("getMediaFilesNames", pattern=pattern)


@media_mcp.tool(
    name="storeMediaFile",
    description="Stores a media file in Anki's media folder. Provide one of 'data' (base64), 'path', or 'url'. Returns the stored filename or false on error.",
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
) -> Any:                                            
    params: Dict[str, Any] = {"filename": filename}
    source_count = sum(1 for src in (data, path, url) if src is not None)
    if source_count != 1:
        raise ValueError(
            "Exactly one of 'data', 'path', or 'url' must be provided for storeMediaFile."
        )

    if data:
        params["data"] = data
    elif path:
        params["path"] = path
    elif url:
        params["url"] = url

    if (
        deleteExisting is not None
    ):                                                                
        params["deleteExisting"] = deleteExisting

    return await anki_call("storeMediaFile", **params)


@media_mcp.tool(
    name="deleteMediaFile",
    description="Deletes the specified file from Anki's media folder.",
)
async def delete_media_file_tool(
    filename: Annotated[
        str,
        Field(description="The name of the file to delete from the media collection."),
    ],
) -> None:
    return await anki_call("deleteMediaFile", filename=filename)
