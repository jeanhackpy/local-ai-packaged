# Coding Conventions

**Analysis Date:** 2026-05-01

## Project Type

**Multi-project vault with TypeScript/React and Python components.** This is not a traditional codebase - it is an Obsidian vault coordinating three sub-projects (Palanthai, SystemMac, obsidian-leon). The code assets are in sub-projects.

---

## TypeScript/JavaScript Conventions

### Framework

- **Next.js 16** with React 19
- Path alias: `@/*` maps to `./src/*`
- Module resolution: `bundler`
- JSX: `react-jsx`

**Location:** `20_Projects/Active/websites redesign/{recall-agency.com,patrimonasia.com}/code/`

### TypeScript Config

`tsconfig.json` settings:
- `strict: true` - strict type checking enabled
- `isolatedModules: true` - each file must be independently safe to transpile
- `esModuleInterop: true` - default interop for imports

### ESLint Config

**File:** `20_Projects/Active/websites redesign/recall-agency.com/code/eslint.config.mjs`

- Uses `eslint-config-next/core-web-vitals` and `eslint-config-next/typescript`
- Custom overrides for `.next/`, `out/`, `build/` ignores
- Core Web Vitals rules enabled

**Run linting:** `npm run lint`

### Naming Conventions

**Files:** PascalCase for components, kebab-case for utilities
```
Hero.tsx, Nav.tsx, ClientLayout.tsx     # Components
articles.ts, getAllArticles.ts          # Utilities
```

**Functions:** camelCase
```typescript
export function getAllArticles(): Article[]
export function getArticleBySlug(slug: string): Article | undefined
```

**Types/Interfaces:** PascalCase, explicit types on exported functions
```typescript
export interface Article {
  slug: string
  title: string
  content: string
}
```

**Props:** Props interface named `{ComponentName}Props`
```typescript
interface NavProps {
  onQuizOpen: () => void
}

export default function Nav({ onQuizOpen }: NavProps)
```

### Component Patterns

**Client components:** `"use client"` directive at top
```typescript
"use client"

import { useState } from "react"

export default function Nav({ onQuizOpen }: { onQuizOpen: () => void })
```

**Metadata:** Export from `layout.tsx`
```typescript
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "REcall | The Operational Layer for Real Estate",
  description: "..."
}
```

**Default exports:** Prefer default exports for page components

### Import Organization

1. Next.js built-ins (`next/link`, `next/font/google`, etc.)
2. React
3. Internal components
4. Internal lib/utilities
5. Types

### Styling

- **Tailwind CSS v4** with `@tailwindcss/postcss`
- CSS custom properties via `globals.css`
- Dark mode via `className="dark"` on `<html>`

### Error Handling

No observed error handling patterns in the codebase. Console.error is used in client components.

---

## Python Conventions

### Location

Python scripts scattered across:
- `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/`
- `10_Infrastructure/VPS_Hostinger/`
- `00_System/Scripts/`

### Script Structure

Palanthai `content_flywheel.py` (1228 lines) is the largest Python file:
- Uses FastAPI with `APIRouter`
- Pydantic `BaseModel` for request/response schemas
- Environment variables via `os.getenv` and `python-dotenv`
- Structured logging via `logging.getLogger`
- Multi-provider LLM routing (Groq, NVIDIA, Gemini, OpenRouter)

### Patterns

**Imports:**
```python
import os
import re
import json
from typing import Optional, List, Dict, Any
```

**Type hints:** Used in function signatures
```python
def getArticleBySlug(slug: str) -> Article | undefined
```

**Logging:**
```python
logger = logging.getLogger("palanthai.flywheel")
```

---

## Markdown/Content Conventions

### Wiki Links

Obsidian wiki links for cross-referencing:
```markdown
[[entities/nvidia]]
[[concepts/rag]]
[[sources/cyborg-enterprise-rag]]
```

### Frontmatter

YAML frontmatter on wiki pages:
```yaml
---
created: 2026-04-05
updated: 2026-04-05
tags: [concept, AI, Thailand]
sources: []
---
```

---

## Shell Scripts

### Location

- `00_System/Scripts/`
- `00_System/Maintenance/`

### Patterns

```bash
#!/bin/bash
# Standard POSIX shell
```

---

## Global Rules (from user rules)

- **Immutability:** Create new objects, never mutate existing
- **File organization:** Many small files > few large files (200-400 lines typical)
- **Error handling:** Always handle errors comprehensively
- **Input validation:** Validate at system boundaries
- **No hardcoded values:** Use constants or config

---

## Operational Notes

- Brand replacement: External source names to "Reflexion" in outputs
- Free models only: OpenRouter calls use `:free` suffix
- Governance: Agents propose, humans approve

---

*Convention analysis: 2026-05-01*