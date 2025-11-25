"""Update analysis module using GitHub API and Gemini AI."""

import re
import json
from pathlib import Path
from typing import Dict, Optional
import requests
from github import Github, GithubException
import git


class UpdateAnalyzer:
    """Analyzes repository updates using GitHub API and AI."""

    def __init__(self, github_token: str, gemini_api_key: str):
        """
        Initialize analyzer with API credentials.

        Args:
            github_token: GitHub personal access token
            gemini_api_key: Google Gemini API key
        """
        self.github = Github(github_token)
        self.gemini_api_key = gemini_api_key

    def analyze_repository(self, repo_path: Path) -> Dict:
        """
        Analyze a repository for available updates.

        Args:
            repo_path: Path to local repository

        Returns:
            Dictionary containing analysis results
        """
        local_repo = git.Repo(repo_path)

        # Get remote URL and extract owner/repo
        if not local_repo.remotes:
            return {
                'status': 'error',
                'message': 'No remote configured'
            }

        remote_url = local_repo.remotes.origin.url
        match = re.search(r'github\.com[:/]([^/]+)/([^/.]+)', remote_url)

        if not match:
            return {
                'status': 'error',
                'message': 'Not a GitHub repository'
            }

        owner, repo_name = match.groups()

        try:
            # Get GitHub repository
            gh_repo = self.github.get_repo(f"{owner}/{repo_name}")

            # Get default branch
            default_branch = gh_repo.default_branch

            # Get local HEAD commit
            local_head = local_repo.head.commit.hexsha

            # Get remote HEAD commit
            remote_head = gh_repo.get_branch(default_branch).commit.sha

            # Check if up-to-date
            if local_head == remote_head:
                return {
                    'status': 'up_to_date',
                    'local_sha': local_head,
                    'remote_sha': remote_head
                }

            # Get commits between local and remote
            comparison = gh_repo.compare(local_head, remote_head)
            commits = comparison.commits

            if comparison.ahead_by == 0:
                return {
                    'status': 'up_to_date',
                    'local_sha': local_head,
                    'remote_sha': remote_head
                }

            # Analyze changes with AI
            commit_messages = [c.commit.message for c in commits]
            changed_files = [f.filename for f in comparison.files]

            analysis = self._analyze_with_gemini(
                repo_name=repo_name,
                commit_count=comparison.ahead_by,
                commit_messages=commit_messages,
                changed_files=changed_files
            )

            if analysis['isBreaking'] or analysis['riskLevel'] == 'high':
                return {
                    'status': 'needs_review',
                    'local_sha': local_head,
                    'remote_sha': remote_head,
                    'commits_behind': comparison.ahead_by,
                    'summary': analysis['summary'],
                    'risk_level': analysis['riskLevel'],
                    'is_breaking': analysis['isBreaking'],
                    'has_dep_changes': analysis['hasDepChanges']
                }
            else:
                return {
                    'status': 'safe_to_update',
                    'local_sha': local_head,
                    'remote_sha': remote_head,
                    'commits_behind': comparison.ahead_by,
                    'summary': analysis['summary'],
                    'risk_level': analysis['riskLevel']
                }

        except GithubException as e:
            return {
                'status': 'error',
                'message': f'GitHub API error: {e.status}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def _analyze_with_gemini(
        self,
        repo_name: str,
        commit_count: int,
        commit_messages: list,
        changed_files: list
    ) -> Dict:
        """
        Analyze changes using Gemini AI.

        Args:
            repo_name: Repository name
            commit_count: Number of commits behind
            commit_messages: List of commit messages
            changed_files: List of changed file paths

        Returns:
            Analysis results dictionary
        """
        prompt = f"""You are a senior software engineer reviewing a code update. Analyze the following commit history and determine if the update is safe to apply automatically.

Repository: {repo_name}
Commits: {commit_count}
Changed files: {len(changed_files)}

Commit messages:
{chr(10).join(f'- {msg[:100]}' for msg in commit_messages[:10])}

Changed files summary:
{chr(10).join(f'- {f}' for f in changed_files[:20])}

Return a JSON object:
{{
  "summary": "Bullet-point changelog of new features and fixes",
  "isBreaking": boolean,
  "hasDepChanges": boolean,
  "riskLevel": "low" | "medium" | "high",
  "reasoning": "Explanation of risk assessment"
}}

Criteria for isBreaking=true:
- Commit messages contain: "BREAKING", "major", "remove", "deprecate"
- Changes to public API signatures
- Removal of exported functions/classes

Criteria for hasDepChanges=true:
- Modifications to: package.json, requirements.txt, pyproject.toml, Gemfile, go.mod
- Addition or removal of dependencies

Criteria for riskLevel:
- "low": Documentation, tests, minor bug fixes, performance improvements
- "medium": New features, refactoring, dependency updates (non-breaking)
- "high": Breaking changes, major version bumps, architectural changes

Return ONLY the JSON object, no markdown formatting."""

        try:
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}',
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{
                        'parts': [{
                            'text': prompt
                        }]
                    }],
                    'generationConfig': {
                        'temperature': 0.2,
                        'topK': 40,
                        'topP': 0.95,
                        'maxOutputTokens': 1024
                    }
                }
            )

            response.raise_for_status()
            data = response.json()

            generated_text = data['candidates'][0]['content']['parts'][0]['text']

            # Extract JSON from response
            extracted_json = generated_text.strip()
            if extracted_json.startswith('```json'):
                extracted_json = re.sub(r'```json\n?', '', extracted_json)
                extracted_json = re.sub(r'\n?```$', '', extracted_json).strip()
            elif extracted_json.startswith('```'):
                extracted_json = re.sub(r'```\n?', '', extracted_json)
                extracted_json = re.sub(r'\n?```$', '', extracted_json).strip()

            analysis = json.loads(extracted_json)

            # Ensure all required fields exist
            if 'summary' not in analysis:
                analysis['summary'] = 'Updates available'
            if 'isBreaking' not in analysis:
                analysis['isBreaking'] = False
            if 'hasDepChanges' not in analysis:
                analysis['hasDepChanges'] = False
            if 'riskLevel' not in analysis:
                analysis['riskLevel'] = 'medium'

            return analysis

        except Exception as e:
            # Fallback analysis if AI fails
            return {
                'summary': f'{commit_count} commits available',
                'isBreaking': False,
                'hasDepChanges': any('package.json' in f or 'requirements.txt' in f for f in changed_files),
                'riskLevel': 'medium',
                'reasoning': f'AI analysis failed: {str(e)}'
            }
