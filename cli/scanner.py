"""Repository scanner module for finding local Git repositories."""

from pathlib import Path
from typing import List
import git


class RepositoryScanner:
    """Scans a directory tree for Git repositories."""

    def __init__(self, root_dir: Path):
        """
        Initialize scanner with root directory.

        Args:
            root_dir: Root directory to scan for repositories
        """
        self.root_dir = root_dir

    def find_repositories(self) -> List[Path]:
        """
        Recursively find all Git repositories under root directory.

        Returns:
            List of paths to Git repository directories
        """
        repos = []

        for item in self.root_dir.rglob('.git'):
            if item.is_dir():
                repo_path = item.parent
                try:
                    # Verify it's a valid Git repository
                    git.Repo(repo_path)
                    repos.append(repo_path)
                except Exception:
                    # Skip invalid repositories
                    pass

        return sorted(repos, key=lambda p: p.name.lower())

    def get_local_head(self, repo_path: Path) -> str:
        """
        Get the local HEAD commit SHA.

        Args:
            repo_path: Path to repository

        Returns:
            Commit SHA string
        """
        repo = git.Repo(repo_path)
        return repo.head.commit.hexsha

    def get_remote_url(self, repo_path: Path) -> str:
        """
        Get the remote URL for the repository.

        Args:
            repo_path: Path to repository

        Returns:
            Remote URL string
        """
        repo = git.Repo(repo_path)

        if not repo.remotes:
            return ""

        # Get origin remote or first remote
        remote = repo.remotes.origin if 'origin' in [r.name for r in repo.remotes] else repo.remotes[0]

        return remote.url
