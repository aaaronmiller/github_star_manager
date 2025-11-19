# GitHub Star Manager API

Backend REST API for the GitHub Star Manager application, built with Hono and TypeScript.

## Features

- RESTful API endpoints
- Zod schema validation
- CORS support
- Request logging
- Comprehensive error handling
- TypeScript strict mode

## Installation

```bash
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The API will be available at `http://localhost:3000`

## Build

Build for production:

```bash
npm run build
```

Run the production build:

```bash
npm start
```

## Linting

Run linter:

```bash
npm run lint
```

Auto-fix linting issues:

```bash
npm run lint:fix
```

## API Endpoints

### GET /

Health check endpoint.

**Response:**
```json
{
  "name": "GitHub Star Manager API",
  "version": "1.0.0",
  "endpoints": {
    "repos": "/api/repos"
  }
}
```

### GET /api/repos

Get all repositories from the repos.json file.

**Response:** `200 OK`
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

**Error Responses:**

- `404 Not Found` - repos.json file not found
- `400 Bad Request` - Invalid data in repos.json
- `500 Internal Server Error` - Server error

## Data Schema

The API validates data using Zod schemas:

```typescript
interface Repository {
  name: string;
  url: string;
  description?: string;
  stars?: number;
  language?: string;
  lastUpdated?: string;
}

interface Metadata {
  totalCount: number;
  lastScanned: string;
}

interface ReposData {
  repositories: Repository[];
  metadata: Metadata;
}
```

## Configuration

- **Port**: Set via `PORT` environment variable (default: 3000)
- **repos.json**: Place in the backend root directory

## Tech Stack

- **Hono** - Fast web framework
- **Zod** - Schema validation
- **TypeScript** - Type safety
- **Biome** - Linting and formatting
