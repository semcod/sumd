"""DSL Shell for interactive SUMD DSL execution."""

from __future__ import annotations

import asyncio
import readline
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from .engine import DSLEngine, DSLContext
from .parser import parse_dsl
from .commands import DSLCommandRegistry, create_builtin_registry


class DSLShell:
    """Interactive shell for SUMD DSL."""
    
    def __init__(
        self,
        engine: Optional[DSLEngine] = None,
        command_registry: Optional[DSLCommandRegistry] = None,
        working_directory: Optional[Path] = None,
    ):
        self.engine = engine or DSLEngine()
        self.command_registry = command_registry or create_builtin_registry()
        self.working_directory = working_directory or Path.cwd()
        self.context = DSLContext(self.working_directory)
        self.history: List[str] = []
        self.running = True
        
        # Setup readline for better input handling
        self._setup_readline()
        
        # Register command functions in context
        self._register_commands()
    
    def _setup_readline(self) -> None:
        """Setup readline for command history and completion."""
        try:
            # Load history
            history_file = Path.home() / ".sumd_dsl_history"
            if history_file.exists():
                readline.read_history_file(history_file)
            
            # Set history length
            readline.set_history_length(1000)
            
            # Setup tab completion
            readline.set_completer(self._completer)
            readline.parse_and_bind("tab: complete")
            
            self.history_file = history_file
        except Exception:
            # Readline not available (Windows, etc.)
            self.history_file = None
    
    def _get_command_completions(self, text: str) -> List[str]:
        options = []
        for command in self.command_registry.list_commands():
            if command.name.startswith(text):
                options.append(command.name)
            for alias in command.aliases:
                if alias.startswith(text):
                    options.append(alias)
        return options

    def _get_completion_options(self, text: str) -> List[str]:
        """Generate completion options based on current text."""
        options = self._get_command_completions(text)
        for var_name in self.context.variables.keys():
            if var_name.startswith(text):
                options.append(var_name)
        for func_name in self.engine.built_in_functions.keys():
            if func_name.startswith(text):
                options.append(func_name)
        return options

    def _completer(self, text: str, state: int) -> Optional[str]:
        """Tab completion for DSL commands."""
        options = self._get_completion_options(text)
        if state < len(options):
            return options[state]
        return None
    
    def _register_commands(self) -> None:
        """Register command functions in the DSL context."""
        for command in self.command_registry.list_commands():
            self.context.register_function(command.name, command.function)
            for alias in command.aliases:
                self.context.register_function(alias, command.function)
    
    async def _process_one_input(self) -> bool:
        """Process a single shell input line. Returns False if EOF."""
        try:
            prompt = self._get_prompt()
            line = input(prompt).strip()
            if not line:
                return True
            if line.startswith("!"):
                await self._handle_shell_command(line[1:])
                return True
            await self._execute_line(line)
            return True
        except KeyboardInterrupt:
            print("^C")
            return True
        except EOFError:
            print()
            return False
        except Exception as e:
            print(f"Error: {e}")
            return True

    async def run(self) -> None:
        """Run the interactive shell."""
        print(f"SUMD DSL Shell v1.0")
        print(f"Working directory: {self.working_directory}")
        print(f"Type 'help' for available commands or 'exit' to quit.")
        print()
        
        try:
            while self.running:
                if not await self._process_one_input():
                    break
        
        finally:
            # Save history
            if self.history_file:
                try:
                    readline.write_history_file(self.history_file)
                except Exception:
                    pass
            
            print("Goodbye!")
    
    def _get_prompt(self) -> str:
        """Get the current prompt."""
        return f"sumd:{self.working_directory.name}> "
    
    def _handle_cd_command(self, path: str) -> None:
        """Handle shell cd command."""
        try:
            new_path = self.working_directory / path
            if new_path.is_dir():
                self.working_directory = new_path.resolve()
                self.context.working_directory = self.working_directory
                print(f"Changed to: {self.working_directory}")
            else:
                print(f"Directory not found: {path}")
        except Exception as e:
            print(f"Error: {e}")

    def _handle_vars_command(self) -> None:
        if self.context.variables:
            print("Variables:")
            for name, value in self.context.variables.items():
                print(f"  {name} = {value}")
        else:
            print("No variables set.")

    def _handle_history_command(self) -> None:
        for i, line in enumerate(self.history[-10:], 1):
            print(f"  {i}: {line}")

    def _dispatch_exact_shell_cmd(self, command: str) -> bool:
        if command in ["exit", "quit"]:
            self.running = False
            return True
        if command == "clear":
            import os
            os.system("clear" if os.name != "nt" else "cls")
            return True
        if command == "help":
            print("Shell Commands:\n  !exit, !quit  - Exit the shell\n  !clear        - Clear the screen\n  !help         - Show this help\n\nUse 'help' for DSL commands.")
            return True
        if command == "pwd":
            print(self.working_directory)
            return True
        if command == "vars":
            self._handle_vars_command()
            return True
        if command == "history":
            self._handle_history_command()
            return True
        return False

    async def _handle_shell_command(self, command: str) -> None:
        """Handle shell commands (prefixed with !)."""
        command = command.strip()
        if self._dispatch_exact_shell_cmd(command):
            return
        if command.startswith("cd "):
            self._handle_cd_command(command[3:].strip())
        else:
            print(f"Unknown shell command: {command}\nType !help for available shell commands.")
    
    def _print_dsl_list(self, result: list) -> None:
        if result:
            for item in result:
                print(f"  {item}")
        else:
            print("  (empty list)")

    def _print_dsl_dict(self, result: dict) -> None:
        if result:
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("  (empty dict)")

    def _print_dsl_result(self, result: Any) -> None:
        """Pretty-print DSL result."""
        if result is None:
            return
        if isinstance(result, list):
            self._print_dsl_list(result)
        elif isinstance(result, dict):
            self._print_dsl_dict(result)
        else:
            print(f"  {result}")

    async def _execute_line(self, line: str) -> None:
        """Execute a DSL line."""
        self.history.append(line)
        try:
            expression = parse_dsl(line)
            result = await self.engine.execute(expression, self.context)
            self._print_dsl_result(result)
        
        except Exception as e:
            print(f"Error: {e}")
    
    async def _execute_script_line(self, line: str, line_num: int) -> bool:
        """Execute a single script line. Return False to abort script."""
        line = line.strip()
        if not line or line.startswith("#"):
            return True
        print(f"{line_num}: {line}")
        try:
            expression = parse_dsl(line)
            result = await self.engine.execute(expression, self.context)
            if result is not None:
                if isinstance(result, (list, dict)):
                    print(f"  Result: {len(result)} items")
                else:
                    print(f"  Result: {result}")
            return True
        except Exception as e:
            print(f"  Error on line {line_num}: {e}")
            return False

    async def execute_script(self, script_path: Path) -> None:
        """Execute a DSL script file."""
        if not script_path.exists():
            raise ValueError(f"Script not found: {script_path}")
        print(f"Executing script: {script_path}")
        try:
            content = script_path.read_text(encoding="utf-8")
            for line_num, line in enumerate(content.splitlines(), 1):
                if not await self._execute_script_line(line, line_num):
                    break
        
        except Exception as e:
            print(f"Error reading script: {e}")
    
    async def execute_command(self, command: str) -> Any:
        """Execute a single DSL command."""
        try:
            expression = parse_dsl(command)
            return await self.engine.execute(expression, self.context)
        except Exception as e:
            raise ValueError(f"Command execution failed: {e}")


class DSLShellServer:
    """Server for DSL shell operations (for MCP integration)."""
    
    def __init__(self, working_directory: Optional[Path] = None):
        self.working_directory = working_directory or Path.cwd()
        self.shell = DSLShell(working_directory=self.working_directory)
    
    async def execute_dsl(self, dsl_expression: str, context_vars: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute DSL expression and return result."""
        try:
            # Set context variables
            if context_vars:
                for name, value in context_vars.items():
                    self.shell.context.set_variable(name, value)
            
            # Parse and execute
            expression = parse_dsl(dsl_expression)
            result = await self.shell.engine.execute(expression, self.shell.context)
            
            return {
                "success": True,
                "result": result,
                "working_directory": str(self.shell.working_directory),
                "variables": self.shell.context.variables,
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "working_directory": str(self.shell.working_directory),
                "variables": self.shell.context.variables,
            }
    
    async def get_shell_info(self) -> Dict[str, Any]:
        """Get shell information."""
        return {
            "working_directory": str(self.shell.working_directory),
            "variables": self.shell.context.variables,
            "available_commands": [
                {
                    "name": cmd.name,
                    "description": cmd.description,
                    "usage": cmd.usage,
                    "aliases": cmd.aliases,
                    "category": cmd.category,
                }
                for cmd in self.shell.command_registry.list_commands()
            ],
            "available_functions": list(self.shell.engine.built_in_functions.keys()),
        }


# CLI entry point
def _should_run_interactive(args) -> bool:
    if args.interactive:
        return True
    if args.command or args.script:
        return False
    return True

async def _main_run_logic(shell: DSLShell, args) -> None:
    if args.command:
        result = await shell.execute_command(args.command)
        if result is not None:
            print(result)
    elif args.script:
        await shell.execute_script(Path(args.script))
    if _should_run_interactive(args):
        await shell.run()

async def main() -> None:
    """Main entry point for DSL shell."""
    import argparse
    parser = argparse.ArgumentParser(description="SUMD DSL Shell")
    parser.add_argument("script", nargs="?", help="DSL script to execute")
    parser.add_argument("--directory", "-d", help="Working directory")
    parser.add_argument("--command", "-c", help="Execute single command")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run interactively after script")
    
    args = parser.parse_args()
    working_directory = Path(args.directory) if args.directory else Path.cwd()
    if not working_directory.exists():
        print(f"Error: Directory not found: {working_directory}")
        sys.exit(1)
    
    shell = DSLShell(working_directory=working_directory)
    try:
        await _main_run_logic(shell, args)
    
    except KeyboardInterrupt:
        print()
        print("Interrupted.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
