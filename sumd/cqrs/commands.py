"""Command pattern implementation for SUMD CQRS architecture."""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from .events import Event, EventStore


@dataclass(frozen=True)
class Command:
    """Base command class for CQRS pattern."""
    command_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    command_type: str = ""
    aggregate_id: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CommandHandler(ABC):
    """Base command handler interface."""
    
    @abstractmethod
    async def handle(self, command: Command) -> List[Event]:
        """Handle a command and return resulting events."""
        pass
    
    @abstractmethod
    def can_handle(self, command_type: str) -> bool:
        """Check if this handler can handle the given command type."""
        pass


class CommandBus:
    """Command bus for dispatching commands to appropriate handlers."""
    
    def __init__(self, event_store: EventStore):
        self._handlers: Dict[str, CommandHandler] = {}
        self._event_store = event_store
    
    def register_handler(self, command_type: str, handler: CommandHandler) -> None:
        """Register a command handler for a specific command type."""
        self._handlers[command_type] = handler
    
    async def dispatch(self, command: Command) -> List[Event]:
        """Dispatch a command to the appropriate handler."""
        handler = self._handlers.get(command.command_type)
        if not handler:
            raise ValueError(f"No handler registered for command type: {command.command_type}")
        
        if not handler.can_handle(command.command_type):
            raise ValueError(f"Handler cannot handle command type: {command.command_type}")
        
        events = await handler.handle(command)
        
        # Store events
        for event in events:
            self._event_store.save_event(event)
        
        return events


# SUMD-specific commands
@dataclass(frozen=True)
class CreateSumdDocument(Command):
    """Command to create a new SUMD document."""
    command_type: str = "create_sumd_document"
    data: Dict[str, Any] = field(default_factory=lambda: {
        "project_name": "",
        "description": "",
        "file_path": "",
        "profile": "rich",
    })


@dataclass(frozen=True)
class UpdateSumdDocument(Command):
    """Command to update an existing SUMD document."""
    command_type: str = "update_sumd_document"
    data: Dict[str, Any] = field(default_factory=lambda: {
        "project_name": "",
        "description": "",
        "file_path": "",
        "changes": {},
    })


@dataclass(frozen=True)
class AddSumdSection(Command):
    """Command to add a section to a SUMD document."""
    command_type: str = "add_sumd_section"
    data: Dict[str, Any] = field(default_factory=lambda: {
        "section_name": "",
        "section_type": "",
        "content": "",
        "level": 2,
    })


@dataclass(frozen=True)
class RemoveSumdSection(Command):
    """Command to remove a section from a SUMD document."""
    command_type: str = "remove_sumd_section"
    data: Dict[str, Any] = field(default_factory=lambda: {
        "section_name": "",
        "section_type": "",
    })


@dataclass(frozen=True)
class ValidateSumdDocument(Command):
    """Command to validate a SUMD document."""
    command_type: str = "validate_sumd_document"
    data: Dict[str, Any] = field(default_factory=lambda: {
        "file_path": "",
        "profile": "rich",
    })


@dataclass(frozen=True)
class ScanProject(Command):
    """Command to scan a project and generate SUMD."""
    command_type: str = "scan_project"
    data: Dict[str, Any] = field(default_factory=lambda: {
        "project_path": "",
        "profile": "rich",
        "fix": False,
        "analyze": False,
        "depth": None,
    })


@dataclass(frozen=True)
class GenerateMap(Command):
    """Command to generate project map."""
    command_type: str = "generate_map"
    data: Dict[str, Any] = field(default_factory=lambda: {
        "project_path": "",
        "force": False,
        "output": None,
    })


@dataclass(frozen=True)
class ExecuteDslCommand(Command):
    """Command to execute DSL command."""
    command_type: str = "execute_dsl_command"
    data: Dict[str, Any] = field(default_factory=lambda: {
        "dsl_expression": "",
        "context": {},
    })


# SUMD Command Handlers
class SumdCommandHandler(CommandHandler):
    """Handler for SUMD commands using a dispatch table."""

    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store
        self._dispatch: Dict[str, Callable[[Command], List[Event]]] = {
            "create_sumd_document": self._handle_create_sumd_document,
            "update_sumd_document": self._handle_update_sumd_document,
            "add_sumd_section": self._handle_add_sumd_section,
            "remove_sumd_section": self._handle_remove_sumd_section,
            "validate_sumd_document": self._handle_validate_sumd_document,
            "scan_project": self._handle_generic,
            "generate_map": self._handle_generic,
            "execute_dsl_command": self._handle_generic,
        }

    def can_handle(self, command_type: str) -> bool:
        return command_type in self._dispatch

    async def handle(self, command: Command) -> List[Event]:
        """Dispatch to specific handler, then append execution audit event."""
        from .events import SumdCommandExecuted

        fn = self._dispatch.get(command.command_type)
        events: List[Event] = []
        if fn is not None:
            events = await fn(command)

        events.append(
            SumdCommandExecuted(
                aggregate_id=command.aggregate_id,
                data={
                    "command": command.command_type,
                    "args": command.data,
                    "result": "success",
                    "duration_ms": 0,
                },
            )
        )
        return events

    # --- individual command handlers ---

    async def _handle_create_sumd_document(self, command: Command) -> List[Event]:
        from .events import SumdDocumentCreated
        return [SumdDocumentCreated(aggregate_id=command.aggregate_id, data=command.data)]

    async def _handle_update_sumd_document(self, command: Command) -> List[Event]:
        from .events import SumdDocumentUpdated
        return [SumdDocumentUpdated(aggregate_id=command.aggregate_id, data=command.data)]

    async def _handle_add_sumd_section(self, command: Command) -> List[Event]:
        from .events import SumdSectionAdded
        return [SumdSectionAdded(aggregate_id=command.aggregate_id, data=command.data)]

    async def _handle_remove_sumd_section(self, command: Command) -> List[Event]:
        from .events import SumdSectionRemoved
        return [SumdSectionRemoved(aggregate_id=command.aggregate_id, data=command.data)]

    async def _handle_validate_sumd_document(self, command: Command) -> List[Event]:
        from ..parser import validate_sumd_file
        from .events import SumdDocumentValidated

        file_path = command.data.get("file_path")
        try:
            result = validate_sumd_file(file_path, profile=command.data.get("profile", "rich"))
            validation_result = "valid" if result["ok"] else "invalid"
            errors = [str(e) for e in result.get("markdown", []) + result.get("codeblocks", [])]
        except Exception as exc:
            validation_result = "error"
            errors = [str(exc)]

        return [
            SumdDocumentValidated(
                aggregate_id=command.aggregate_id,
                data={
                    "file_path": file_path,
                    "validation_result": validation_result,
                    "errors": errors,
                    "warnings": [],
                },
            )
        ]

    async def _handle_generic(self, command: Command) -> List[Event]:
        """Placeholder for commands that emit no domain events."""
        return []
