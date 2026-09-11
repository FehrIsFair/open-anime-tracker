---
name: spec-workflow-integration
description: Execute the project's spec-driven development workflow. Activates when the user wants to plan, design, or implement a new feature. Guides through requirements → design → tasks → implementation with approval gates, using project-specific templates and steering docs.
---

# Spec Workflow Integration

This skill guides the agent through the spec-driven development workflow using the `.spec-workflow/` directory structure. Use it whenever the user wants to plan or build a new feature.

## Workflow Overview

```
1. Steering Docs   → Define project standards (tech, structure, product)
2. Requirements     → User stories + acceptance criteria
3. Design           → Architecture, components, data models, error handling
4. Tasks            → Granular, actionable implementation steps with prompts
5. Implementation   → Execute tasks, log progress
6. Approval         → Review and approve completed specs
7. Archive          → Move completed specs to archive
```

## When to Activate

- User says "plan a feature", "spec out", "design a feature", "create a spec"
- User wants to add a new feature and needs structured planning
- User wants to review or continue an existing spec
- User references the spec workflow

## Directory Structure

```
.spec-workflow/
├── steering/             ← Project-wide standards (tech.md, structure.md, product.md)
├── templates/            ← Default document templates
├── user-templates/       ← Custom templates (override defaults)
├── specs/                ← Active spec directories (one per feature)
│   └── {feature-name}/
│       ├── requirements.md
│       ├── design.md
│       ├── tasks.md
│       └── Implementation Logs/   ← Per-task implementation logs
├── approvals/            ← Approved/completed specs
│   └── {feature-name}/
└── archive/              ← Archived old specs
```

## Step-by-Step Workflow

### Step 0: Determine Where We Are

Ask the user what they need:

- **"I want to plan a new feature"** → Start from Step 1
- **"I want to implement {feature}"** → Check if a spec exists; if not, jump to creating it, then implement
- **"Continue working on {feature}"** → Find the existing spec, check which tasks are done, continue from there
- **"Review/approve {feature}"** → Move to Step 6
- **"What features are in progress?"** → List specs under `specs/`

### Step 1: Steering Documents (One-Time Setup)

Steering docs define project-wide standards. Check if they exist under `.spec-workflow/steering/`. If not, create them based on the project's AGENTS.md and actual codebase.

**Files to create (if missing):**

- **`tech.md`** — Technology stack, languages, frameworks, databases, tools, coding standards
- **`structure.md`** — Directory layout, naming conventions, import patterns, code organization
- **`product.md`** — Product purpose, target users, key features, objectives, principles

**How to create them:**

1. Read `AGENTS.md` in the project root
2. Scan the actual codebase (file structure, imports, patterns) to verify conventions
3. Write steering docs that match reality, not templates
4. Always reference actual files, functions, and patterns from the codebase

These are created once and updated when the project's architecture changes.

### Step 2: Requirements Document

Create a new spec directory: `.spec-workflow/specs/{feature-name}/`

Create `requirements.md` using the template at `.spec-workflow/templates/requirements-template.md` (or `user-templates/requirements-template.md` if customized).

**Structure to follow:**

```markdown
# Requirements Document

## Introduction
[What this feature does and its value]

## Alignment with Product Vision
[How it fits the project goals]

## Requirements
### Requirement N: [Title]
**User Story:** As a [role], I want [feature], so that [benefit]
#### Acceptance Criteria
1. WHEN [event] THEN [system] SHALL [response]
2. ...

## Non-Functional Requirements
### Code Architecture and Modularity
### Performance
### Security
### Reliability
### Usability
```

**Key rules:**
- Write requirements in clear, testable language
- Use WHEN/THEN acceptance criteria format
- Include non-functional requirements (performance, security, reliability)
- Number requirements sequentially for task traceability

### Step 3: Design Document

Create `design.md` in the same spec directory using the template.

**Structure to follow:**

```markdown
# Design Document

## Overview
[High-level description]

## Steering Document Alignment
### Technical Standards (tech.md)
[How it follows project standards]

### Project Structure (structure.md)
[How it follows project organization]

## Code Reuse Analysis
### Existing Components to Leverage
- **[Actual File/Module]**: [How it will be used]

### Integration Points
- **[System/API]**: [Integration details]

## Architecture
[Design patterns, mermaid diagram]

### Modular Design Principles
- [Separation of concerns]

## Components and Interfaces
### Component N
- **Purpose:** [What it does]
- **Interfaces:** [API/signatures]
- **Dependencies:** [What it needs]
- **Reuses:** [Existing code to leverage — reference actual files]

## Data Models
[If new data structures, define them with actual field names]

## Error Handling
[Error scenarios with handling and user impact]

## Testing Strategy
[Unit, integration, E2E testing approach]
```

**Key rules:**
- Reference **actual existing files** in the codebase — never hypothetical paths
- Include a mermaid diagram for the architecture
- List every component with clear purpose and interfaces
- Analyze what existing code will be leveraged
- Define error handling for all failure modes

### Step 4: Tasks Document

Create `tasks.md` — this is the bridge between design and implementation. Each task must be a single, focused action that produces a file change.

**Structure to follow:**

```markdown
# Tasks Document

- [ ] 1. [Action-oriented title]
  - File: `path/to/file.ext` (new|modify)
  - [What to implement — specific functions, fields, behaviors]
  - Purpose: [Why this task exists]
  - _Leverage: `actual/file/path.py`_
  - _Requirements: [requirement numbers, e.g., 1.1, 2.3]_
  - _Prompt: Role: [Role] with expertise in [skills] | Task: [detailed instruction] | Restrictions: [boundaries] | _Leverage: [files] | _Requirements: [numbers]_ | Success: [definition of done]_
```

**Key rules for tasks:**

1. **Each task is a single file change** — don't combine multiple files in one task
2. **File column is critical** — always specify the exact file path and whether it's new or modified
3. **Prompt column is critical** — embed the full agent prompt so tasks can be delegated to sub-agents later
4. **Reference actual code** — leverage column should point to real files in the codebase
5. **Trace to requirements** — every task references requirement numbers
6. **Order by dependency** — earlier tasks must complete before later ones can start
7. **Include sub-tasks** (3a, 3b, 3c) when related file changes naturally group together
8. **Be specific about patterns** — reference exact existing patterns (blueprint setup, form patterns, API helper patterns)

### Step 5: Implementation

Now implement the tasks one by one. For each task:

1. Read the task description from `tasks.md`
2. Read the design document for context
3. Read the files the task will modify/leverage to understand existing patterns
4. Implement the task
5. Create an **implementation log** in `Implementation Logs/task-{N}_{short-name}.md`

**Implementation log format:**

```markdown
# Task N Implementation Log: {Title}

**Timestamp:** {date}
**Task:** {task title}
**Status:** {In Progress | Completed | Blocked}

## Summary
[Brief description of what was done]

## Files Modified/Created
| File | Action | Lines |
|------|--------|-------|
| `path/to/file` | Created/Modified | +N/-M |

## Key Implementation Details
- [Notable decisions or patterns followed]
- [Any deviations from the spec]
```

**After completing all tasks:**

1. Mark all tasks as done in `tasks.md` (change `- [ ]` to `- [x]`)
2. Check that all references in the spec point to real files
3. Run the app to verify the feature works (start infra, backend, frontend if applicable)

### Step 6: Approval

When a spec is complete:

1. Verify all tasks are marked done
2. Verify the feature works end-to-end
3. Copy the spec directory to `.spec-workflow/approvals/{feature-name}/`
4. Optionally archive the spec (move from `specs/` to `archive/`)

### Step 7: Archive

Old completed specs can be moved to `.spec-workflow/archive/` to keep the active specs directory clean. The approvals directory keeps a reference.

## Template Customization

The project can have custom templates in `.spec-workflow/user-templates/`. Always check there first before using defaults from `.spec-workflow/templates/`.

Current custom templates:
- `README.md` — Explains custom template usage

To customize a template, create a file with the same name in `user-templates/`.

## Practical Tips

### For Creating Specs Fast

1. Start with a clear feature description from the user
2. Create steering docs once (they're project-wide, not per-feature)
3. Requirements → Design → Tasks flow naturally — each document builds on the previous
4. The tasks document is the most important — it's what you'll actually execute from
5. Include agent prompts in tasks so they can be delegated

### For Continuing Work on an Existing Spec

1. Read `tasks.md` to see which tasks are checked off
2. Check `Implementation Logs/` for context on what was done
3. Resume from the first unchecked task
4. Update implementation logs with current progress

### For Reviewing a Spec

1. Check requirements are testable (WHEN/THEN format)
2. Check design references real existing code
3. Check tasks are actionable (not vague — each references specific files)
4. Check implementation logs match completed work
5. Verify the feature works by running the app

### Common Patterns to Recognize

This project uses:
- **Flask blueprints** for routes (see `routes/anime.py`, `routes/user.py`)
- **Service layer** pattern (`common_funcs/` for utilities)
- **SQLAlchemy models** (`db_models/`)
- **React + TypeScript + Material-UI** for frontend (`oat-frontend/src/`)
- **Axios engine** for API calls (`oat-frontend/src/BackendRequests/`)
- **Auth context** for authentication (`context/auth_context`)
- **Docker Compose** for PostgreSQL + Redis infrastructure

Always reference these patterns when writing design and tasks documents.
