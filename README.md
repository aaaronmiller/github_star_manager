# Agentic GitHub Star Manager

An AI-powered platform for managing and maintaining your GitHub starred repositories with intelligent update analysis and multi-OS installation guides.

## Features

### Web Dashboard
- **Repository Dashboard**: Browse, search, and sort your curated GitHub repositories
- **Multi-OS Installation Guides**: Platform-specific instructions for macOS, Windows, Linux, and Docker
- **AI-Powered Repository Ingestion**: Automatically extract metadata and installation instructions using Gemini AI
- **Responsive Design**: Beautiful, mobile-friendly interface built with SvelteKit and Tailwind CSS

### CLI Tool
- **Local Repository Scanning**: Automatically find all Git repositories in your projects directory
- **Intelligent Update Analysis**: AI-powered analysis of pending updates using Gemini
- **Risk Categorization**: Updates categorized as "up-to-date", "safe to update", or "needs review"
- **Safe Update Scripts**: Generate shell scripts for low-risk updates
- **Rich Terminal Output**: Color-coded results with detailed summaries

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User (Developer)                      │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             │ Browser                    │ Terminal
             │                            │
┌────────────▼────────────┐   ┌──────────▼──────────────┐
│   SvelteKit Frontend    │   │   Python CLI Tool       │
│  (Cloudflare Pages)     │   │                         │
│                         │   │  - Repository scanner   │
│  - Dashboard UI         │   │  - Update analyzer      │
│  - Installation pages   │   │  - Script generator     │
│  - Search/filter        │   │                         │
└────────────┬────────────┘   └──────────┬──────────────┘
             │                            │
             │ API Calls                  │ GitHub API
             │                            │
┌────────────▼────────────┐              │
│   SvelteKit API         │              │
│   (Serverless)          │◄─────────────┘
│                         │
│  - GET /api/repos       │   ┌──────────────────┐
│  - GET /api/instructions│──►│   Gemini API     │
│  - POST /api/add-repo   │   │  (AI Analysis)   │
└────────────┬────────────┘   └──────────────────┘
             │
             │ Read Data
             │
┌────────────▼────────────┐
│   Data Store (JSON)     │
│                         │
│  - repos.json           │
│  - instructions.json    │
└─────────────────────────┘
```

## Technology Stack

- **Frontend**: SvelteKit 2.x + Svelte 5 (Runes API) + Tailwind CSS
- **Deployment**: Cloudflare Pages (SSG)
- **API**: SvelteKit API routes with Zod validation
- **AI Integration**: Google Gemini API
- **CLI**: Python 3.11+ with Rich, Click, GitPython, PyGithub
- **Data Storage**: JSON files in Git repository

## Getting Started

### Prerequisites

- Node.js 18.0 or higher
- Python 3.11 or higher (for CLI tool)
- Gemini API key ([Get one here](https://ai.google.dev/))
- GitHub personal access token (optional, for higher rate limits)

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/agentic-github-star-manager.git
cd agentic-github-star-manager
```

#### 2. Install frontend dependencies

```bash
npm install
```

#### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
```

#### 4. Run the development server

```bash
npm run dev
```

The application will be available at http://localhost:5173

#### 5. Install CLI tool (optional)

```bash
cd cli
pip install -r requirements.txt
```

Create CLI configuration:

```bash
mkdir -p ~/.config/repo-updater
cp config.example.json ~/.config/repo-updater/config.json
```

Edit `~/.config/repo-updater/config.json`:

```json
{
  "repo_root_dir": "/path/to/your/projects",
  "github_token": "your_github_token",
  "gemini_api_key": "your_gemini_api_key"
}
```

Run the CLI:

```bash
python updater.py
```

## Usage

### Adding Repositories

1. Navigate to the dashboard
2. Enter a GitHub repository URL in the "Add New Repository" field
3. Click "Add Repository"
4. The AI will analyze the repository and extract metadata
5. Review the generated data and commit to persist

### Browsing Repositories

- Use the search bar to filter repositories by name or description
- Sort by "Date Added", "Last Updated", or "Created Date"
- Click on any repository card to view detailed installation instructions

### Installation Instructions

Each repository detail page provides:
- Multi-OS installation guides (macOS, Windows, Linux, Docker)
- Step-by-step commands with copy buttons
- Platform-specific notes and prerequisites
- Mobile/device setup instructions when applicable

### CLI Update Management

Run the CLI tool to:
1. Scan your local projects directory for Git repositories
2. Check each repository against its remote
3. Analyze pending updates with AI
4. Get color-coded recommendations:
   - **Green**: Up-to-date
   - **Yellow**: Safe to update (low risk)
   - **Red**: Needs review (breaking changes or high risk)
5. Generate and review update scripts for safe updates

## Deployment

### Cloudflare Pages

1. Push your code to GitHub
2. Connect your repository to Cloudflare Pages
3. Configure build settings:
   - Build command: `npm run build`
   - Build output directory: `.svelte-kit/cloudflare`
4. Add environment variables in Cloudflare dashboard:
   - `GEMINI_API_KEY`
   - `GITHUB_TOKEN` (optional)
5. Deploy!

Your site will automatically rebuild on every push to your repository.

## Data Schema

### Repository Schema

```typescript
interface Repository {
  id: string;                // "owner-repo_name" (lowercase)
  url: string;              // Full GitHub URL
  name: string;             // Repository name
  owner: string;            // Owner/organization
  summary: string;          // AI-generated summary
  createdAt: string;        // ISO 8601 timestamp
  lastUpdatedAt: string;    // ISO 8601 timestamp
  addedAt: string;          // ISO 8601 timestamp
}
```

### Instructions Schema

```typescript
interface Instructions {
  macOS?: OSInstructions;
  windows?: OSInstructions;
  linux?: OSInstructions;
  docker?: DockerInstructions;
  mobile?: MobileInstructions;
}

interface OSInstructions {
  summary: string;
  steps: string[];
  notes?: string;
}

interface DockerInstructions extends OSInstructions {
  isPreferred: boolean;
  rationale: string;
}

interface MobileInstructions extends OSInstructions {
  hostOS: string;
  deviceOS: string;
}
```

## API Endpoints

### `GET /api/repos`

Returns all repositories with optional sorting.

**Query Parameters:**
- `sort`: `dateAdded` | `lastUpdated` | `createdDate`

**Response:**
```json
{
  "repositories": [...],
  "metadata": {
    "totalCount": 5,
    "lastScanned": "2024-11-19T12:00:00Z"
  }
}
```

### `GET /api/instructions/:id`

Returns installation instructions for a specific repository.

**Response:**
```json
{
  "macOS": { ... },
  "windows": { ... },
  "linux": { ... },
  "docker": { ... }
}
```

### `POST /api/add-repo`

Adds a new repository using AI analysis.

**Request:**
```json
{
  "urls": ["https://github.com/owner/repo"]
}
```

**Response:**
```json
{
  "success": true,
  "results": [...],
  "message": "Processed 1 repository URL(s)"
}
```

## Development

### Project Structure

```
agentic-github-star-manager/
├── src/
│   ├── lib/
│   │   ├── data/
│   │   │   ├── repos.json
│   │   │   └── instructions.json
│   │   ├── types.ts
│   │   └── schemas.ts
│   ├── routes/
│   │   ├── api/
│   │   │   ├── repos/+server.ts
│   │   │   ├── instructions/[id]/+server.ts
│   │   │   └── add-repo/+server.ts
│   │   ├── repo/[id]/
│   │   │   ├── +page.svelte
│   │   │   └── +page.ts
│   │   ├── +layout.svelte
│   │   ├── +page.svelte
│   │   └── +page.ts
│   ├── app.html
│   └── app.css
├── cli/
│   ├── updater.py
│   ├── scanner.py
│   ├── analyzer.py
│   ├── script_generator.py
│   ├── requirements.txt
│   └── README.md
├── static/
├── package.json
├── svelte.config.js
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run check` - Type check

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.

## Acknowledgments

- Built with [SvelteKit](https://kit.svelte.dev/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- AI powered by [Google Gemini](https://ai.google.dev/)
- Deployed on [Cloudflare Pages](https://pages.cloudflare.com/)

## Related Documentation

For comprehensive product requirements and architecture details, see [prd-2.md](./prd-2.md).
