# Agentic Update Assistant CLI

A Python CLI tool for intelligent local repository management with AI-powered update analysis.

## Features

- Scan local directories for Git repositories
- Compare local and remote repository states
- AI-powered impact analysis of pending updates
- Categorize updates by risk level (safe, needs review)
- Generate safe update scripts for review

## Installation

1. Install Python 3.11 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create configuration file at `~/.config/repo-updater/config.json`:

```json
{
  "repo_root_dir": "/path/to/your/projects",
  "github_token": "your_github_token_here",
  "gemini_api_key": "your_gemini_api_key_here"
}
```

## Usage

Run the updater:

```bash
python updater.py
```

This will:
1. Scan your configured directory for Git repositories
2. Check each repository for available updates
3. Analyze changes using AI
4. Display color-coded update recommendations
5. Generate a safe update script

## Configuration

The tool reads configuration from `~/.config/repo-updater/config.json`:

- `repo_root_dir`: Root directory to scan for repositories
- `github_token`: GitHub personal access token (for higher API rate limits)
- `gemini_api_key`: Google Gemini API key (for AI analysis)

## Output

- **Green**: Up-to-date repositories
- **Yellow**: Safe to update (low risk)
- **Red**: Needs review (breaking changes or high risk)

Generated update scripts are saved to `update_script.sh` for manual review and execution.
