# Build Star Manager Command

You are the **Orchestrator** for building the GitHub Star Manager application. Follow these steps in order:

## Step 1: Initialize Project Structure
- Create the `frontend/` directory for the Svelte 5 application
- Create the `backend/` directory for the Hono API
- Create the `cli/` directory for the Python tool

## Step 2: Backend API (Delegate to api-engineer)
Spawn the **api-engineer** agent with the following task:

**Task**: Build a Hono API with the following requirements:
1. Create a Hono application with CORS and logging middleware
2. Implement a `repos.json` schema using Zod that includes:
   - name (string, required)
   - url (string, URL format, required)
   - description (string, optional)
   - stars (number, optional)
   - language (string, optional)
   - lastUpdated (string, ISO date, optional)
3. Create a GET `/api/repos` endpoint that:
   - Reads from a `repos.json` file
   - Validates the data against the schema
   - Returns the repositories as JSON
   - Handles errors appropriately
4. Set up proper TypeScript configuration
5. Add necessary dependencies and build scripts

Reference the **hono-skill** for patterns and best practices.

## Step 3: Frontend UI (Delegate to ui-architect)
Spawn the **ui-architect** agent with the following task:

**Task**: Build a Svelte 5 UI with the following requirements:
1. Create a SvelteKit application structure
2. Set up Tailwind CSS for styling
3. Build a Dashboard page that:
   - Fetches data from `/api/repos`
   - Displays repositories in a responsive grid layout
   - Shows loading and error states
   - Includes repository name, description, stars, and language
4. Build a List view as an alternative display
5. Use Svelte 5 Runes ($state, $derived, $effect)
6. Implement mobile-first responsive design
7. Add proper TypeScript types

Reference the **svelte-skill** for patterns and best practices.

## Step 4: CLI Tool (Delegate to sys-admin)
Spawn the **sys-admin** agent with the following task:

**Task**: Build a Python CLI tool with the following requirements:
1. Create a script that scans a directory for Git repositories
2. Use argparse for command-line interface:
   - Accept a path argument to scan
   - Accept an optional --output flag for the output file
   - Accept a --verbose flag for detailed output
3. Use GitPython to extract repository information:
   - Repository name
   - Remote URL
   - Current branch
   - Last commit info
   - Star count (if available from remote)
4. Generate a `repos.json` file matching the backend schema
5. Use Rich library for formatted terminal output
6. Add proper error handling and type hints
7. Create requirements.txt with dependencies

Reference the **python-skill** for patterns and best practices.

## Step 5: Integration & Testing
1. Ensure all builds pass (`npm run build` for frontend and backend)
2. Verify the CLI generates valid JSON
3. Test the API can read and serve the generated data
4. Test the frontend can fetch and display the data
5. Run linters (biome for TS/JS, ruff for Python)

## Step 6: Documentation
Create README files for:
- Project root (overview, architecture, setup)
- Backend (API documentation, endpoints)
- Frontend (component structure, development)
- CLI (usage examples, options)

## Success Criteria
✓ All TypeScript/JavaScript code passes biome linting
✓ All Python code passes ruff linting
✓ Frontend builds successfully
✓ Backend builds successfully
✓ CLI generates valid repos.json
✓ API serves data correctly
✓ UI displays data with loading/error states
