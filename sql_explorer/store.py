import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class QueryHistoryItem:
    query: str
    error: Optional[str]
    columns: List[str] = field(default_factory=list)
    rows: List[List[Any]] = field(default_factory=list)


@dataclass
class SessionData:
    db_dump: Optional[bytes] = None
    table_names: List[str] = field(default_factory=list)
    schema: Dict[str, Any] = field(default_factory=dict)
    history: List[QueryHistoryItem] = field(default_factory=list)
    updated_at: float = field(default_factory=time.time)


_STORE: Dict[str, SessionData] = {}


def get_or_create_session_id(existing: Optional[str]) -> str:
    if existing and existing in _STORE:
        return existing
    session_id = uuid.uuid4().hex
    _STORE[session_id] = SessionData()
    return session_id


def get_session(session_id: str) -> SessionData:
    if session_id not in _STORE:
        _STORE[session_id] = SessionData()
    _STORE[session_id].updated_at = time.time()
    return _STORE[session_id]
