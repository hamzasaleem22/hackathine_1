# Project Constitution - Usage Guide

This directory contains project governance documents (constitutions) that define principles, decision frameworks, and quality standards for development.

## Available Constitutions

### 1. `constitution.md` (v2.0.0 - General Framework) - **RECOMMENDED FOR NEW PROJECTS**

**Type**: Universal project governance framework (~680 lines)

**Use When**:
- Starting a new software project (web app, CLI tool, mobile app, library)
- Need high-level governance principles without project-specific constraints
- Solo developer or small team seeking actionable decision frameworks
- Want to adapt principles to your specific domain

**Contains**:
- 7 Universal Principles (Demo Reliability, Single-Threaded Focus, Incremental Validation, etc.)
- Resource Management Framework (time budgets, cost management patterns)
- Risk Management Framework (kill switches, contingency planning, pre-mortem exercises)
- Quality Assurance Framework (testing philosophy, performance standards, code quality)
- Governance (ADRs, development journals, communication standards)

**Does NOT contain**:
- Technology stack prescriptions
- Project-specific timelines or budgets
- Domain-specific requirements
- Hackathon scoring criteria

---

### 2. `constitution-v1.2.0-hackathon-backup.md` (Archived) - **FOR REFERENCE ONLY**

**Type**: Hackathon-specific constitution (1,790 lines)

**Use When**:
- You want concrete examples of how to apply general principles to a specific project
- Building a Physical AI/Robotics educational platform (the original project)
- Need detailed examples of time budgets, tech stack decisions, and milestone planning

**Contains**:
- All general principles PLUS:
- Specific tech stack (Docusaurus, FastAPI, Qdrant, Neon Postgres, Better-Auth)
- 4-week timeline with 160-hour budget breakdown
- Hackathon scoring alignment (238-338 points)
- Content governance for educational textbook
- MVP gates (MVP-0, MVP-1, MVP-2, MVP-3) with specific deliverables

**Warning**: This is a snapshot of a specific project. Do NOT copy it verbatim for other projects.

---

## How to Use

### For New Projects

1. **Start with `constitution.md` (v2.0.0)**:
   - Read Section 0 (Universal Principles) first
   - Adapt resource allocation percentages to your project size
   - Define your own risk assessment table (Section 2.1)
   - Set project-specific performance targets (Section 3.3)

2. **Customize for Your Domain**:
   - Add project-specific sections (e.g., "Content Governance" for educational platforms)
   - Document deviations in ADRs (Architecture Decision Records)
   - Update version to v2.1.0 (MINOR change for additions)

3. **Review Weekly** (Section 4.4):
   - Are principles being followed?
   - Are time budgets accurate?
   - Are there contradictions or gaps?

### For Adapting Existing Projects

1. **Read Both Constitutions**:
   - v2.0.0 for principles
   - v1.2.0 for concrete examples of application

2. **Extract Relevant Patterns**:
   - Time budget allocation patterns → adapt percentages
   - Risk assessment examples → adapt to your risks
   - Testing philosophy → critical path focus

3. **Document Adaptations**:
   - Create ADRs for significant decisions
   - Update your constitution version appropriately

---

## Constitution Evolution

### v2.0.0 (2026-02-08) - Current
- **BREAKING**: Generalized from hackathon-specific to universal
- Removed all project/tech-specific content
- Optimized for solo developers
- ~680 lines (down from 1,790)

### v1.2.0 (2026-02-08) - Archived
- Hackathon-specific (Physical AI textbook platform)
- Added Universal Principles (Section 0)
- Consolidated testing standards

### v1.1.0 (2026-02-08)
- Expert recommendations integrated
- Time budget reallocation (content: 50h → 70h)

### v1.0.0 (2026-02-08)
- Initial ratification

---

## Quick Reference

| I need... | Use this file |
|-----------|---------------|
| Governance principles for any project | `constitution.md` |
| Example of detailed time budgeting | `constitution-v1.2.0-hackathon-backup.md` (Section 7.1) |
| Risk management templates | `constitution.md` (Section 2) |
| Testing philosophy | `constitution.md` (Section 3.2) |
| ADR format | `constitution.md` (Section 4.1) |
| Specific tech stack decisions | `constitution-v1.2.0-hackathon-backup.md` (Section 3.2) |

---

## Questions?

- **"Which version should I use?"** → Start with `constitution.md` (v2.0.0)
- **"Can I modify the constitution?"** → Yes! See Section 4.4 (Amendment Process)
- **"How often should I review it?"** → Weekly (5 minutes), see Section 4.4
- **"What if I violate a principle?"** → Document why in an ADR, consider amendment if violating >2 times

---

**Last Updated**: 2026-02-08
