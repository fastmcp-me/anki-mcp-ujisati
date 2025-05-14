from typing import Any

import httpx

ANKICONNECT_URL = "http://127.0.0.1:8765"


async def anki_call(action: str, **params: Any) -> Any:
    async with httpx.AsyncClient() as client:
        payload = {"action": action, "version": 6, "params": params}
        result = await client.post(ANKICONNECT_URL, json=payload)
        result.raise_for_status()                                      
        result_json = result.json()
        error = result_json.get("error")
        if error:
            raise Exception(f"AnkiConnect error for action '{action}': {error}")
        response = result_json.get("result")
                                                             
                                                                                                     
                                                                                        
        if "result" in result_json:
            return response
        return result_json                                                                        
