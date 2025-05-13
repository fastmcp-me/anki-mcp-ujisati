import pytest
import pytest_asyncio
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport

from src.anki_mcp import anki_mcp, setup


@pytest_asyncio.fixture
async def anki():
    await setup()
    transport = FastMCPTransport(mcp=anki_mcp)
    client = Client(transport)
    yield client


@pytest.mark.asyncio
async def test_list_resources(anki: Client):
    async with anki:
        result = await anki.list_resources()
    assert "GetDeckNamesAndIds" in str(result[0])
