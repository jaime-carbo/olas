import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.environ.get("MONGODB_URI", "")
MONGODB_DB = os.environ.get("MONGODB_DB", "olas_metrics")
MOCK_MODE = not MONGODB_URI

_client = None
_db = None


def get_db():
    return _db


def is_connected():
    return _db is not None


async def connect():
    global _client, _db
    if MOCK_MODE:
        print("DB | mock mode (no MONGODB_URI)")
        return
    try:
        _client = AsyncIOMotorClient(MONGODB_URI)
        await _client.admin.command("ping")
        _db = _client[MONGODB_DB]
        await _db["clicks"].create_index("timestamp")
        await _db["clicks"].create_index("section")
        await _db["dwell"].create_index("timestamp")
        await _db["dwell"].create_index("section")
        await _db["dwell"].create_index("session_id")
        print(f"DB | connected to {MONGODB_URI}")
        print("DB | indexes ready")
    except Exception as e:
        _client = None
        _db = None
        print(f"DB | connection failed: {e}")


async def disconnect():
    global _client, _db
    if _client:
        _client.close()
    _client = None
    _db = None
