# GitHub Star Manager - Project Context

## Project Overview
GitHub Star Manager is a full-stack application for managing and visualizing GitHub starred repositories. It consists of three main components:

1. **Backend API** (Hono + TypeScript)
2. **Frontend UI** (Svelte 5 + Tailwind CSS)
3. **CLI Tool** (Python)

## Architecture

```
github_star_manager/
├── backend/           # Hono API server
├── frontend/          # Svelte 5 UI
├── cli/              # Python CLI tool
└── .claude/          # Agent configuration
```

## Shared Data Schema

### Repository Object
All components must use this consistent schema:

```typescript
interface Repository {
  name: string;           // Repository name (required)
  url: string;           // Repository URL (required, must be valid URL)
  description?: string;  // Short description (optional)
  stars?: number;        // Star count (optional)
  language?: string;     // Primary language (optional)
  lastUpdated?: string;  // ISO 8601 date string (optional)
}
```

### repos.json Structure
```json
{
  "repositories": [
    {
      "name": "example-repo",
      "url": "https://github.com/user/example-repo",
      "description": "An example repository",
      "stars": 1234,
      "language": "TypeScript",
      "lastUpdated": "2025-01-15T10:30:00Z"
    }
  ],
  "metadata": {
    "totalCount": 1,
    "lastScanned": "2025-01-15T10:30:00Z"
  }
}
```

## API Endpoints

### GET /api/repos
Returns all repositories.

**Response**: `200 OK`
```json
{
  "repositories": [...],
  "metadata": {...}
}
```

**Error Response**: `500 Internal Server Error`
```json
{
  "error": "Internal Server Error",
  "message": "Error message here"
}
```

## Component Responsibilities

### Backend (api-engineer)
- Serve API endpoints
- Validate data with Zod
- Read repos.json file
- Handle errors with appropriate HTTP codes
- Enable CORS for frontend access

### Frontend (ui-architect)
- Fetch data from API
- Display in Grid and List views
- Handle loading states
- Handle error states
- Responsive design
- Svelte 5 Runes API

### CLI (sys-admin)
- Scan directories for Git repos
- Extract repository metadata
- Generate repos.json file
- Provide rich terminal output
- Handle file system errors

## Development Standards

### TypeScript
- Strict mode enabled
- Explicit types for all exports
- No `any` types
- Use Zod for runtime validation

### Python
- Type hints for all functions
- PEP 8 compliance
- Docstrings for public functions
- Error handling with try/except

### Styling
- Tailwind CSS utility classes
- Mobile-first responsive design
- Consistent color scheme
- Accessible components

## Success Criteria
1. All builds pass without errors
2. All linters pass (biome, ruff)
3. API returns valid JSON
4. UI displays data correctly
5. CLI generates valid repos.json
6. No placeholders or TODOs in code
7. Production-ready quality
