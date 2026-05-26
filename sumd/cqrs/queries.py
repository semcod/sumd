"""Query pattern implementation for SUMD CQRS architecture."""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from .events import EventStore


@dataclass(frozen=True)
class Query:
    """Base query class for CQRS pattern."""

    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_type: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class QueryHandler(ABC):
    """Base query handler interface."""

    @abstractmethod
    async def handle(self, query: Query) -> Any:
        """Handle a query and return results."""

    @abstractmethod
    def can_handle(self, query_type: str) -> bool:
        """Check if this handler can handle the given query type."""


class QueryBus:
    """Query bus for dispatching queries to appropriate handlers."""

    def __init__(self, event_store: EventStore):
        self._handlers: Dict[str, QueryHandler] = {}
        self._event_store = event_store

    def register_handler(self, query_type: str, handler: QueryHandler) -> None:
        """Register a query handler for a specific query type."""
        self._handlers[query_type] = handler

    async def dispatch(self, query: Query) -> Any:
        """Dispatch a query to the appropriate handler."""
        handler = self._handlers.get(query.query_type)
        if not handler:
            raise ValueError(f"No handler registered for query type: {query.query_type}")
        if not handler.can_handle(query.query_type):
            raise ValueError(f"Handler cannot handle query type: {query.query_type}")
        return await handler.handle(query)


# SUMD-specific query value objects
@dataclass(frozen=True)
class GetSumdDocument(Query):
    """Query to get a SUMD document."""

    query_type: str = "get_sumd_document"
    parameters: Dict[str, Any] = field(default_factory=lambda: {"file_path": ""})


@dataclass(frozen=True)
class ListSumdSections(Query):
    """Query to list sections in a SUMD document."""

    query_type: str = "list_sumd_sections"
    parameters: Dict[str, Any] = field(default_factory=lambda: {"file_path": ""})


@dataclass(frozen=True)
class GetSumdSection(Query):
    """Query to get a specific section from a SUMD document."""

    query_type: str = "get_sumd_section"
    parameters: Dict[str, Any] = field(
        default_factory=lambda: {"file_path": "", "section_name": ""}
    )


@dataclass(frozen=True)
class GetProjectInfo(Query):
    """Query to get project information."""

    query_type: str = "get_project_info"
    parameters: Dict[str, Any] = field(default_factory=lambda: {"project_path": ""})


@dataclass(frozen=True)
class GetEventHistory(Query):
    """Query to get event history for an aggregate."""

    query_type: str = "get_event_history"
    parameters: Dict[str, Any] = field(
        default_factory=lambda: {"aggregate_id": "", "from_version": 0}
    )


@dataclass(frozen=True)
class GetAllEvents(Query):
    """Query to get all events from the event store."""

    query_type: str = "get_all_events"
    parameters: Dict[str, Any] = field(
        default_factory=lambda: {"limit": 100, "offset": 0}
    )


@dataclass(frozen=True)
class SearchDocuments(Query):
    """Query to search SUMD documents."""

    query_type: str = "search_documents"
    parameters: Dict[str, Any] = field(
        default_factory=lambda: {"query": "", "project_path": "", "file_pattern": "*.md"}
    )


@dataclass(frozen=True)
class GetValidationResults(Query):
    """Query to get validation results for a document."""

    query_type: str = "get_validation_results"
    parameters: Dict[str, Any] = field(
        default_factory=lambda: {"file_path": "", "profile": "rich"}
    )


@dataclass(frozen=True)
class ExecuteDslQuery(Query):
    """Query to execute DSL query."""

    query_type: str = "execute_dsl_query"
    parameters: Dict[str, Any] = field(
        default_factory=lambda: {"dsl_expression": "", "context": {}}
    )


# SUMD Query Handler — dispatch-table based (CC=2 for handle())
class SumdQueryHandler(QueryHandler):
    """Handler for SUMD queries using a dispatch table (no if/elif chain)."""

    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store
        # Each key maps directly to its private handler method.
        self._dispatch: Dict[str, Callable[[Query], Any]] = {
            "get_sumd_document": self._handle_get_sumd_document,
            "list_sumd_sections": self._handle_list_sumd_sections,
            "get_sumd_section": self._handle_get_sumd_section,
            "get_project_info": self._handle_get_project_info,
            "get_event_history": self._handle_get_event_history,
            "get_all_events": self._handle_get_all_events,
            "search_documents": self._handle_search_documents,
            "get_validation_results": self._handle_get_validation_results,
            "execute_dsl_query": self._handle_execute_dsl_query,
        }

    def can_handle(self, query_type: str) -> bool:
        return query_type in self._dispatch

    async def handle(self, query: Query) -> Any:
        """Dispatch to the appropriate handler method."""
        fn = self._dispatch.get(query.query_type)
        if fn is None:
            raise ValueError(f"Unknown query type: {query.query_type}")
        return await fn(query)

    # --- individual handler methods ---

    async def _handle_get_sumd_document(self, query: Query) -> Dict[str, Any]:
        from pathlib import Path
        from ..parser import parse_file

        try:
            doc = parse_file(Path(query.parameters.get("file_path")))
            return {
                "success": True,
                "data": {
                    "project_name": doc.project_name,
                    "description": doc.description,
                    "sections": [
                        {
                            "name": s.name,
                            "type": s.type.value,
                            "content": s.content,
                            "level": s.level,
                        }
                        for s in doc.sections
                    ],
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_list_sumd_sections(self, query: Query) -> Dict[str, Any]:
        from pathlib import Path
        from ..parser import parse_file

        try:
            doc = parse_file(Path(query.parameters.get("file_path")))
            return {
                "success": True,
                "data": [
                    {"name": s.name, "type": s.type.value, "level": s.level}
                    for s in doc.sections
                ],
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_get_sumd_section(self, query: Query) -> Dict[str, Any]:
        from pathlib import Path
        from ..parser import parse_file

        section_name = query.parameters.get("section_name")
        try:
            doc = parse_file(Path(query.parameters.get("file_path")))
            for section in doc.sections:
                if section.name.lower() == (section_name or "").lower():
                    return {
                        "success": True,
                        "data": {
                            "name": section.name,
                            "type": section.type.value,
                            "content": section.content,
                            "level": section.level,
                        },
                    }
            return {"success": False, "error": f"Section '{section_name}' not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_get_project_info(self, query: Query) -> Dict[str, Any]:
        from pathlib import Path
        from ..extractor import extract_pyproject, extract_readme_title

        project_path = Path(query.parameters.get("project_path"))
        try:
            pyproj = extract_pyproject(project_path)
            title = extract_readme_title(project_path)
            return {
                "success": True,
                "data": {
                    "name": pyproj.get("name", project_path.name),
                    "version": pyproj.get("version", "0.0.0"),
                    "description": pyproj.get("description", title or ""),
                    "dependencies": pyproj.get("dependencies", []),
                    "dev_dependencies": pyproj.get("dev_dependencies", []),
                    "scripts": pyproj.get("scripts", []),
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_get_event_history(self, query: Query) -> Dict[str, Any]:
        aggregate_id = query.parameters.get("aggregate_id")
        from_version = query.parameters.get("from_version", 0)
        try:
            events = self._event_store.get_events(aggregate_id, from_version)
            return {"success": True, "data": [e.to_dict() for e in events]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_get_all_events(self, query: Query) -> Dict[str, Any]:
        limit = query.parameters.get("limit", 100)
        offset = query.parameters.get("offset", 0)
        try:
            all_events = self._event_store.get_all_events()
            paginated = all_events[offset : offset + limit]
            return {
                "success": True,
                "data": {
                    "events": [e.to_dict() for e in paginated],
                    "total": len(all_events),
                    "limit": limit,
                    "offset": offset,
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_search_documents(self, query: Query) -> Dict[str, Any]:
        from pathlib import Path

        search_query = query.parameters.get("query", "")
        project_path = Path(query.parameters.get("project_path", "."))
        file_pattern = query.parameters.get("file_pattern", "*.md")
        try:
            results = []
            for fp in project_path.rglob(file_pattern):
                if not fp.is_file():
                    continue
                try:
                    content = fp.read_text(encoding="utf-8")
                    if search_query.lower() in content.lower():
                        results.append({
                            "file_path": str(fp.relative_to(project_path)),
                            "size": len(content),
                            "matches": content.lower().count(search_query.lower()),
                        })
                except Exception:
                    continue
            return {"success": True, "data": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_get_validation_results(self, query: Query) -> Dict[str, Any]:
        from pathlib import Path
        from ..parser import validate_sumd_file

        file_path = Path(query.parameters.get("file_path"))
        profile = query.parameters.get("profile", "rich")
        try:
            result = validate_sumd_file(file_path, profile=profile)
            return {
                "success": True,
                "data": {
                    "ok": result["ok"],
                    "markdown": [str(i) for i in result.get("markdown", [])],
                    "codeblocks": [str(i) for i in result.get("codeblocks", [])],
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _handle_execute_dsl_query(self, query: Query) -> Dict[str, Any]:
        return {"success": False, "error": "DSL engine not yet implemented"}
