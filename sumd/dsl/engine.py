"""DSL Engine for executing SUMD DSL expressions."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass

from .parser import DSLExpression, DSLExpressionType, parse_dsl
from ..cqrs.commands import CommandBus, Command
from ..cqrs.queries import QueryBus, Query
from .schema import (
    DSLProjectSchema,
    DSLContext as SchemaDSLContext,
    DEFAULT_PROJECT_SCHEMA,
)
from .schema_commands import SchemaCommandRegistry, SchemaBasedCommands
from .context_mixin import VariableMixin


@dataclass
class DSLContext(VariableMixin):
    """Execution context for DSL expressions."""
    variables: Dict[str, Any]
    functions: Dict[str, Callable]
    working_directory: Path
    metadata: Dict[str, Any]
    
    def __init__(self, working_directory: Path = None):
        self.variables = {}
        self.functions = {}
        self.working_directory = working_directory or Path.cwd()
        self.metadata = {}
    
    def register_function(self, name: str, func: Callable) -> None:
        """Register a function in the context."""
        self.functions[name] = func
    
    def get_function(self, name: str) -> Optional[Callable]:
        """Get a function from the context."""
        return self.functions.get(name)


# ---------------------------------------------------------------------------
# Operator dispatch maps — defined at module level to avoid re-creation
# ---------------------------------------------------------------------------

_COMPARISON_OPS: dict[str, Any] = {
    "==": lambda l, r: l == r,
    "!=": lambda l, r: l != r,
    "<":  lambda l, r: l < r,
    "<=": lambda l, r: l <= r,
    ">": lambda l, r: l > r,
    ">=": lambda l, r: l >= r,
    "contains":   lambda l, r: str(r) in str(l),
    "startswith": lambda l, r: str(l).startswith(str(r)),
    "endswith":   lambda l, r: str(l).endswith(str(r)),
}

_ARITHMETIC_OPS: dict[str, Any] = {
    "+":  lambda l, r: l + r,
    "-":  lambda l, r: l - r,
    "*":  lambda l, r: l * r,
    "/":  lambda l, r: l / r,
    "%":  lambda l, r: l % r,
    "**": lambda l, r: l ** r,
}


class DSLEngine:
    """Engine for executing DSL expressions."""
    
    def __init__(self, 
                 command_bus: Optional[CommandBus] = None, 
                 query_bus: Optional[QueryBus] = None,
                 project_schema: Optional[DSLProjectSchema] = None):
        self.command_bus = command_bus
        self.query_bus = query_bus
        self.project_schema = project_schema or DEFAULT_PROJECT_SCHEMA
        self.built_in_functions = self._initialize_builtin_functions()
        
        # Initialize schema-based commands
        self.schema_registry = SchemaCommandRegistry(self.project_schema)
        self.schema_commands = SchemaBasedCommands(
            DSLContext(self.project_schema.root_path),
            self.schema_registry
        )
    
    async def execute(self, expression: DSLExpression, context: DSLContext) -> Any:
        """Execute a DSL expression in the given context."""
        return await self._execute_expression(expression, context)
    
    async def execute_text(self, text: str, context: DSLContext) -> Any:
        """Parse and execute DSL text."""
        # Check if this is natural language input
        if self._is_natural_language(text):
            nlp_result = self.schema_registry.process_natural_language(text)
            if nlp_result.success:
                # Convert NLP result to DSL and execute
                dsl_command = nlp_result.result["dsl_command"]
                return await self.execute_text(dsl_command, context)
        
        expression = parse_dsl(text)
        return await self.execute(expression, context)
    
    def _is_natural_language(self, text: str) -> bool:
        """Check if input is natural language rather than DSL."""
        # Simple heuristic: if it contains spaces and no special DSL characters
        dsl_chars = ["=", "+", "*", "/", "-", "(", ")", "[", "]", "{", "}", "|", "&", "!", "<", ">"]
        has_dsl_chars = any(char in text for char in dsl_chars)
        has_spaces = " " in text.strip()
        
        return has_spaces and not has_dsl_chars and len(text.split()) > 2
    
    async def process_natural_language(self, text: str) -> Any:
        """Process natural language input."""
        return self.schema_registry.process_natural_language(text)
    
    def get_suggestions(self, partial_input: str) -> List[str]:
        """Get command suggestions."""
        return self.schema_registry.get_suggestions(partial_input)
    
    def _build_dispatch_table(self) -> dict:
        """Build expression-type → handler dispatch table."""
        return {
            DSLExpressionType.ASSIGNMENT:     self._execute_assignment,
            DSLExpressionType.COMMAND:        self._execute_command,
            DSLExpressionType.FUNCTION_CALL:  self._execute_function_call,
            DSLExpressionType.PROPERTY_ACCESS: self._execute_property_access,
            DSLExpressionType.COMPARISON:     self._execute_comparison,
            DSLExpressionType.LOGICAL:        self._execute_logical,
            DSLExpressionType.ARITHMETIC:     self._execute_arithmetic,
            DSLExpressionType.PIPELINE:       self._execute_pipeline,
            DSLExpressionType.LIST:           self._execute_list,
            DSLExpressionType.DICT:           self._execute_dict,
            DSLExpressionType.BLOCK:          self._execute_block,
        }

    async def _execute_expression(self, expression: DSLExpression, context: DSLContext) -> Any:
        """Execute a single DSL expression."""
        if expression.type == DSLExpressionType.LITERAL:
            return expression.value
        if expression.type == DSLExpressionType.IDENTIFIER:
            return context.get_variable(expression.value) or expression.value

        handler = self._build_dispatch_table().get(expression.type)
        if handler is None:
            raise ValueError(f"Unknown expression type: {expression.type}")
        return await handler(expression, context)
    
    async def _execute_assignment(self, expression: DSLExpression, context: DSLContext) -> Any:
        """Execute assignment expression."""
        if len(expression.children) != 2:
            raise ValueError("Assignment requires exactly 2 children")
        
        left = expression.children[0]
        right = expression.children[1]
        
        if left.type != DSLExpressionType.IDENTIFIER:
            raise ValueError("Left side of assignment must be identifier")
        
        value = await self._execute_expression(right, context)
        context.set_variable(left.value, value)
        
        return value
    
    async def _resolve_schema_call(
        self, name: str, args: list, context: DSLContext
    ) -> tuple[bool, Any]:
        """Try to dispatch *name* as a schema command. Returns (handled, result)."""
        command_schema = self.schema_registry.get_command(name)
        if command_schema is None:
            return False, None
        named_args = {
            command_schema.parameters[i].name: v
            for i, v in enumerate(args)
            if i < len(command_schema.parameters)
        }
        self.schema_commands.context = context
        return True, await self.schema_commands.execute_command(name, named_args)

    async def _evaluate_args(
        self, expression: DSLExpression, context: DSLContext
    ) -> list:
        """Evaluate all child expressions and return their values."""
        return [
            await self._execute_expression(child, context)
            for child in expression.children
        ]

    async def _execute_command(self, expression: DSLExpression, context: DSLContext) -> Any:
        """Execute command expression."""
        command_name = expression.value
        args = await self._evaluate_args(expression, context)

        handled, result = await self._resolve_schema_call(command_name, args, context)
        if handled:
            return result

        if command_name in self.built_in_functions:
            return await self._call_function(self.built_in_functions[command_name], args, context)
        if command_name in context.functions:
            return await self._call_function(context.functions[command_name], args, context)
        if self.command_bus:
            return await self._execute_sumd_command(command_name, args, context)
        if not args:
            return command_name
        raise ValueError(f"Unknown command: {command_name}")
    
    async def _execute_function_call(self, expression: DSLExpression, context: DSLContext) -> Any:
        """Execute function call expression."""
        function_name = expression.value
        args = await self._evaluate_args(expression, context)

        handled, result = await self._resolve_schema_call(function_name, args, context)
        if handled:
            return result
        if function_name in self.built_in_functions:
            return await self._call_function(self.built_in_functions[function_name], args, context)
        if function_name in context.functions:
            return await self._call_function(context.functions[function_name], args, context)
        raise ValueError(f"Unknown function: {function_name}")
    
    async def _execute_property_access(self, expression: DSLExpression, context: DSLExpression) -> Any:
        """Execute property access expression."""
        object_name = expression.value
        property_name = expression.children[0].value
        
        # Get the object
        obj = context.get_variable(object_name)
        if obj is None:
            raise ValueError(f"Unknown object: {object_name}")
        
        # Access property
        if hasattr(obj, property_name):
            return getattr(obj, property_name)
        elif isinstance(obj, dict) and property_name in obj:
            return obj[property_name]
        else:
            raise ValueError(f"Object {object_name} has no property {property_name}")
    
    async def _execute_comparison(self, expression: DSLExpression, context: DSLContext) -> bool:
        """Execute comparison expression."""
        if len(expression.children) != 2:
            raise ValueError("Comparison requires exactly 2 children")
        left = await self._execute_expression(expression.children[0], context)
        right = await self._execute_expression(expression.children[1], context)
        operator = expression.value
        if operator == "matches":
            import re
            return bool(re.search(str(right), str(left)))
        op_fn = _COMPARISON_OPS.get(operator)
        if op_fn is None:
            raise ValueError(f"Unknown comparison operator: {operator}")
        return op_fn(left, right)
    
    async def _execute_not_logical(self, expression: DSLExpression, context: DSLContext) -> bool:
        if len(expression.children) != 1:
            raise ValueError("not requires exactly 1 operand")
        operand = await self._execute_expression(expression.children[0], context)
        return not operand

    async def _execute_and_or_logical(self, operator: str, expression: DSLExpression, context: DSLContext) -> bool:
        if len(expression.children) != 2:
            raise ValueError(f"{operator} requires exactly 2 operands")
        left = await self._execute_expression(expression.children[0], context)
        right = await self._execute_expression(expression.children[1], context)
        if operator == "and":
            return left and right
        return left or right

    async def _execute_logical(self, expression: DSLExpression, context: DSLContext) -> bool:
        """Execute logical expression."""
        operator = expression.value
        if operator == "not":
            return await self._execute_not_logical(expression, context)
        elif operator in ["and", "or"]:
            return await self._execute_and_or_logical(operator, expression, context)
        else:
            raise ValueError(f"Unknown logical operator: {operator}")
    
    async def _execute_arithmetic(self, expression: DSLExpression, context: DSLContext) -> Union[int, float]:
        """Execute arithmetic expression."""
        operator = expression.value
        if operator == "-" and len(expression.children) == 1:
            operand = await self._execute_expression(expression.children[0], context)
            return -operand
        if len(expression.children) != 2:
            raise ValueError(f"Arithmetic operator {operator} requires 1 or 2 operands")
        left = await self._execute_expression(expression.children[0], context)
        right = await self._execute_expression(expression.children[1], context)
        op_fn = _ARITHMETIC_OPS.get(operator)
        if op_fn is None:
            raise ValueError(f"Unknown arithmetic operator: {operator}")
        return op_fn(left, right)
    
    async def _execute_pipeline_stage(self, child: DSLExpression, previous_result: Any, context: DSLContext) -> Any:
        """Execute a single pipeline stage given the previous result."""
        if child.type == DSLExpressionType.IDENTIFIER:
            func_name = child.value
            if func_name in self.built_in_functions:
                return await self._call_function(self.built_in_functions[func_name], [previous_result], context)
            if func_name in context.functions:
                return await self._call_function(context.functions[func_name], [previous_result], context)
            return func_name
        return await self._execute_expression(child, context)

    async def _execute_pipeline(self, expression: DSLExpression, context: DSLContext) -> Any:
        """Execute pipeline expression."""
        result = None
        for i, child in enumerate(expression.children):
            if i == 0:
                result = await self._execute_expression(child, context)
            else:
                result = await self._execute_pipeline_stage(child, result, context)
            context.set_variable("_", result)
        
        return result
    
    async def _execute_list(self, expression: DSLExpression, context: DSLContext) -> List[Any]:
        """Execute list expression."""
        items = []
        
        for item_expr in expression.children:
            item = await self._execute_expression(item_expr, context)
            items.append(item)
        
        return items
    
    async def _execute_dict(self, expression: DSLExpression, context: DSLContext) -> Dict[str, Any]:
        """Execute dictionary expression."""
        result = {}
        
        for key_expr, value_expr in expression.metadata.get("items", []):
            key = await self._execute_expression(key_expr, context)
            value = await self._execute_expression(value_expr, context)
            result[str(key)] = value
        
        return result
    
    async def _execute_block(self, expression: DSLExpression, context: DSLContext) -> Any:
        """Execute block expression."""
        result = None
        
        for child in expression.children:
            result = await self._execute_expression(child, context)
        
        return result
    
    async def _execute_sumd_command(self, command_name: str, args: List[Any], context: DSLContext) -> Any:
        """Execute SUMD command via command bus."""
        if not self.command_bus:
            raise ValueError("Command bus not configured")
        
        from ..cqrs.commands import (
            CreateSumdDocument,
            UpdateSumdDocument,
            AddSumdSection,
            RemoveSumdSection,
            ValidateSumdDocument,
            ScanProject,
            GenerateMap,
        )
        
        # Map command names to command classes
        command_map = {
            "create": CreateSumdDocument,
            "update": UpdateSumdDocument,
            "add_section": AddSumdSection,
            "remove_section": RemoveSumdSection,
            "validate": ValidateSumdDocument,
            "scan": ScanProject,
            "map": GenerateMap,
        }
        
        command_class = command_map.get(command_name)
        if not command_class:
            raise ValueError(f"Unknown SUMD command: {command_name}")
        
        # Create command
        if args:
            data = args[0] if isinstance(args[0], dict) else {}
        else:
            data = {}
        
        command = command_class(
            aggregate_id=context.working_directory.name,
            data=data,
        )
        
        # Execute command
        events = await self.command_bus.dispatch(command)
        
        return {
            "command": command_name,
            "events": len(events),
            "success": True,
        }
    
    async def _call_function(self, func: Callable, args: List[Any], context: DSLContext) -> Any:
        """Call a function with arguments."""
        if asyncio.iscoroutinefunction(func):
            return await func(context, args)
        else:
            return func(context, args)
    
    def _initialize_builtin_functions(self) -> Dict[str, Callable]:
        """Initialize built-in functions."""
        return {
            "print": self._builtin_print,
            "len": self._builtin_len,
            "str": self._builtin_str,
            "int": self._builtin_int,
            "float": self._builtin_float,
            "bool": self._builtin_bool,
            "type": self._builtin_type,
            "write_file": self._builtin_write_file,
            "list_files": self._builtin_list_files,
            "cwd": self._builtin_cwd,
            "cd": self._builtin_cd,
            "help": self._builtin_help,
        }
    
    # Built-in function implementations
    async def _builtin_print(self, context: DSLContext, args: List[Any]) -> None:
        """Print arguments to console."""
        print(*args)
    
    def _builtin_len(self, context: DSLContext, args: List[Any]) -> int:
        """Get length of object."""
        if not args:
            raise ValueError("len() requires an argument")
        return len(args[0])
    
    def _builtin_str(self, context: DSLContext, args: List[Any]) -> str:
        """Convert object to string."""
        if not args:
            # Use the last result from context (pipeline variable)
            obj = context.variables.get('_', '')
        else:
            obj = args[0]
        return str(obj)
    
    def _builtin_int(self, context: DSLContext, args: List[Any]) -> int:
        """Convert object to int."""
        if not args:
            raise ValueError("int() requires an argument")
        return int(args[0])
    
    def _builtin_float(self, context: DSLContext, args: List[Any]) -> float:
        """Convert object to float."""
        if not args:
            raise ValueError("float() requires an argument")
        return float(args[0])
    
    def _builtin_bool(self, context: DSLContext, args: List[Any]) -> bool:
        """Convert object to bool."""
        if not args:
            raise ValueError("bool() requires an argument")
        return bool(args[0])
    
    def _builtin_type(self, context: DSLContext, args: List[Any]) -> str:
        """Get type of object."""
        if not args:
            raise ValueError("type() requires an argument")
        return type(args[0]).__name__
    
    async def _builtin_write_file(self, context: DSLContext, path: str, content: str) -> None:
        """Write content to file."""
        full_path = context.working_directory / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
    
    def _builtin_list_files(self, context: DSLContext, pattern: str = "*") -> List[str]:
        """List files matching pattern."""
        return [str(p.relative_to(context.working_directory)) 
                for p in context.working_directory.glob(pattern) 
                if p.is_file()]
    
    def _builtin_cwd(self, context: DSLContext) -> str:
        """Get current working directory."""
        return str(context.working_directory)
    
    def _builtin_cd(self, context: DSLContext, path: str) -> None:
        """Change working directory."""
        new_path = context.working_directory / path
        if new_path.is_dir():
            context.working_directory = new_path.resolve()
        else:
            raise ValueError(f"Directory not found: {path}")
    
    def _builtin_help(self, context: DSLContext) -> str:
        """Show help information."""
        help_text = """
SUMD DSL Built-in Functions:
  print(args...)           - Print arguments to console
  len(obj)                - Get length of object
  str(obj)                - Convert to string
  int(obj)                - Convert to integer
  float(obj)              - Convert to float
  bool(obj)               - Convert to boolean
  type(obj)               - Get type name
  exists(path)            - Check if file/directory exists
  read_file(path)         - Read file contents
  write_file(path, content) - Write content to file
  list_files(pattern)     - List files matching pattern
  cwd()                   - Get current working directory
  cd(path)                - Change working directory
  help()                  - Show this help

SUMD Commands:
  scan(path)              - Scan project and generate SUMD
  map(path)               - Generate project map
  validate(path)          - Validate SUMD document
  create(data)            - Create SUMD document
  update(data)            - Update SUMD document
  add_section(data)       - Add section to document
  remove_section(name)    - Remove section from document

DSL Examples:
  scan(".") | validate(".")
  files = list_files("*.md")
  if exists("SUMD.md"): print("SUMD found")
        """
        return help_text.strip()
