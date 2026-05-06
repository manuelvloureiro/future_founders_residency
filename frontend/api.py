import os

import httpx

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")


async def fetch_scenario() -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(f"{BACKEND_URL}/api/scenario")
        r.raise_for_status()
        return r.json()


async def approve_insight(insight_id: str) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(
            f"{BACKEND_URL}/api/scenario/approve",
            json={"insight_id": insight_id},
        )
        r.raise_for_status()
        return r.json()
