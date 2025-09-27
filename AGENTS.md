# AGENTS.md

## 1. Purpose
This file documents how AI coding agents (e.g., Codex) will be used in this project.  
It defines prompting conventions, repository structure, coding standards, and build/test workflows for the personal website.

---

## 2. Project Overview
- **Goal**: Build a personal website using React (scaffolded with Vite).  
- **Deployment**: GitHub Pages (with GitHub Actions workflow).  
- **Core Features**:
  - Landing page with intro and links
  - Resume/experience section
  - Blog posts (Markdown/MDX-based)
  - Dark/light theme toggle
  - Responsive, mobile-first layout

---

## 3. Repository Structure
A recommended starting structure:

```
repo/
├── src/ # Main application source
│ ├── components/ # Reusable React components
│ ├── pages/ # Page-level components
│ ├── styles/ # Global and Tailwind styles
│ ├── utils/ # Utility/helper functions
│ └── assets/ # Images, icons, fonts
├── public/ # Static files
├── tests/ # Unit/integration tests
├── .eslintrc.json # Linting configuration
├── .prettierrc # Code formatting rules
├── package.json
├── vite.config.js
└── README.md
```

---

## 4. Coding Standards

### 4.1 General
- **JavaScript/TypeScript**: ESNext syntax.
- **React**: Functional components, React Hooks, Context API where appropriate.
- **Styling**: TailwindCSS for rapid and consistent styling.
- **Linting**: ESLint configured with Airbnb + React plugin.
- **Formatting**: Prettier for consistent style.
- **Git**: Meaningful commit messages (e.g., `feat: add navbar component`).

### 4.2 PEP8
Even though this repo is React-focused, any supporting Python scripts (for tooling, automation, data, etc.) must follow **PEP8** standards:
- Use `black` or `flake8` for formatting.
- Follow 79-character line length where applicable.
- Consistent docstrings using `"""triple quotes"""`.

### 4.3 Additional Notes
- Strict typing: pydantic / Python type hints everywhere.
- Logging: structured logs with structlog or logging.
- Testing: pytest for unit/integration tests.
- Linting/formatting: black, isort, flake8/ruff.
- Async patterns: leverage asyncio for non-blocking servers.
- Docs: docstrings + auto-generated docs with mkdocs or sphinx.

---

## 5. Build & Test Commands

### 5.1 Local Development
```bash
# Install dependencies
npm install

# Start local dev server
npm run dev

# Run tests
npm test

# Lint & format
npm run lint
npm run format
```

### 5.2 Remote Build (GitHub Pages)

Deployment will be automated via GitHub Actions.

```bash
# Create production build
npm run build

# Preview production build locally
npm run preview
```

The dist/ directory will be deployed to GitHub Pages using an Actions workflow.

## 6. Code Style Guidelines
### JavaScript/React
- Use functional components with hooks.
- Keep components small and reusable.
- Destructure props at the component level.
- Use explicit imports, avoid * imports.
- Follow consistent naming conventions:
    - PascalCase for components.
    - camelCase for variables/functions.
    - UPPER_CASE for constants.

### CSS/Tailwind
- Prefer utility classes from Tailwind.
- Extract reusable patterns into @apply or component-level style files when needed.


## 7. Testing Instructions

- Use Jest + React Testing Library for unit and integration tests.
- Tests live in /tests with .test.js or .spec.js suffix.

```bash
Example:

npm test
```

- For end-to-end tests, consider Playwright or Cypress in future iterations.



## 8. Security Considerations
- Never commit API keys, secrets, or tokens (use .env with .gitignore).
- Sanitize any user-generated content before rendering.
- Keep dependencies up to date (npm audit fix regularly).
- Enable Dependabot for GitHub repo.
- Use HTTPS-only deployment (GitHub Pages defaults to HTTPS).
- Validate external links and resources to avoid mixed content.

## 9. Agent Workflow
- Draft clear prompt for Codex (single responsibility per task).
- Generate code → review → test locally.
- Refine if necessary.
- Create and update SUMMARY.md with timestamps and actions taken, as a changelog of sorts

## 10. Future Extensions
- Add blog integration with MDX.
- Consider i18n (internationalization).
- Explore adding 3D/interactive elements (e.g., tilt cards, animations).
- Automate accessibility tests (axe-core, Lighthouse).