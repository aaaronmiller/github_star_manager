"""Script generation module for creating update scripts."""

from typing import List, Dict
from datetime import datetime


class ScriptGenerator:
    """Generates shell scripts for safe repository updates."""

    def generate_script(self, repos: List[Dict]) -> str:
        """
        Generate a shell script for updating repositories.

        Args:
            repos: List of repository dictionaries with 'path' and 'name'

        Returns:
            Shell script content as string
        """
        script_lines = [
            "#!/bin/bash",
            "# Agentic Update Assistant - Safe Update Script",
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "#",
            "# This script updates repositories categorized as 'safe to update'",
            "# Review this script before executing!",
            "",
            "set -e  # Exit on error",
            "",
            "echo '================================'",
            "echo 'Agentic Update Assistant'",
            "echo 'Safe Repository Updates'",
            "echo '================================'",
            "",
        ]

        for i, repo in enumerate(repos, 1):
            script_lines.extend([
                f"# {i}. {repo['name']}",
                f"echo ''",
                f"echo 'Updating {repo['name']}...'",
                f"cd '{repo['path']}'",
                "git pull",
                "",
            ])

        script_lines.extend([
            "echo ''",
            "echo '================================'",
            "echo 'All updates completed!'",
            "echo '================================'",
        ])

        return '\n'.join(script_lines)
