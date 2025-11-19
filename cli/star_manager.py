#!/usr/bin/env python3
"""
GitHub Star Manager CLI Tool

Scans directories for Git repositories and generates a repos.json file.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from git import InvalidGitRepositoryError, Repo
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


def get_repo_info(path: Path, verbose: bool = False) -> dict[str, Any] | None:
    """
    Extract information from a Git repository.

    Args:
        path: Path to the repository
        verbose: Enable verbose output

    Returns:
        Dictionary with repository information or None if not a valid repo
    """
    try:
        repo = Repo(path)

        if verbose:
            console.print(f"[cyan]Processing:[/cyan] {path}")

        remote_url = None
        if repo.remotes:
            try:
                remote_url = repo.remotes.origin.url
                if remote_url.endswith('.git'):
                    remote_url = remote_url[:-4]
                if remote_url.startswith('git@github.com:'):
                    remote_url = remote_url.replace('git@github.com:', 'https://github.com/')
            except AttributeError:
                pass

        if not remote_url:
            if verbose:
                console.print(f"[yellow]  Skipping (no remote URL)[/yellow]")
            return None

        latest_commit = repo.head.commit
        last_updated = latest_commit.committed_datetime.isoformat()

        repo_name = path.name

        return {
            'name': repo_name,
            'url': remote_url,
            'description': '',
            'lastUpdated': last_updated,
        }
    except InvalidGitRepositoryError:
        if verbose:
            console.print(f"[red]  Not a git repository[/red]")
        return None
    except Exception as e:
        if verbose:
            console.print(f"[red]  Error: {e}[/red]")
        return None


def find_git_repos(root_path: Path, max_depth: int = 3, verbose: bool = False) -> list[Path]:
    """
    Find all Git repositories in a directory tree.

    Args:
        root_path: Root directory to start scanning
        max_depth: Maximum depth to search
        verbose: Enable verbose output

    Returns:
        List of paths to Git repositories
    """
    repos: list[Path] = []

    def scan_directory(path: Path, depth: int) -> None:
        if depth > max_depth:
            return

        try:
            if (path / '.git').exists() and (path / '.git').is_dir():
                repos.append(path)
                return

            if not path.is_dir():
                return

            for item in path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    scan_directory(item, depth + 1)
        except PermissionError:
            if verbose:
                console.print(f"[yellow]Permission denied:[/yellow] {path}")
        except Exception as e:
            if verbose:
                console.print(f"[red]Error scanning {path}:[/red] {e}")

    scan_directory(root_path, 0)
    return repos


def main() -> None:
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(
        description='GitHub Star Manager - Scan directories for Git repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ~/projects
  %(prog)s ~/projects -o custom.json
  %(prog)s ~/projects --depth 5 --verbose
        """,
    )

    parser.add_argument(
        'path', type=str, help='Path to scan for repositories'
    )

    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default='repos.json',
        help='Output JSON file (default: repos.json)',
    )

    parser.add_argument(
        '-d',
        '--depth',
        type=int,
        default=3,
        help='Maximum depth to search (default: 3)',
    )

    parser.add_argument(
        '-v', '--verbose', action='store_true', help='Enable verbose output'
    )

    args = parser.parse_args()

    scan_path = Path(args.path).expanduser().resolve()

    if not scan_path.exists():
        console.print(f"[red]Error:[/red] Path does not exist: {scan_path}")
        sys.exit(1)

    if not scan_path.is_dir():
        console.print(f"[red]Error:[/red] Path is not a directory: {scan_path}")
        sys.exit(1)

    console.print(f"\n[bold cyan]GitHub Star Manager[/bold cyan]")
    console.print(f"Scanning: {scan_path}\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Finding repositories...", total=None)

        repo_paths = find_git_repos(scan_path, args.depth, args.verbose)
        progress.update(task, completed=True)

    console.print(f"\n[green]Found {len(repo_paths)} repositories[/green]\n")

    if not repo_paths:
        console.print("[yellow]No repositories found. Exiting.[/yellow]")
        sys.exit(0)

    repositories = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing repositories...", total=len(repo_paths))

        for repo_path in repo_paths:
            repo_info = get_repo_info(repo_path, args.verbose)
            if repo_info:
                repositories.append(repo_info)
            progress.advance(task)

    repos_data = {
        'repositories': repositories,
        'metadata': {
            'totalCount': len(repositories),
            'lastScanned': datetime.now().isoformat(),
        },
    }

    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(repos_data, f, indent=2, ensure_ascii=False)

    console.print(f"\n[bold green]Success![/bold green]")
    console.print(f"Saved {len(repositories)} repositories to: {output_path.absolute()}\n")

    if repositories:
        table = Table(title="Repository Summary")
        table.add_column("Name", style="cyan")
        table.add_column("URL", style="blue")
        table.add_column("Last Updated", style="green")

        for repo in repositories[:10]:
            last_updated = (
                datetime.fromisoformat(repo['lastUpdated']).strftime('%Y-%m-%d')
                if repo.get('lastUpdated')
                else 'Unknown'
            )
            table.add_row(repo['name'], repo['url'], last_updated)

        if len(repositories) > 10:
            table.add_row("...", f"and {len(repositories) - 10} more", "...")

        console.print(table)


if __name__ == '__main__':
    main()
