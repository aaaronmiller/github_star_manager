#!/usr/bin/env python3
"""
Agentic Update Assistant - AI-powered local repository update manager
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

from scanner import RepositoryScanner
from analyzer import UpdateAnalyzer
from script_generator import ScriptGenerator

console = Console()


def load_config() -> Dict:
    """Load configuration from user config file."""
    config_path = Path.home() / '.config' / 'repo-updater' / 'config.json'

    if not config_path.exists():
        console.print(
            "[red]Configuration file not found![/red]\n"
            f"Please create {config_path} with:\n"
            "{\n"
            '  "repo_root_dir": "/path/to/your/projects",\n'
            '  "github_token": "your_github_token",\n'
            '  "gemini_api_key": "your_gemini_api_key"\n'
            "}"
        )
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    required_keys = ['repo_root_dir', 'github_token', 'gemini_api_key']
    missing = [key for key in required_keys if key not in config]

    if missing:
        console.print(f"[red]Missing configuration keys: {', '.join(missing)}[/red]")
        sys.exit(1)

    return config


@click.command()
@click.option('--dry-run', is_flag=True, help='Run without generating update script')
def main(dry_run: bool):
    """Scan local repositories and analyze available updates."""

    console.print(Panel.fit(
        "[bold blue]Agentic Update Assistant[/bold blue]\n"
        "AI-powered local repository update manager",
        border_style="blue"
    ))

    # Load configuration
    config = load_config()
    repo_root = Path(config['repo_root_dir'])

    if not repo_root.exists():
        console.print(f"[red]Repository root directory not found: {repo_root}[/red]")
        sys.exit(1)

    # Initialize components
    scanner = RepositoryScanner(repo_root)
    analyzer = UpdateAnalyzer(config['github_token'], config['gemini_api_key'])
    script_gen = ScriptGenerator()

    # Scan for repositories
    console.print(f"\n[bold]Scanning {repo_root} for Git repositories...[/bold]")

    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=None)
        repos = scanner.find_repositories()
        progress.update(task, completed=1, total=1)

    console.print(f"[green]Found {len(repos)} repositories[/green]\n")

    if not repos:
        console.print("[yellow]No Git repositories found in the specified directory.[/yellow]")
        return

    # Analyze each repository
    results = {
        'up_to_date': [],
        'safe_to_update': [],
        'needs_review': []
    }

    console.print("[bold]Analyzing repositories for updates...[/bold]\n")

    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing...", total=len(repos))

        for repo_path in repos:
            repo_name = repo_path.name

            try:
                analysis = analyzer.analyze_repository(repo_path)

                if analysis['status'] == 'up_to_date':
                    results['up_to_date'].append({
                        'name': repo_name,
                        'path': str(repo_path)
                    })
                elif analysis['status'] == 'safe_to_update':
                    results['safe_to_update'].append({
                        'name': repo_name,
                        'path': str(repo_path),
                        'summary': analysis['summary'],
                        'commits_behind': analysis['commits_behind']
                    })
                else:  # needs_review
                    results['needs_review'].append({
                        'name': repo_name,
                        'path': str(repo_path),
                        'summary': analysis['summary'],
                        'commits_behind': analysis['commits_behind'],
                        'risk_level': analysis.get('risk_level', 'high')
                    })

            except Exception as e:
                console.print(f"[red]Error analyzing {repo_name}: {e}[/red]")

            progress.advance(task)

    # Display results
    console.print("\n[bold]Analysis Results:[/bold]\n")

    # Up-to-date repositories
    if results['up_to_date']:
        table = Table(title="✓ Up-to-Date Repositories", style="green")
        table.add_column("Repository", style="cyan")
        table.add_column("Path", style="dim")

        for repo in results['up_to_date']:
            table.add_row(repo['name'], repo['path'])

        console.print(table)
        console.print()

    # Safe to update
    if results['safe_to_update']:
        table = Table(title="⚡ Safe to Update", style="yellow")
        table.add_column("Repository", style="cyan")
        table.add_column("Commits Behind", justify="center")
        table.add_column("Summary", style="dim")

        for repo in results['safe_to_update']:
            table.add_row(
                repo['name'],
                str(repo['commits_behind']),
                repo['summary'][:60] + "..." if len(repo['summary']) > 60 else repo['summary']
            )

        console.print(table)
        console.print()

    # Needs review
    if results['needs_review']:
        table = Table(title="⚠ Needs Review", style="red")
        table.add_column("Repository", style="cyan")
        table.add_column("Risk", justify="center")
        table.add_column("Commits Behind", justify="center")
        table.add_column("Summary", style="dim")

        for repo in results['needs_review']:
            table.add_row(
                repo['name'],
                repo['risk_level'].upper(),
                str(repo['commits_behind']),
                repo['summary'][:50] + "..." if len(repo['summary']) > 50 else repo['summary']
            )

        console.print(table)
        console.print()

    # Generate update script for safe updates
    if results['safe_to_update'] and not dry_run:
        script_content = script_gen.generate_script(results['safe_to_update'])
        script_path = Path('update_script.sh')

        with open(script_path, 'w') as f:
            f.write(script_content)

        os.chmod(script_path, 0o755)

        console.print(
            f"[green]✓ Generated update script: {script_path}[/green]\n"
            "[yellow]Review the script before executing:[/yellow]\n"
            f"  cat {script_path}\n"
            f"  ./{script_path}"
        )

    # Summary
    console.print(Panel.fit(
        f"[bold]Summary[/bold]\n"
        f"Up-to-date: [green]{len(results['up_to_date'])}[/green] | "
        f"Safe to update: [yellow]{len(results['safe_to_update'])}[/yellow] | "
        f"Needs review: [red]{len(results['needs_review'])}[/red]",
        border_style="blue"
    ))


if __name__ == '__main__':
    main()
