# Python CLI Skill

## Overview
Best practices and patterns for building command-line tools with Python.

## Core Patterns

### 1. Argparse CLI Structure
```python
import argparse
from typing import Optional

def main() -> None:
    parser = argparse.ArgumentParser(
        description='GitHub Star Manager CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'path',
        type=str,
        help='Path to scan for repositories'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='repos.json',
        help='Output JSON file (default: repos.json)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()
    process(args.path, args.output, args.verbose)

if __name__ == '__main__':
    main()
```

### 2. GitPython Repository Operations
```python
from git import Repo, InvalidGitRepositoryError
from pathlib import Path

def get_repo_info(path: Path) -> dict:
    try:
        repo = Repo(path)

        # Get remote URL
        remote_url = None
        if repo.remotes:
            remote_url = repo.remotes.origin.url

        # Get branch info
        branch = repo.active_branch.name if not repo.head.is_detached else None

        # Get latest commit
        latest_commit = repo.head.commit

        return {
            'path': str(path),
            'name': path.name,
            'remote_url': remote_url,
            'branch': branch,
            'last_commit': {
                'hash': latest_commit.hexsha[:7],
                'message': latest_commit.message.strip(),
                'author': latest_commit.author.name,
                'date': latest_commit.committed_datetime.isoformat()
            }
        }
    except InvalidGitRepositoryError:
        return None
```

### 3. Rich Terminal Output
```python
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

# Print styled text
console.print("[bold green]Success![/bold green]")
console.print("[red]Error occurred[/red]")

# Create tables
table = Table(title="Repositories")
table.add_column("Name", style="cyan")
table.add_column("Branch", style="magenta")
table.add_column("Status", style="green")

table.add_row("my-repo", "main", "Clean")
console.print(table)

# Progress bars
for item in track(items, description="Processing..."):
    process_item(item)
```

### 4. JSON Data Handling
```python
import json
from pathlib import Path
from typing import Any

def save_json(data: Any, filepath: Path) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filepath: Path) -> Any:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### 5. Error Handling
```python
import sys
from rich.console import Console

console = Console()

def safe_operation() -> None:
    try:
        # Perform operation
        result = risky_operation()
    except FileNotFoundError as e:
        console.print(f"[red]Error: File not found - {e}[/red]")
        sys.exit(1)
    except PermissionError as e:
        console.print(f"[red]Error: Permission denied - {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)
```

### 6. File System Operations
```python
from pathlib import Path
from typing import List

def find_git_repos(root_path: Path, max_depth: int = 3) -> List[Path]:
    repos = []

    def scan_directory(path: Path, depth: int) -> None:
        if depth > max_depth:
            return

        try:
            if (path / '.git').exists():
                repos.append(path)
                return  # Don't scan subdirectories of a git repo

            for item in path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    scan_directory(item, depth + 1)
        except PermissionError:
            pass  # Skip directories we can't access

    scan_directory(root_path, 0)
    return repos
```

### 7. Type Hints
```python
from typing import List, Dict, Optional, Any
from pathlib import Path

def process_repos(
    paths: List[Path],
    output_file: str,
    verbose: bool = False
) -> Dict[str, Any]:
    results: Dict[str, Any] = {}

    for path in paths:
        info: Optional[Dict[str, Any]] = get_repo_info(path)
        if info:
            results[info['name']] = info

    return results
```

## Best Practices
- Use argparse for CLI argument parsing
- Leverage GitPython for Git operations
- Use Rich for beautiful terminal output
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Handle errors gracefully
- Use pathlib.Path for file operations
- Provide verbose/quiet modes
- Write docstrings for public functions
- Use virtual environments
