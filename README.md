# anki-mcp

The most comprehensive Model Context Protocol server for Anki flashcards.

## Prerequisites

- Anki desktop application
- AnkiConnect add-on installed
- uv

## Usage
```bash

# Run
uv run anki-mcp

# Inspect
npx @modelcontextprotocol/inspector uv run anki-mcp
```

## Available MCP Tools & Resources

This MCP server provides access to Anki functionality through the following services:

### Deck Service
- **Resources**: Get deck names, IDs, and configuration
- **Tools**: Create decks, delete decks, change card decks, save deck configuration

### Note Service
- **Resources**: Find notes, get note info, get note tags
- **Tools**: Add notes (single/multiple), update note fields, delete notes, add/remove tags

### Card Service
- **Resources**: Find cards, get card info, check suspension status, get modification time
- **Tools**: Suspend/unsuspend cards, set specific card values

### Model Service
- **Resources**: Get model names/IDs, find models, get field names/templates/styling
- **Tools**: Create models, update templates/styling, add/remove fields

### Media Service
- **Resources**: Retrieve media files, list media files by pattern
- **Tools**: Store media files (from base64/path/URL), delete media files

## Development

```bash
uv pip install -e .

pytest
```
