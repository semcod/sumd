import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path
from .engine import HybridPrologEngine, PYSWIP_AVAILABLE

console = Console()

def get_engine() -> HybridPrologEngine:
    # Try finding the logic rules path
    # Look next to package or root
    pkg_dir = Path(__file__).resolve().parent
    rules_path = pkg_dir.parent / "logic" / "rules.pl"
    if not rules_path.exists():
        # Fallback to current folder or nested pkg logic
        rules_path = pkg_dir / "logic" / "rules.pl"
        if not rules_path.exists():
            rules_path = Path("./logic/rules.pl")
            
    if not rules_path.exists():
        # Create a dummy rules.pl if not found
        rules_path.parent.mkdir(parents=True, exist_ok=True)
        rules_path.write_text("parent(john, mary).\n", encoding="utf-8")
        
    return HybridPrologEngine(rules_path)

@click.group()
def main():
    """🧠 Hybrid Python-Prolog logic runner CLI."""
    pass

@main.command()
def info():
    """Display information about the available Prolog backends."""
    console.print(Panel.fit(
        "[bold green]🧠 Hybrid Python-Prolog Logic Engine[/bold green]\n"
        "Supported Backends:\n"
        f"  - [cyan]PySwip (Direct Bindings):[/cyan] {'✅ Available' if PYSWIP_AVAILABLE else '❌ Not Available'}\n"
        "  - [cyan]SWI-Prolog CLI Subprocess:[/cyan] Ready (fallback)\n"
        "  - [cyan]Pure Python Resolution Engine:[/cyan] ✅ Active (fallback)",
        title="Engine Status"
    ))

@main.command()
@click.argument("query_str")
def query(query_str: str):
    """Query the logic rules.

    Example:
      query "ancestor(john, mary)"
      query "sibling(mary, X)"
    """
    engine = get_engine()
    
    console.print(f"[bold yellow]🔍 Running Query:[/bold yellow] {query_str}")
    results = engine.query(query_str)
    
    if not results:
        console.print("[bold red]❌ No solutions found (or evaluates to False).[/bold red]")
        return
        
    if results == [{}]:
        console.print("[bold green]✅ True.[/bold green]")
        return
        
    # Build results table
    table = Table(title="Query Solutions")
    keys = list(results[0].keys())
    for k in keys:
        table.add_column(k, style="cyan")
        
    for r in results:
        table.add_row(*[str(r[k]) for k in keys])
        
    console.print(table)

@main.command()
def shell():
    """Start interactive logic query shell."""
    engine = get_engine()
    
    console.print(Panel(
        "[bold green]Interactive Logic Shell Started.[/bold green]\n"
        "Type your Prolog queries here, or [bold red]quit[/bold red] / [bold red]exit[/bold red] to stop.\n"
        "Example: parent(john, X) or ancestor(john, mary)",
        title="Prolog Interactive Shell"
    ))
    
    while True:
        try:
            q = input("prolog-py> ").strip()
            if q.lower() in ("quit", "exit"):
                break
            if not q:
                continue
            
            results = engine.query(q)
            if not results:
                console.print("[red]False.[/red]")
            elif results == [{}]:
                console.print("[green]True.[/green]")
            else:
                for idx, r in enumerate(results):
                    kv_pairs = ", ".join(f"{k} = {v}" for k, v in r.items())
                    console.print(f"[{idx+1}] [cyan]{kv_pairs}[/cyan]")
        except (KeyboardInterrupt, EOFError):
            console.print("\nBye!")
            break
        except Exception as e:
            console.print(f"[bold red]Error parsing/querying:[/bold red] {e}")

if __name__ == "__main__":
    main()
