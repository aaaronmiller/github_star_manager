# GitHub Star Manager UI

Frontend application for visualizing GitHub starred repositories, built with Svelte 5 and Tailwind CSS.

## Features

- Svelte 5 with Runes API ($state, $derived, $effect)
- Responsive grid and list views
- Loading and error states
- Tailwind CSS styling
- TypeScript type safety
- SvelteKit for routing and SSG

## Installation

```bash
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The UI will be available at `http://localhost:5173`

The dev server proxies `/api` requests to `http://localhost:3000` (backend).

## Build

Build for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Type Checking

Run Svelte type checker:

```bash
npm run check
```

Watch mode:

```bash
npm run check:watch
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

## Project Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── RepoCard.svelte       # Grid view card component
│   │   │   └── RepoListItem.svelte   # List view row component
│   │   └── types.ts                   # TypeScript type definitions
│   ├── routes/
│   │   ├── +layout.svelte             # Root layout
│   │   └── +page.svelte               # Main dashboard page
│   ├── app.css                        # Global styles with Tailwind
│   └── app.html                       # HTML template
├── static/                            # Static assets
├── svelte.config.js                   # Svelte configuration
├── tailwind.config.js                 # Tailwind configuration
├── vite.config.ts                     # Vite configuration
└── tsconfig.json                      # TypeScript configuration
```

## Components

### RepoCard

Grid view card component displaying repository information.

**Props:**
- `repo: Repository` - Repository data object

### RepoListItem

List view table row component.

**Props:**
- `repo: Repository` - Repository data object

### Main Page (+page.svelte)

Dashboard page with:
- Data fetching from `/api/repos`
- Grid/List view toggle
- Loading state spinner
- Error handling with retry
- Repository count and last scanned timestamp
- Responsive layout

## Styling

The UI uses Tailwind CSS utility classes with a mobile-first approach:

- **Breakpoints**: sm (640px), md (768px), lg (1024px)
- **Color Scheme**: Gray scale with blue accents
- **Layout**: Container with responsive grid (1-3 columns)

## Tech Stack

- **Svelte 5** - Reactive UI framework with Runes
- **SvelteKit** - Application framework
- **Tailwind CSS** - Utility-first CSS
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Biome** - Linting and formatting
