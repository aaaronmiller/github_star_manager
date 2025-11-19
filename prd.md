Product Requirements Document: Agentic Build System for GitHub Star Manager1. OverviewThis document defines the configuration for a "Claude Code" agentic environment designed to autonomously build the "GitHub Star Manager" application. The system utilizes a hub-and-spoke model where a central Orchestrator manages specialized subagents.2. System Architecture2.1 The Orchestrator (Root Session)Role: Project Manager & Integration Lead.Context: Loaded via CLAUDE.md.Capabilities: Spawning agents, reading global config, executing git commands, file system management.Primary Interface: Custom Slash Command /build-star-manager.2.2 Subagents (The Workers)All agents are defined in .claude/agents/ and strictly scoped to their domain to prevent context pollution.Agent NameRoleToolsModelapi-engineerBackend LogicRead, Write, Bash, GrepSonnetui-architectFrontend UX/UIRead, Write, Bash, GrepSonnetsys-adminLocal CLI ToolRead, Write, Bash, GrepSonnet2.3 Skills (The Knowledge)Modular markdown files in .claude/skills/ containing specific technical constraints and patterns.hono-skill: Hono routing, Zod validation, Cloudflare bindings.svelte-skill: Svelte 5 Runes, Tailwind utility classes, store patterns.python-skill: argparse, GitPython, rich library for TUI.3. Implementation Details3.1 Directory Structure.claude/
├── settings.json           # Global permissions & model config
├── commands/
│   └── build-star-manager.md # The Master Orchestration Script
├── agents/
│   ├── api-engineer.md     # Hono specialist
│   ├── ui-architect.md     # Svelte specialist
│   └── sys-admin.md        # Python specialist
├── skills/
│   ├── hono/SKILL.md
│   ├── svelte/SKILL.md
│   └── python/SKILL.md
└── hooks/
    └── pre-commit.sh       # Auto-linting before commit
3.2 The Master Command (/build-star-manager)This command functions as the build script. It contains the step-by-step logic:Initialize: npm create svelte@latest & npm create hono@latest.Agent Handoff 1 (Backend): "Spawn api-engineer. Task: Implement repos.json schema and GET /repos endpoint using hono-skill."Agent Handoff 2 (Frontend): "Spawn ui-architect. Task: Fetch data from /api/repos and render Grid using svelte-skill."Agent Handoff 3 (CLI): "Spawn sys-admin. Task: Create main.py to scan local folders matching the repos.json structure."3.3 Data ContractsThe CLAUDE.md file will contain the Shared Schemas (JSON structure for Repos and Instructions) so all agents adhere to the same data format without needing to communicate directly.4. Execution Strategy (Headless)To run this autonomously:claude --headless --print-stdout --command "/build-star-manager 'Build the MVP with just the Dashboard and List functionality'"
5. Success MetricsZero-Touch Scaffolding: The directory structure is created without human input.Passing Builds: npm run build passes for frontend and backend.Lint Compliance: All code passes biome (JS/TS) and ruff (Python) checks via Hooks.
