# GitHub Star Manager

A full-stack application for managing and visualizing GitHub starred repositories.

## Overview

GitHub Star Manager consists of three main components:

1. **Backend API** - Hono-based REST API serving repository data
2. **Frontend UI** - Svelte 5 application with grid and list views
3. **CLI Tool** - Python script for scanning local Git repositories

## Architecture

```
github_star_manager/
├── backend/           # Hono API (TypeScript)
├── frontend/          # Svelte 5 UI (TypeScript)
├── cli/              # Python CLI tool
└── .claude/          # Claude Code agent configuration
```

## Quick Start

### 1. Install Dependencies

**Backend:**
```bash
cd backend
npm install
```

**Frontend:**
```bash
cd frontend
npm install
```

**CLI:**
```bash
cd cli
pip install -r requirements.txt
```

### 2. Generate Repository Data

Scan your local directories for Git repositories:

```bash
cd cli
python star_manager.py ~/projects -o ../backend/repos.json
```

### 3. Start the Backend

```bash
cd backend
npm run dev
```

The API will be available at `http://localhost:3000`

### 4. Start the Frontend

```bash
cd frontend
npm run dev
```

The UI will be available at `http://localhost:5173`

## Features

- Scan local directories for Git repositories
- Extract repository metadata (name, URL, last commit)
- REST API with Zod validation
- Responsive grid and list views
- Loading and error state handling
- Production-ready builds
- Automated linting (biome for TS/JS, ruff for Python)

## Development

### Backend

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run linter
- `npm run lint:fix` - Fix linting issues

### Frontend

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run linter
- `npm run lint:fix` - Fix linting issues

### CLI

- `python star_manager.py <path>` - Scan directory
- `python star_manager.py <path> --verbose` - Verbose output
- `python star_manager.py <path> -o custom.json` - Custom output file

## API Documentation

See [backend/README.md](backend/README.md) for API endpoint documentation.

## Claude Code Integration

This project includes a complete Claude Code agent configuration in `.claude/`:

- **Agents**: Specialized subagents for backend, frontend, and CLI
- **Skills**: Domain-specific knowledge for Hono, Svelte, and Python
- **Commands**: `/build-star-manager` orchestration command
- **Hooks**: Pre-commit linting automation

## License

MIT
