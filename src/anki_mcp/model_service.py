from typing import Annotated, Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import Field

from .common import anki_call

model_mcp = FastMCP(name="AnkiModelService")


@model_mcp.tool(
    name="modelNamesAndIds",
    description="Gets the complete list of model (note type) names and their IDs. Returns a dictionary mapping model names to IDs.",
)
async def list_model_names_and_ids_tool() -> Dict[str, int]:
    return await anki_call("modelNamesAndIds")


@model_mcp.tool(
    name="findModelsByName",
    description="Gets a list of model definitions for the provided model names.",
)
async def find_models_by_name_tool(
    modelNames: Annotated[List[str], Field(description="A list of model names.")],
) -> List[Dict[str, Any]]:
    return await anki_call("findModelsByName", modelNames=modelNames)


@model_mcp.tool(
    name="modelFieldNames",
    description="Gets the list of field names for the provided model name.",
)
async def get_model_field_names_tool(
    modelName: Annotated[str, Field(description="The name of the model.")],
) -> List[str]:
    return await anki_call("modelFieldNames", modelName=modelName)


@model_mcp.tool(
    name="modelTemplates",
    description="Returns an object indicating the template content for each card of the specified model.",
)
async def get_model_templates_tool(
    modelName: Annotated[str, Field(description="The name of the model.")],
) -> Dict[str, Any]:                                                                 
    return await anki_call("modelTemplates", modelName=modelName)


@model_mcp.tool(
    name="modelStyling",
    description="Gets the CSS styling for the provided model name. Returns an object containing the 'css' field.",
)
async def get_model_styling_tool(
    modelName: Annotated[str, Field(description="The name of the model.")],
) -> Dict[str, Any]:                         
    return await anki_call("modelStyling", modelName=modelName)


@model_mcp.tool(
    name="createModel",
    description="Creates a new model (note type). Returns the created model object.",
)
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
    modelId: Annotated[
        Optional[int], Field(description="Optional model ID to use.")
    ] = None,                                   
) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "modelName": modelName,
        "inOrderFields": inOrderFields,
        "cardTemplates": cardTemplates,
        "isCloze": isCloze,
    }
    if css is not None:
        params["css"] = css
    if modelId is not None:
        params["modelId"] = modelId
    return await anki_call("createModel", **params)


@model_mcp.tool(
    name="updateModelTemplates",
    description="Modifies the templates of an existing model by name.",
)
async def update_model_templates_tool(
    model: Annotated[
        Dict[str, Any],
        Field(
            description="Model object. Must include 'name' (model name) and 'templates' (dict of template name to Front/Back definitions)."
        ),
    ],
) -> None:
    return await anki_call("updateModelTemplates", model=model)


@model_mcp.tool(
    name="updateModelStyling",
    description="Modifies the CSS styling of an existing model by name.",
)
async def update_model_styling_tool(
    model: Annotated[
        Dict[str, Any],
        Field(
            description="Model object. Must include 'name' (model name) and 'css' (the new CSS string)."
        ),
    ],
) -> None:
    return await anki_call("updateModelStyling", model=model)


@model_mcp.tool(
    name="modelFieldAdd", description="Adds a new field to an existing model."
)
async def add_model_field_tool(                                                     
    modelName: Annotated[str, Field(description="Name of the model to modify.")],
    fieldName: Annotated[str, Field(description="Name of the new field to add.")],
    index: Annotated[
        Optional[int],
        Field(description="Optional 0-based index to insert the field at."),
    ] = None,
) -> None:
    params: Dict[str, Any] = {"modelName": modelName, "fieldName": fieldName}
    if index is not None:
        params["index"] = index
    return await anki_call("modelFieldAdd", **params)


@model_mcp.tool(
    name="modelFieldRemove", description="Removes a field from an existing model."
)
async def remove_model_field_tool(                                                        
    modelName: Annotated[str, Field(description="Name of the model to modify.")],
    fieldName: Annotated[str, Field(description="Name of the field to remove.")],
) -> None:
    return await anki_call("modelFieldRemove", modelName=modelName, fieldName=fieldName)
