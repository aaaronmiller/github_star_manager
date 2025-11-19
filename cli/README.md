# GitHub Star Manager CLI

A Python command-line tool for scanning directories and extracting Git repository information.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python star_manager.py ~/projects
```

Specify output file:
```bash
python star_manager.py ~/projects -o custom.json
```

Adjust search depth and enable verbose output:
```bash
python star_manager.py ~/projects --depth 5 --verbose
```

## Options

- `path` - Directory path to scan for repositories (required)
- `-o, --output` - Output JSON file path (default: repos.json)
- `-d, --depth` - Maximum directory depth to search (default: 3)
- `-v, --verbose` - Enable verbose output

## Output Format

The tool generates a JSON file with the following structure:

```json
{
  "repositories": [
    {
      "name": "repo-name",
      "url": "https://github.com/user/repo-name",
      "description": "",
      "lastUpdated": "2025-01-15T10:30:00Z"
    }
  ],
  "metadata": {
    "totalCount": 1,
    "lastScanned": "2025-01-15T10:30:00Z"
  }
}
```

## Features

- Recursively scans directories for Git repositories
- Extracts repository metadata including remote URL and last commit date
- Displays progress with rich terminal UI
- Generates structured JSON output compatible with the API
- Handles errors gracefully
