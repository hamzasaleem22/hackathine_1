---
id: 0003
title: Add Framework Technology Stack Details
stage: spec
date: 2026-02-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-textbook
branch: 001-physical-ai-textbook
user: salim
command: implement plan
labels: ["spec", "framework", "technology-stack", "docusaurus", "typescript"]
links:
  spec: specs/001-physical-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-textbook/spec.md
tests:
  - Verified FR-036 updated with MDX clarification
  - Verified FR-042 updated with Structurizr and draw.io
  - Verified FR-049 through FR-055 added correctly
  - Verified Technology Stack Reference Table added
---

## Prompt

Implement the following plan:

# Plan: Add Framework and Technology Stack Details to Specification

## Context

The user requested research on which frameworks and technologies to use for writing and publishing the educational textbook on Physical AI & Humanoid Robotics. The specification currently mentions Docusaurus (FR-018) and programming languages (Python, Markdown/MDX), but lacks detailed framework choices for interactive features, diagrams, code playgrounds, and development tooling.

**Research completed** on best practices for educational textbook frameworks in 2026 reveals:
- **Docusaurus remains the top choice** for educational documentation (confirmed by industry comparison)
- **Interactive code playgrounds** via `@docusaurus/theme-live-codeblock` plugin
- **TypeScript is now the baseline** for serious JavaScript projects in 2026
- **Advanced diagram support** via Mermaid (already in spec), plus Structurizr for architecture diagrams
- **React 19** brings compiler optimizations (25-40% fewer re-renders)

## Recommended Technology Stack

[... Full plan content included technology recommendations for Docusaurus 3.x, TypeScript 5.x, interactive code playgrounds, diagram tools (Mermaid, Structurizr, draw.io), Node.js 18+, and development tooling ...]

## Specification Updates Required

### Add New Section: "Technology Stack & Frameworks"
- FR-049 through FR-055 covering TypeScript, code playgrounds, interactive execution, diagrams, Node.js, React components, and GitHub Actions
- Technology Stack Reference Table mapping components to technologies

### Update Existing Requirements
- FR-036: Clarify MDX usage for interactive components
- FR-042: Add Structurizr and draw.io diagram support

## Response snapshot

Successfully implemented all specification updates:

1. **Updated FR-036** (line 140):
   - Added clarification: "with MDX used for pages requiring interactive React components (code playgrounds, interactive diagrams)"

2. **Updated FR-042** (line 146):
   - Changed from SHOULD to MUST
   - Added: "Structurizr plugin for C4 model system architecture, and draw.io integration for complex robotics system illustrations"

3. **Added Technology Stack & Frameworks section** (lines 162-188):
   - FR-049: TypeScript for Docusaurus config and components
   - FR-050: @docusaurus/theme-live-codeblock integration
   - FR-051: Python code execution support for ROS 2, Isaac, VLA
   - FR-052: Multi-format diagram rendering (Mermaid, Structurizr, draw.io)
   - FR-053: Node.js 18+ requirement
   - FR-054: TypeScript for custom React components
   - FR-055: GitHub Actions with TypeScript compilation

4. **Added Technology Stack Reference Table** (lines 172-188):
   - 13 components mapped to technologies, versions, and purposes
   - Covers framework, languages, tools, CI/CD, hosting, analytics

All requirements are now properly sequenced between existing FR-048 and FR-023 sections.

## Outcome

- ✅ Impact: Specification now provides complete technology stack guidance for textbook development, covering frameworks (Docusaurus 3.x), languages (TypeScript 5.x for infrastructure, Python for content), interactive features (live code playgrounds), diagram tools (Mermaid, Structurizr, draw.io), and deployment infrastructure (Node.js 18+, GitHub Actions, GitHub Pages)
- 🧪 Tests: Manual verification of all edits - FR-036 and FR-042 updated correctly, FR-049 through FR-055 added in proper sequence, Technology Stack Reference Table formatted correctly with 13 component rows
- 📁 Files: Modified specs/001-physical-ai-textbook/spec.md (3 sections updated: FR-036 enhanced, FR-042 upgraded to MUST requirement, new Technology Stack & Frameworks section with 7 requirements + reference table added after Language Usage table)
- 🔁 Next prompts: Ready for `/sp.plan` to design Docusaurus project structure implementing these technology requirements, or `/sp.tasks` to break down implementation into actionable development tasks
- 🧠 Reflection: Technology choices align well with 2026 industry standards - TypeScript for infrastructure ensures maintainability, @docusaurus/theme-live-codeblock enables hands-on learning, Structurizr adds architectural clarity for complex robotics systems

## Evaluation notes (flywheel)

- Failure modes observed: None - all edits executed successfully on first attempt
- Graders run and results (PASS/FAIL): PASS - Verified by reading updated spec sections, all placeholders filled, no syntax errors, requirements properly numbered in sequence
- Prompt variant (if applicable): Standard implementation prompt with detailed plan
- Next experiment (smallest change to try): If expanding further, consider adding specific version constraints for plugins (@docusaurus/theme-live-codeblock@^3.x) or documenting minimum hardware requirements for running Docusaurus dev server
