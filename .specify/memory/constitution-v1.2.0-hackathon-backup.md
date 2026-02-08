# Physical AI & Humanoid Robotics Interactive Textbook Platform Constitution

<!--
Sync Impact Report:
- Version: 1.1.0 → 1.2.0
- Amendment Date: 2026-02-08
- Amendment Type: MAJOR (structural reorganization + universal principles)
- Changes:
  ✅ **BREAKING**: Added Section 0: Universal Principles (NEW - foundational layer)
  ✅ Added Section 0.1: Seven Foundational Principles (apply to ALL work)
  ✅ Added Section 0.2: Universal Decision Framework (standardized thresholds)
  ✅ Added Section 0.3: Hierarchy of Authority (conflict resolution rules)
  ✅ **BREAKING**: Consolidated testing standards (removed duplication from 3.1.VI and 5.3)
  ✅ Updated Section 8.2: Now AUTHORITATIVE testing source
  ✅ Added cross-references to principles in all major sections
  ✅ Fixed decision framework inconsistencies (30min/6h/2day thresholds standardized)
  ✅ Added Constitution Health Checklist (Section 16)
  ✅ Elevated implicit principles: Demo Reliability, Single-Threaded Focus, Human as Tool
- Rationale: Address structural issues identified in comprehensive review
- Breaking Changes: Section numbering shifted (old Section 1 → Section 1, but new Section 0 added)
- Migration Path: All references to principles now point to Section 0
- Follow-up TODOs: Priority 2 fixes (consolidate risks, merge quality gates) in v1.3.0
-->

---

## 0. UNIVERSAL PRINCIPLES

*These principles govern ALL work across the entire project. They override individual preferences, section-specific rules, and implementation details. When in doubt, return to these principles.*

### 0.1 Seven Foundational Principles

#### I. Demo Reliability Over Feature Completeness (NON-NEGOTIABLE)
**Rule**: If a feature cannot be demonstrated live without errors, it does not ship. A working subset is always better than a broken superset.

**Application**:
- Content: Publish 3 perfect modules > 5 mediocre modules
- Code: 5 test queries passing > 100 queries with 10% failure rate
- Features: Authentication working flawlessly > Auth + Personalization both buggy

**Litmus Test**: "Would I bet $100 this works during the demo without any failures?"

**Rationale**: Hackathon judges score based on working software. "90% complete" = 0 points.

---

#### II. Single-Threaded Focus (Solo Developer Constraint)
**Rule**: One task at a time until completion or explicit abandonment. No feature-hopping, no multitasking, no "just quickly checking" side tasks.

**Application**:
- Daily: Select ONE task in morning stand-up (Section 5.1.4)
- Weekly: Focus on ONE milestone (MVP-0, MVP-1, MVP-2, or MVP-3)
- Decision: If blocked on Task A, either unblock it OR abandon it via kill switch. Do NOT start Task B "while waiting"

**Litmus Test**: "Can I describe my current task in one sentence?"

**Rationale**: Context-switching is the #1 productivity killer for solo developers. Finishing 1 thing beats starting 5 things.

---

#### III. Incremental Validation (MVP Philosophy)
**Rule**: Every deliverable must be independently demo-able. Never have "90% complete" features. Each increment is a complete, working product.

**Application**:
- Content: Each module validated independently (Section 4.1.5) before next module starts
- Code: Each MVP (MVP-0, MVP-1, MVP-2, MVP-3) is a shippable product (Section 2.1.1)
- Testing: Test after each feature, not "at the end" (Section 8.2)

**Litmus Test**: "Can I show this to someone today and get useful feedback?"

**Rationale**: Early validation prevents building the wrong thing for weeks. Small failures are cheap; big failures are catastrophic.

---

#### IV. Progressive Enhancement (Static-First Architecture)
**Rule**: Core functionality MUST work without JavaScript, backend services, or authentication. Enhance progressively from a solid baseline.

**Application**:
- Content: Textbook readable without JS (Docusaurus SSG)
- Chatbot: Textbook still useful if chatbot fails (progressive enhancement)
- Auth: Platform usable anonymously; auth adds features but isn't required

**Litmus Test**: "Does this work if all external services fail right now?"

**Rationale**: Free-tier services (Render, Qdrant) can go down during demos. Static baseline = unbreakable demo.

---

#### V. Explicit Over Implicit (Zero Assumptions)
**Rule**: All decisions, assumptions, constraints, and dependencies MUST be documented. If it's not written down, it doesn't exist.

**Application**:
- Decisions: Every architectural decision → ADR (Section 11)
- Work: Every >1 hour task → PHR (Section 12.3)
- Constraints: Budget limits, time boxes, free-tier quotas → explicitly stated (Section 7)

**Litmus Test**: "Could someone else understand this decision 6 months from now without asking me?"

**Rationale**: Solo developer = no team to ask "why did we do it this way?" Documentation is future-you's only teammate.

---

#### VI. Constraint-Driven Development (Constraints as Features)
**Rule**: Treat constraints as design inputs, not limitations. Every constraint forces creative solutions that improve the product.

**Application**:
- Budget: $20 API limit → Forces caching (improves UX) + rate limiting (prevents abuse)
- Time: 4 weeks → Forces MVP thinking (prevents scope creep)
- Free-tier: Render spin-down → Forces static-first architecture (improves reliability)

**Litmus Test**: "Have I turned this constraint into a feature or just complained about it?"

**Rationale**: Constraints breed creativity. Unlimited resources breed bloat.

---

#### VII. Human as Tool (Escalation Protocol)
**Rule**: Invoke the user (human judgment) when facing ambiguity, uncertainty, architectural choices, or blockers. Humans are a specialized tool for decision-making.

**Triggers for Human Escalation**:
1. **Ambiguous Requirements**: User intent unclear → Ask 2-3 clarifying questions
2. **Unforeseen Dependencies**: Discovered new constraint → Surface it and ask for prioritization
3. **Architectural Uncertainty**: Multiple valid approaches with tradeoffs → Present options, get preference
4. **Blockers**: Stuck >30 min → Ask for help or authorization to abandon task

**Litmus Test**: "Am I making assumptions that only a human can validate?"

**Rationale**: AI should not make arbitrary decisions on ambiguous problems. Use human judgment as a tool.

---

### 0.2 Universal Decision Framework

This table standardizes decision thresholds across the entire project. If a section specifies a different threshold, it MUST justify why via ADR.

| Decision Type | Time Limit | Kill Switch Trigger | Authority | Notes |
|---------------|-----------|---------------------|-----------|-------|
| **Trivial Tool Integration** | 30 min debugging | Not working after 30 min | This constitution (Section 0.2) | Example: Linter setup, formatter config |
| **Core Feature Integration** | 6 hours debugging | Not working after 6 hours + ADR documenting failure | Section 3.2.1, 14.2 | Example: Better-Auth, OpenAI ChatKit |
| **Content Quality** | No time limit | >5 factual errors after validation | Section 4.1.5 | Quality never compromised for speed |
| **Schedule Slip** | 2 consecutive days | Activate contingency plan | Section 14.3 | Traffic light goes Red → escalate |
| **Budget Overrun** | $15 spent (out of $20) | Disable feature causing overrun | Section 7.2 | $18 = hard stop, $15 = warning |
| **Test Failures** | 3 consecutive failing builds | Roll back to last green build | Section 8.2 | Never ship broken builds |
| **Performance Degradation** | Response time >5s p95 | Optimize or disable feature | Section 8.3 | User experience non-negotiable |

**Conflict Resolution**: If this table conflicts with section-specific rules, this table wins UNLESS the section has an explicit ADR justifying deviation.

---

### 0.3 Hierarchy of Authority

When sections of this constitution conflict, apply this precedence order (highest authority first):

```
┌─────────────────────────────────────┐
│  1. UNIVERSAL PRINCIPLES (Section 0) │ ← NEVER override
│     - Seven Foundational Principles   │
│     - Universal Decision Framework    │
└─────────────────────────────────────┘
           ↓ overrides ↓
┌─────────────────────────────────────┐
│  2. CORE DELIVERABLES (Section 2.1)  │ ← MUST HAVE features
│     - Textbook (4 modules + capstone)│
│     - RAG Chatbot                     │
│     - Deployed site                   │
└─────────────────────────────────────┘
           ↓ overrides ↓
┌─────────────────────────────────────┐
│  3. MILESTONE GATES (Section 13)     │ ← Weekly success criteria
│     - MVP-0, MVP-1, MVP-2, MVP-3     │
│     - Go/No-Go decisions             │
└─────────────────────────────────────┘
           ↓ overrides ↓
┌─────────────────────────────────────┐
│  4. TECHNICAL GOVERNANCE (Section 3) │ ← Stack, principles, standards
│     - 6 Technical Principles         │
│     - Technology choices             │
└─────────────────────────────────────┘
           ↓ overrides ↓
┌─────────────────────────────────────┐
│  5. IMPLEMENTATION DETAILS (Sections │ ← Lowest priority
│     4-15: Content, Workflow, QA,     │
│     Risks, Resources, etc.)          │
└─────────────────────────────────────┘
```

**Conflict Resolution Rules**:
1. **Higher level wins**: If Section 0 conflicts with Section 8, Section 0 wins
2. **Later version wins**: If v1.2.0 conflicts with v1.1.0, v1.2.0 wins
3. **Explicit ADR wins**: If an ADR explicitly overrides constitution, ADR wins (but must document why)
4. **All conflicts MUST be documented**: Create ADR explaining resolution + update constitution

**Example Application**:
- Section 8.2 says "40% backend coverage", but Section 0.I says "Demo Reliability Over Completeness"
- Resolution: If achieving 40% coverage breaks the demo (e.g., time spent testing > time fixing bugs), Section 0.I wins
- Action: Create ADR-NNN documenting why coverage was reduced to 20% for this milestone

---

### 0.4 Constitution as Living Document

**Adaptation Principle**: This constitution is a TEMPLATE, not a rigid contract. It must evolve as we learn.

**When to Update**:
- **After each milestone** (Week 1, 2, 3, 4): Reflect on what worked/didn't work
- **When discovering new constraints**: External factors (API limits changed, service deprecated)
- **When external feedback challenges assumptions**: User testing reveals different priorities
- **When violating same principle >2 times**: Principle is wrong or unrealistic → amend it

**Amendment Process** (See Section Governance):
1. Create ADR documenting proposed change + rationale
2. Update constitution + increment version (MAJOR/MINOR/PATCH)
3. Update PHR documenting amendment
4. Communicate changes if team expands

**Amendment Speed**: For solo developer, amendments can be lightweight (15-30 min). Do NOT let process paralyze progress.

---

## Table of Contents

0. [Universal Principles](#0-universal-principles) ⭐ **START HERE**
1. [Executive Summary](#1-executive-summary)
2. [Project Scope](#2-project-scope)
3. [Technical Governance](#3-technical-governance)
4. [Content Governance](#4-content-governance)
5. [Development Workflow](#5-development-workflow)
6. [Risk Management](#6-risk-management)
7. [Resource Management](#7-resource-management)
8. [Quality Assurance](#8-quality-assurance) ⭐ **AUTHORITATIVE for Testing**
9. [Ethical Guidelines](#9-ethical-guidelines)
10. [Success Metrics](#10-success-metrics)
11. [Decision Log](#11-decision-log)
12. [Communication Standards](#12-communication-standards)
13. [Project Milestones](#13-project-milestones)
14. [Contingency Planning](#14-contingency-planning)
15. [Handoff & Maintenance](#15-handoff--maintenance)
16. [Constitution Health](#16-constitution-health) ⭐ **Weekly Review**

---

## 1. Executive Summary

**Governing Principles**: Section 0.1 (I, II, III, VI)
**Last Updated**: 2026-02-08 (Version 1.2.0)

**Project Name**: Physical AI & Humanoid Robotics Interactive Textbook Platform

**Mission**: Deliver a production-quality, university-level interactive textbook platform that educates users on Physical AI and Humanoid Robotics through AI-powered assistance, contextual learning, and evidence-based retrieval augmented generation (RAG).

**Timeline**: 4 weeks (2026-02-08 to 2026-03-08)

**Team Composition**: Solo developer with AI assistance (Claude Code, Spec-Kit Plus)

**Target Outcome**: 238-338 points in hackathon scoring (base 238, up to +100 bonus); deployment-ready platform with excellent user experience in core features.

**Core Philosophy**: Excellence in fundamentals over breadth of features. Every feature that ships must be polished, functional, and user-tested. Incomplete features do not ship. *(See Section 0.1.I: Demo Reliability Over Feature Completeness)*

**Authority**: This constitution is the single source of truth for all technical, content, and process decisions. All development activities, architectural decisions, and scope negotiations MUST reference this document. Deviations require explicit documentation via ADR (Architecture Decision Record). *(See Section 0.3: Hierarchy of Authority)*

### 1.1 Hackathon Requirements Breakdown

**Core Deliverables (Required for Base Score)**:

1. **AI/Spec-Driven Book Creation**
   - Docusaurus-based textbook on Physical AI & Humanoid Robotics
   - Written using Spec-Kit Plus and Claude Code
   - Deployed to GitHub Pages
   - Covers all 4 modules + capstone project content

2. **Integrated RAG Chatbot** (Embedded in the book)
   - **Technology Stack**:
     - OpenAI Agents/ChatKit SDKs - chat interface
     - FastAPI - backend API
     - Neon Serverless Postgres - database storage
     - Qdrant Cloud Free Tier - vector database for RAG
   - **Features Required**:
     - Answer questions about book content
     - Answer questions based on user-selected text only
     - Embedded within the published Docusaurus site

**Bonus Features (Up to 200 Extra Points Total)**:

3. **Claude Code Subagents & Agent Skills** (50 bonus points)
   - Create reusable intelligence via Claude Code Subagents and Agent Skills
   - Use these throughout the book project

4. **Authentication System** (50 bonus points)
   - Implement Signup/Signin using Better-Auth
   - Capture user background (software/hardware skill levels)
   - Use for content personalization

5. **Content Personalization** (50 bonus points)
   - Button at start of each chapter
   - Adjusts technical depth based on user background

6. **Urdu Translation** (50 bonus points)
   - Translation button at start of each chapter
   - Real-time AI-powered translation

**Submission Requirements**:
- Public GitHub Repository link
- Deployed Book (GitHub Pages) with all implemented features
- Demo Video (max 90 seconds)
- WhatsApp number (for presentation invitation)

---

## 2. Project Scope

**Governing Principles**: Section 0.1 (I, III, VI)
**Overrides**: None
**Superseded By**: None
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 2.1 MUST HAVE (Core Deliverables - Non-Negotiable)

*Governed by Principle I (Demo Reliability) and Principle III (Incremental Validation)*

#### Textbook Content
- **4 Complete Modules** covering:
  1. Introduction to Physical AI and Humanoid Robotics
  2. Core Technologies (sensors, actuators, control systems)
  3. AI Integration (perception, planning, learning)
  4. Real-World Applications
- **1 Capstone Module**: Integrated project showcasing concepts from all 4 modules
- **University-Level Quality**: Technical accuracy, citations, diagrams, code examples
- **Minimum Content Volume**: 40 pages equivalent (10 pages per module minimum)

#### Technical Platform
- **Deployed Docusaurus Site**: Accessible via GitHub Pages, responsive design, <3s page load
- **Functional RAG Chatbot**:
  - Embedded in every textbook page using OpenAI ChatKit SDK
  - Returns cited answers referencing textbook sections
  - Handles at minimum 5 question types (definition, how-to, comparison, troubleshooting, concept explanation)
  - Response time <5 seconds for 95% of queries
  - **Bonus Feature**: Answer questions based on user-selected text only
- **Backend API**: FastAPI service hosted on free-tier platform (Render/Railway)
  - `/api/v1/chat` endpoint with RAG integration
  - `/api/v1/chat/selection` endpoint for selected-text queries
  - `/api/health` endpoint for monitoring
- **Vector Database**: Qdrant Cloud integration with textbook content indexed
- **PostgreSQL Database**: Neon Serverless for chat history and usage tracking

#### Infrastructure
- **Continuous Deployment**: GitHub Actions CI/CD for frontend
- **Environment Configuration**: `.env` template with all required API keys documented
- **Monitoring**: Basic error logging and API usage tracking

### 2.1.1 Incremental Delivery Mandate

*Implements Principle III (Incremental Validation)*

**Critical Rule**: Each MVP must be independently deployable and demo-able. Never have "90% complete" features.

**MVP-0 (Day 7 - Week 1 Milestone)**:
- [ ] Docusaurus site deployed with landing page
- [ ] Module 1 published (Introduction to Physical AI)
- [ ] Chatbot working with Module 1 content ONLY
- [ ] Minimum 3 test queries answering correctly with citations
- [ ] Publicly accessible URL
- **Demo-able**: Can show judges a complete end-to-end flow for Module 1

**MVP-1 (Day 14 - Week 2 Milestone)**:
- [ ] Modules 1-2 published (Introduction + Core Technologies)
- [ ] Chatbot retrieves from both modules with citations
- [ ] Selected-text query feature functional
- [ ] Basic error handling (graceful degradation if backend down)
- [ ] 10 test queries passing
- **Demo-able**: Show multi-module retrieval + selected-text feature

**MVP-2 (Day 21 - Week 3 Milestone)**:
- [ ] Modules 1-3 published (Introduction + Core Technologies + AI Integration)
- [ ] Chatbot performance optimized (<3s p95 response time)
- [ ] Mobile responsive verified on real devices
- [ ] Integration testing complete
- **Demo-able**: Full textbook experience, optimized performance

**MVP-3 (Day 28 - Week 4 Milestone)**:
- [ ] Module 4 + capstone published (or gracefully degrade to "Coming Soon" stubs)
- [ ] At least 1 bonus feature implemented (preferably authentication)
- [ ] Demo video recorded (90 seconds)
- [ ] Submission materials prepared
- **Demo-able**: Production-ready platform with bonus features

**Rule**: If any MVP deadline is missed by >2 days, trigger contingency plan (Section 14.3). *(See Section 0.2: Universal Decision Framework - Schedule Slip)*

### 2.2 SHOULD HAVE (High-Value Bonus Features - 50 Points Each)

These features proceed ONLY if core deliverables are 100% complete and tested by end of Week 3.

#### 1. User Authentication (50 points)
- **Better-Auth Integration**: Social login (Google, GitHub) OR email/password
- **User Profiles**: Profile page capturing software/hardware background
- **Session Management**: Secure JWT tokens, refresh token flow
- **Minimum Viable Version**: Email/password signup + basic profile (no social login)
- **Go/No-Go Rule**: If authentication takes >6 hours to integrate, ship without it *(Section 0.2 authority)*

#### 2. Content Personalization (50 points)
- **Personalization Button**: At start of each chapter
- **Functionality**: Adjusts technical depth based on user background
- **Minimum Viable Version**: Static personalization presets (3 levels)
- **Go/No-Go Rule**: If personalization quality is poor (<80% user satisfaction), disable feature

### 2.3 COULD HAVE (Nice-to-Have Features - 50 Points Each)

These features proceed ONLY if all MUST and SHOULD features are complete AND >3 days remain before deadline.

#### 3. Urdu Translation (50 points)
- **Translation Button**: At start of each chapter
- **RTL Layout Support**: Docusaurus i18n configuration
- **Translated Content**: At least Module 1 fully translated
- **Go/No-Go Rule**: Skip if translation quality cannot be verified by native Urdu speaker

#### 4. Advanced Claude Code Integration (50 points)
- **Custom Subagents**: Domain-specific code generation
- **Agent Skills**: Custom Spec-Kit Plus commands
- **Go/No-Go Rule**: Skip if core development workflow is not yet stable

### 2.4 WON'T HAVE (Explicit Exclusions)

- Real-time collaboration features
- Video content hosting (link to external only)
- Mobile native applications
- Payment/subscription features
- Multi-tenancy or white-labeling
- Offline-first functionality
- Social features (comments, forums, upvoting)
- Gamification (badges, leaderboards)
- Advanced analytics dashboard

### 2.5 Competitive Positioning

| Competitor | What They Do | Our Differentiation |
|-----------|--------------|---------------------|
| **Traditional Textbooks** | Static content | ✅ AI chatbot with citations |
| **ChatGPT/Claude** | General AI, no citations | ✅ Citations to textbook sections (verifiable) |
| **Khan Academy** | Video-based learning | ✅ Text-based, searchable, faster |
| **Coursera/edX** | MOOC platforms, signup required | ✅ Free, open-access, no signup |
| **Other Hackathon Projects** | Generic chatbots | ✅ Domain-specific, university-level |

**Elevator Pitch** (30 seconds):
"Imagine a robotics textbook that answers your questions in real-time, WITH citations to the exact page. That's what we built. Students get ChatGPT-quality answers, but grounded in our curated university-level content. Try asking it: 'What sensors do humanoid robots use?'"

**Demo Hook**: Start demo by showing a bad ChatGPT answer (hallucinated citation), then show ours with real citation.

---

## 3. Technical Governance

**Governing Principles**: Section 0.1 (I, IV, V, VI)
**Overrides**: Implementation preferences
**Superseded By**: Section 0 (Universal Principles)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 3.1 Core Technical Principles

*These principles are specific to technical implementation. For universal principles, see Section 0.1.*

#### I. Cost-Consciousness (NON-NEGOTIABLE)
**Rules**:
- All infrastructure MUST use free tiers
- OpenAI API costs MUST NOT exceed $20 total budget
- Implement request rate limiting: 10 queries/minute per user
- Cache RAG responses for identical queries (24-hour TTL)
- Monitor API spend daily; halt feature development if >$15 spent

**Rationale**: Hackathon constraints and sustainability of free-tier demo.
**Governed By**: Section 0.1.VI (Constraint-Driven Development), Section 0.2 (Budget Overrun threshold)

#### II. Static-First Architecture
**Rules**:
- Frontend MUST be deployable as static files (GitHub Pages)
- Backend API MUST be optional for content viewing (progressive enhancement)
- Textbook content readable without JavaScript enabled
- All interactive features degrade gracefully when backend unavailable

**Rationale**: Reliability, cost, and scoring criteria for deployment simplicity.
**Governed By**: Section 0.1.IV (Progressive Enhancement)

#### III. API Contract Stability
**Rules**:
- Backend API versioned (e.g., `/api/v1/chat`)
- Breaking changes require new version endpoint
- Response schemas documented in OpenAPI spec
- Frontend MUST handle API errors gracefully (retry + fallback UI)

**Rationale**: Prevents deployment coupling issues and ensures demo resilience.
**Governed By**: Section 0.1.I (Demo Reliability)

#### IV. Security-First Development
**Rules**:
- No API keys in frontend code or Git history
- All secrets in `.env` file (`.gitignore` enforced)
- Input sanitization on all user-provided text (XSS prevention)
- SQL queries use parameterized statements (no string concatenation)
- CORS configured to allow only production domain

**Rationale**: Prevents credential leakage and common web vulnerabilities.
**Governed By**: Section 0.1.V (Explicit Over Implicit - document security decisions)

#### V. Solo-Optimized Tooling
**Rules**:
- Use managed services over self-hosted (Neon, Qdrant Cloud, Render)
- Automate repetitive tasks (linting, formatting, deployment)
- Prefer libraries with excellent documentation over "powerful" tools
- Maximum 30 minutes allowed for debugging any single third-party integration *(Section 0.2 authority)*

**Rationale**: Time is the scarcest resource; reduce operational overhead.
**Governed By**: Section 0.1.II (Single-Threaded Focus), Section 0.2 (Trivial Tool Integration threshold)

#### VI. Test Coverage for Critical Paths
**Rules** - *(Note: This section provides high-level principle only. For specific testing standards, see Section 8.2)*:
- RAG chatbot MUST have integration tests
- API endpoints MUST have unit tests
- Frontend MUST NOT crash on malformed API responses
- Pre-commit hooks prevent committing untested code

**Rationale**: Demo reliability under pressure; prevents last-minute failures.
**Governed By**: Section 0.1.I (Demo Reliability), **SUPERSEDED BY**: Section 8.2 for specific coverage targets

### 3.2 Technology Stack Standards

| Component | Technology | Justification | Alternatives Rejected |
|-----------|-----------|---------------|----------------------|
| Frontend Framework | Docusaurus 3.x | Built for documentation, MDX, SSG | Next.js (overkill), VitePress (less mature) |
| Backend Framework | FastAPI | Type-safe, async, auto OpenAPI docs | Flask (no async), Django (too heavy) |
| Database (Relational) | Neon Serverless Postgres | Free tier, no cold starts | Supabase (complex), SQLite (not cloud) |
| Vector Database | Qdrant Cloud | Free tier, Python SDK, good docs | Pinecone (paid), Weaviate (self-hosted) |
| AI Provider | OpenAI GPT-4o-mini | Cost-effective, reliable, streaming | Claude (expensive), local models (infra) |
| Chatbot SDK | OpenAI ChatKit | Official SDK, well-documented | Custom UI (time-consuming) |
| Authentication | Better-Auth | Modern, framework-agnostic | Auth0 (paid), NextAuth (Next.js only) |
| Hosting (Frontend) | GitHub Pages | Free, auto-deployment, CDN | Vercel (overkill), Netlify (quota limits) |
| Hosting (Backend) | Render Free Tier | Persistent storage, simple setup | Railway (complex), Heroku (deprecated) |

### 3.2.1 Technology Stack Decision Review (Day 3 Checkpoint)

*Implements Section 0.2 (Universal Decision Framework - Core Feature Integration)*

**Mandatory Review Questions** (End of Day 3):
- [ ] Did I spend >2 hours debugging any single integration? *(Approaching Section 0.2 threshold)*
- [ ] Do I have working end-to-end flow (frontend → API → database)?
- [ ] Can I deploy changes in <10 minutes?
- [ ] Are all services (Neon, Qdrant, Render) provisioned and tested?

**Simplification Triggers** *(Section 0.2 authority - 6 hour limit for core integrations)*:
- **If FastAPI + Render taking >6 hours** → Consider Next.js API routes (single deployment)
- **If Qdrant + Neon complex** → Consider Supabase (unified platform with vector support)
- **If Better-Auth blocking progress** → Ship without auth (Section 0.2: 6-hour kill switch)
- **If OpenAI ChatKit integration difficult** → Build custom React chatbot component (2-3h)

**Trade-off**: Simpler stack = less resume flex, but higher completion probability. Prioritize shipping over learning new tools. *(Section 0.1.I: Demo Reliability)*

**Decision Log**: Document any stack changes in ADR with justification. *(Section 0.1.V: Explicit Over Implicit)*

### 3.3 Code Quality Standards

#### File Structure Requirements
```
frontend/                # Docusaurus site
├── docs/               # Textbook modules (MDX)
├── src/
│   ├── components/     # React components (Chatbot, Auth UI)
│   ├── css/           # Custom styles
│   └── pages/         # Landing, profile pages
└── docusaurus.config.js

backend/                # FastAPI service
├── app/
│   ├── api/
│   │   └── v1/        # API v1 endpoints
│   │       ├── chat.py
│   │       └── health.py
│   ├── core/          # Config, dependencies
│   ├── models/        # Pydantic schemas
│   ├── services/      # RAG, auth logic
│   └── main.py
├── tests/             # Pytest tests
└── requirements.txt

.specify/              # Spec-Kit Plus artifacts
├── memory/
│   └── constitution.md
├── templates/
└── scripts/

specs/                 # Feature specifications
history/               # ADRs and PHRs
```

#### Naming Conventions
- **Files**: `kebab-case.tsx`, `snake_case.py`
- **Components**: `PascalCase` (React), `snake_case` (Python)
- **Functions**: `camelCase` (TypeScript), `snake_case` (Python)
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Git Branches**: `feature/<name>`, `fix/<name>`, `docs/<name>`

#### Documentation Requirements (MUST)
- Every API endpoint: Docstring with example request/response
- Every React component: JSDoc with props description
- Every Python service: Module docstring + type hints
- README files: Root + frontend + backend (setup instructions)

*Governed By*: Section 0.1.V (Explicit Over Implicit)

#### Linting and Formatting
- **TypeScript**: ESLint + Prettier (pre-commit hook)
- **Python**: Black + isort + mypy (pre-commit hook)
- **Commit Messages**: Conventional Commits format (`feat:`, `fix:`, `docs:`)

---

## 4. Content Governance

**Governing Principles**: Section 0.1 (I, III, V)
**Overrides**: None
**Superseded By**: Section 0 (Universal Principles)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 4.1 Textbook Content Standards

#### Academic Rigor
- **Accuracy**: All technical claims MUST be verifiable from authoritative sources
- **Citations**: Minimum 3 citations per module (academic papers, manufacturer docs, textbooks)
- **Review**: Each module reviewed for technical correctness before integration

*Governed By*: Section 0.1.V (Explicit Over Implicit - cite sources), Section 0.1.III (Incremental Validation)

#### Accessibility
- **Reading Level**: Undergraduate sophomore level (assume linear algebra, basic physics)
- **Definitions**: All jargon defined on first use with inline tooltips
- **Visual Aids**: Minimum 2 diagrams per module (architectural diagrams, flowcharts)
- **Code Examples**: Minimum 1 runnable code snippet per module (Python preferred)

#### Structure
- **Module Length**: 8-12 pages per module (A4 equivalent)
- **Sections**: Introduction, Key Concepts, Technical Deep Dive, Applications, Summary
- **Learning Objectives**: 3-5 specific, measurable objectives per module
- **Self-Assessment**: 5 review questions at end of each module

### 4.1.5 Content Quality Gates (Pre-Publication Checklist)

*Implements Section 0.1.III (Incremental Validation) and Section 0.2 (Content Quality threshold)*

**Per-Module Validation (30 min mandatory, non-negotiable)**:
- [ ] **Citation Check**: All citations resolve to real papers/docs (use Google Scholar)
- [ ] **Formula Verification**: Run code examples; verify math with Wolfram Alpha or manual calculation
- [ ] **Recency Check**: Confirm information is post-2022 (avoid outdated robotics data)
- [ ] **Diagram Accuracy**: Cross-check architectural diagrams against official specs (e.g., ROS documentation)
- [ ] **Readability Test**: Read aloud; if you stumble, users will too (fix awkward phrasing)
- [ ] **Jargon Audit**: All technical terms defined on first use

**External Validation (Optional but Recommended)**:
- [ ] Post Module 1 draft on Reddit r/robotics → Get feedback in 24 hours
- [ ] Run through ChatGPT as "technical reviewer" → Prompt: "Review this for factual errors"
- [ ] Grammarly Premium check → Fix passive voice and clarity issues
- [ ] Send to 1 external reader (friend, colleague) → Get fresh-eyes feedback

**Kill Switch** *(Section 0.2 authority)*: If a module fails validation with >5 factual errors or >10 clarity issues, use placeholder content and mark "Draft - Coming Soon." Do NOT publish broken content.

**Time Allocation**: 30 minutes per module for validation = 2.5 hours total for 5 modules.

*Governed By*: Section 0.1.I (Demo Reliability - quality over completeness)

### 4.2 Chatbot Response Standards

#### Response Quality (MUST)
- **Citation Required**: Every factual claim MUST link to textbook section or external source
- **Accuracy Threshold**: 95% factual accuracy verified via test question set
- **Fallback Behavior**: "I don't have enough context to answer accurately. Please refer to [Module X, Section Y](#link)."
- **No Hallucinations**: If retrieval fails, admit limitation rather than guess

*Governed By*: Section 0.1.I (Demo Reliability), Section 0.1.V (Explicit - cite sources)

#### Response Format
- **Max Length**: 300 words per response
- **Markdown Formatting**: Bullet points, bold for key terms, inline code blocks
- **Citation Format**: `[Source: Module 2, Section 3.1](#link)` or `[IEEE Paper Title](URL)`
- **Tone**: Friendly but professional, avoids condescension

#### Safety Guardrails
- **Out-of-Scope Queries**: Redirect to textbook ("This platform focuses on Physical AI. For general robotics, see...")
- **Prohibited Content**: No medical advice, no dangerous instructions, no homework answers (encourage exploration)

### 4.3 Content Generation Workflow

1. **Outline Creation**: Define learning objectives and section structure (use Claude/GPT-4 for brainstorming)
2. **Draft**: Generate via AI-assisted writing (GPT-4, Claude) with human review and editing
3. **Technical Review**: Verify accuracy of formulas, code, and claims (use Section 4.1.5 checklist)
4. **Indexing**: Add to RAG system (chunk, embed, upload to Qdrant) and test chatbot retrieval
5. **User Testing**: 1-2 test readers per module (developer + external volunteer if available)
6. **Publication**: Deploy after all checks pass

*Implements*: Section 0.1.III (Incremental Validation - validate each module independently)

### 4.4 Content Update Policy

- **Minor Corrections**: Fix typos, update links (no approval needed)
- **Technical Updates**: Algorithm explanations, code examples (requires review with Section 4.1.5 checklist)
- **Major Revisions**: Structural changes, new sections (requires ADR per Section 0.1.V)

---

## 5. Development Workflow

**Governing Principles**: Section 0.1 (II, III, VII)
**Overrides**: None
**Superseded By**: Section 0 (Universal Principles)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 5.1 Daily Workflow (Solo Developer)

*Implements Section 0.1.II (Single-Threaded Focus)*

#### Morning Routine (30 min)
1. Review task board (GitHub Projects or `tasks.md`)
2. Check API spend dashboard (OpenAI usage page)
3. Pull latest changes (if using multiple machines)
4. Run full test suite (verify nothing broke overnight)

#### Development Cycle (90-min blocks)
1. Select ONE task from current milestone *(Section 0.1.II: Single-Threaded Focus)*
2. Write/update tests (if applicable)
3. Implement feature
4. Run tests + manual verification
5. Commit with conventional message
6. Update PHR if >1 hour work *(Section 0.1.V: Explicit Over Implicit)*

#### Evening Routine (15 min)
1. Push all changes to remote
2. Update milestone progress (check off completed items)
3. Document blockers or decisions in ADR (if applicable)

### 5.1.4 Daily Stand-Up (Solo Edition)

*Implements Section 0.1.II (Single-Threaded Focus) and Section 0.1.VII (Human as Tool)*

**Morning Reflection (5 min)**:
- What did I complete yesterday that moved me closer to current MVP?
- What is the ONE task I must complete today? *(Section 0.1.II: Single-Threaded Focus)*
- What is blocking me? *(If >30 min debugging, escalate per Section 0.1.VII or Section 0.2)*

**Evening Reflection (5 min)**:
- Did I complete my ONE task? If no, why not?
- Am I on track for this week's milestone? (Green/Yellow/Red)
- What can I defer to lower priority?

**Weekly Check-In (Sundays, 15 min)**:
- **Traffic Light Status**:
  - 🟢 Green: On track, no blockers
  - 🟡 Yellow: 1-2 days behind, manageable with extra effort
  - 🔴 Red: >2 days behind, activate contingency plan *(Section 0.2: Schedule Slip trigger)*

**Logging**: Keep a simple log in `docs/dev-log.md` with daily status updates (30-second entries).

### 5.2 Git Workflow

#### Branch Strategy
- **Main Branch**: `main` (production-ready, deployed to GitHub Pages)
- **Development Branch**: `develop` (integration branch)
- **Feature Branches**: `feature/<name>` (short-lived, merge to `develop`)

#### Commit Standards
- **Conventional Commits**: `type(scope): description`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
  - Example: `feat(chatbot): add citation links to RAG responses`
- **Atomic Commits**: One logical change per commit *(Section 0.1.II: Single-Threaded Focus)*
- **Squash on Merge**: Feature branches squashed before merging

#### Deployment Triggers
- **Frontend**: Any push to `main` triggers GitHub Pages rebuild
- **Backend**: Manual deployment to Render (no auto-deploy to prevent accidents)

### 5.3 Testing Strategy

**(DEPRECATED - Consolidated into Section 8.2)**

**Note**: This section previously contained testing standards. All testing guidance has been consolidated into **Section 8.2 (Quality Assurance)** to eliminate duplication and conflicts.

**See Section 8.2 for authoritative testing standards** including:
- Coverage targets (40% backend, 20% frontend)
- Critical path testing requirements
- Test execution workflow

*This consolidation resolves conflicts identified in constitution review.*

### 5.4 Code Review (Solo Context)

#### Pre-Commit Checklist
- [ ] Code passes all linters and formatters
- [ ] Tests written and passing (if critical path - see Section 8.2)
- [ ] No hardcoded secrets or TODOs
- [ ] Changes aligned with current milestone *(Section 0.1.II: Single-Threaded Focus)*
- [ ] Documentation updated (if API/component changed - Section 0.1.V)

#### Pre-Merge Checklist (feature → develop)
- [ ] Feature complete per acceptance criteria
- [ ] Manual testing in local environment
- [ ] No console errors or warnings
- [ ] Git history clean (no "WIP" or "fix" commits in sequence)

---

## 6. Risk Management

**Governing Principles**: Section 0.1 (I, VI, VII)
**Overrides**: None
**Superseded By**: Section 0 (Universal Principles)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 6.1 Technical Risks

*Governed by Section 0.2 (Universal Decision Framework)*

| Risk | Probability | Impact | Mitigation Strategy | Kill Switch | Authority |
|------|------------|--------|---------------------|-------------|-----------|
| **OpenAI API cost overrun** | High | High | Rate limiting, caching, daily monitoring | Disable chatbot if >$18 spent | Section 0.2 |
| **Qdrant free tier limits** | Medium | High | Limit textbook size, optimize embeddings | Fallback to keyword search (PostgreSQL full-text) | Section 14.2 |
| **Render free tier downtime** | Medium | Medium | Static fallback UI, status page | Accept degraded UX, mention in demo | Section 0.1.IV |
| **GitHub Pages build failure** | Low | High | Local build verification, backup Netlify deploy | Manual deployment to Netlify | Section 14.2 |
| **Auth integration complexity** | Medium | Low | MVP = email/password only, defer social login | Ship without auth (6h limit) | Section 0.2 |
| **Better-Auth setup issues** | High | Low | 30-min debugging limit | Skip auth entirely | Section 0.2 |

### 6.2 Schedule Risks

#### Critical Path Dependencies
1. **Week 1 (Day 1-7)**: Docusaurus setup + Module 1 content + Backend scaffold
2. **Week 2 (Day 8-14)**: Backend API + RAG integration + Modules 2-3
3. **Week 3 (Day 15-21)**: Module 4 + Capstone + Integration testing
4. **Week 4 (Day 22-28)**: Polish + bonus features + demo video

#### Risk: Content Creation Bottleneck
- **Trigger**: <50% content complete by end of Week 2 (i.e., <3 modules done)
- **Response**: Reduce module scope to 3 modules + smaller capstone
- **Fallback**: Use placeholder content for Modules 3-4 (clearly marked "Coming Soon")

*Governed By*: Section 0.1.I (Demo Reliability - ship working subset)

#### Risk: Integration Hell
- **Trigger**: Frontend-backend integration not working by Day 18
- **Response**: Freeze feature development, focus on integration debugging (allocate 8 hours)
- **Escalation**: Remove chatbot from demo, showcase textbook-only (still viable for 150+ points)

*Governed By*: Section 0.2 (Schedule Slip - 2 day trigger)

### 6.3 Quality Risks

#### Risk: Chatbot Hallucinations
- **Detection**: Test with 20 adversarial questions (create list in Week 2)
- **Acceptance**: <5% hallucination rate (i.e., <1 out of 20 queries returns wrong answer)
- **Mitigation**: Strengthen retrieval confidence thresholds, add "I don't know" responses
- **Fallback**: Disable chatbot, label as "beta feature"

*Governed By*: Section 0.1.I (Demo Reliability - broken chatbot does not ship)

#### Risk: Mobile UX Degradation
- **Detection**: Manual testing on iPhone/Android by Day 20
- **Acceptance**: Chatbot usable, textbook readable (no horizontal scroll)
- **Mitigation**: Responsive CSS audit (use Chrome DevTools)
- **Fallback**: Add "Best viewed on desktop" notice

### 6.4 Hackathon-Specific Risks

#### Risk: Demo Day Technical Failure
**Probability**: Medium (WiFi issues, laptop problems common at hackathons)

**Mitigation**:
- Record full demo video as backup (play video if live demo fails)
- Pre-load site on local server (works offline - Section 0.1.IV: Progressive Enhancement)
- Bring second laptop with full setup
- Test on venue WiFi 1 hour before demo
- Run Render wake-up script 10 minutes before demo (avoid cold start)

**Kill Switch**: If live demo impossible, present video + architecture walkthrough

#### Risk: Scope Creep During Demo Q&A
**Trigger**: Judges ask "Why didn't you implement feature X?"

**Response Script**:
"Great question! X was deprioritized because [technical reason / time constraint]. Our focus was [core value prop: RAG with citations]. X is documented in our roadmap for post-hackathon."

**Never Say**: "We ran out of time" or "We didn't think of that" (sounds unprepared)

*Governed By*: Section 0.1.I (Demo Reliability - polished subset > broken superset)

#### Risk: Developer Burnout (Week 3)
**Detection**: Missing daily commits, skipping morning routine, feeling exhausted

**Mitigation**:
- Mandatory 1 full day off per week (documented in schedule)
- If falling behind: Cut Module 4 + Capstone to "Coming Soon" stubs
- Avoid all-nighters (degrades decision-making quality)
- Take 15-min walks every 2 hours (improves focus)

**Escalation**: Reduce scope to 3 modules + chatbot MVP (still 180+ points achievable)

*Governed By*: Section 0.1.II (Single-Threaded Focus requires rest)

### 6.5 Pre-Mortem: What Could Cause Total Failure?

**Exercise**: Imagine it's March 8th and you scored <150 points. What went wrong?

**Most Likely Failure Modes**:
1. **Chatbot Returns Garbage Answers** (50% probability)
   - Cause: Embedding quality poor, retrieval tuning skipped
   - Prevention: Allocate 6 hours in Week 2 for retrieval tuning ONLY (test queries, adjust chunk size, tune similarity thresholds)

2. **Content is Mediocre "AI Slop"** (40% probability)
   - Cause: Relied too heavily on GPT-4 without human review
   - Prevention: Every module must pass "Can I defend this to a robotics professor?" test (Section 4.1.5)

3. **Demo Day: Nothing Works** (30% probability)
   - Cause: Render free tier spun down, cold start took too long
   - Prevention: Run wake-up script 10 minutes before demo + have backup video

4. **Scope Creep: 80% Complete on Everything, 100% on Nothing** (60% probability)
   - Cause: Tried to implement auth + personalization + translation + subagents
   - Prevention: This constitution's MUST/SHOULD/COULD gates + MVP checkpoints prevent this

**Action**: Review this pre-mortem at end of Week 1 and Week 2. Adjust strategy if any failure mode is becoming real.

*Governed By*: Section 0.1.III (Incremental Validation - catch problems early)

---

## 7. Resource Management

**Governing Principles**: Section 0.1 (II, VI)
**Overrides**: None
**Superseded By**: Section 0 (Universal Principles)
**Related ADRs**: ADR-001 (Content time allocation rationale)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 7.1 Time Budget (4 weeks = 160 hours) - AUTHORITATIVE

*Implements Section 0.1.VI (Constraint-Driven Development - 160h constraint)*

**Critical Change**: Content creation is the primary deliverable. Increased from 31% to 44% of total time.

| Activity | Total Hours | % of Total | Week 1 | Week 2 | Week 3 | Week 4 | Rationale |
|----------|-------------|-----------|--------|--------|--------|--------|-----------|
| **Content Creation** | **70** | **44%** | 20 (M1) | 22 (M2-3) | 16 (M4+Cap) | 12 (Review) | **Primary deliverable; 40 pages cannot be rushed** |
| Backend Development | 25 | 16% | 10 | 12 | 2 | 1 | Use FastAPI templates, minimize custom logic |
| Frontend Development | 20 | 13% | 6 | 4 | 8 | 2 | Docusaurus defaults + minimal customization |
| Testing & QA | 15 | 9% | 1 | 2 | 6 | 6 | Focus on integration tests (Section 8.2) |
| Deployment & DevOps | 8 | 5% | 2 | 2 | 2 | 2 | Use CI/CD templates |
| Demo Video | 6 | 4% | 0 | 0 | 2 | 4 | Record while implementing |
| Buffer | 16 | 10% | 4 | 4 | 4 | 4 | Content revisions + debugging |
| **TOTAL** | **160** | **100%** | 40 | 40 | 40 | 40 | |

**Reference This Table**: All milestone hours (Section 13.2) link back to this authoritative breakdown.

*Governed By*: Section 0.1.II (Single-Threaded Focus - allocate time to one activity at a time)

### 7.2 Financial Budget

*Governed by Section 0.2 (Budget Overrun threshold: $15)*

| Service | Free Tier Limit | Expected Usage | Cost |
|---------|----------------|----------------|------|
| OpenAI API (ChatKit + API) | Pay-as-go | ~50K tokens (dev + demo) | $15-20 |
| Qdrant Cloud | 1GB / 1M vectors | ~10K vectors (textbook) | $0 |
| Neon Postgres | 0.5GB / 1 project | Chat history (~1K rows) | $0 |
| Render | 750 hours/month | 1 service (continuous) | $0 |
| GitHub Pages | Unlimited (soft 100GB/month) | ~50MB site | $0 |
| **Total** | | | **$15-20** |

#### Cost Control Measures
- Cache OpenAI responses for 24 hours (PostgreSQL JSON column)
- Use GPT-4o-mini instead of GPT-4 ($0.15 vs $5 per 1M input tokens)
- Implement aggressive rate limiting (10 queries/minute per user)
- Limit chatbot response length to 300 words max

*Implements*: Section 0.1.VI (Constraint-Driven Development - $20 constraint becomes caching feature)

### 7.3 Infrastructure Limits

#### Render Free Tier Constraints
- **Spin-down after 15 min inactivity**: Accept cold start delay (10-30s)
- **512MB RAM**: Sufficient for FastAPI + minimal caching
- **Mitigation**: Wake-up endpoint in demo script

*Implements*: Section 0.1.IV (Progressive Enhancement - static baseline unaffected by backend spin-down)

#### GitHub Pages Constraints
- **1GB repository size**: Limit images to <100KB each (optimize with TinyPNG)
- **100GB bandwidth/month**: Sufficient for demo traffic
- **No server-side logic**: All dynamic features require external API

---

## 8. Quality Assurance ⭐ AUTHORITATIVE

**Governing Principles**: Section 0.1 (I, III)
**Overrides**: All other testing guidance (Sections 3.1.VI, 5.3 deprecated)
**Superseded By**: Section 0 (Universal Principles)
**Last Updated**: 2026-02-08 (Version 1.2.0) - **This section is the SINGLE SOURCE OF TRUTH for all testing standards**

*This section consolidates all testing standards to eliminate duplication. References to testing in other sections point here.*

### 8.1 Definition of Done (Feature-Level)

*Implements Section 0.1.III (Incremental Validation)*

A feature is DONE when ALL criteria are met:

- [ ] Acceptance criteria from spec met 100%
- [ ] Code passes all linters and type checks
- [ ] Unit tests written and passing (see Section 8.2 for coverage targets)
- [ ] Integration tests passing (if applicable - see Section 8.2)
- [ ] Manual testing completed on target devices (desktop + mobile)
- [ ] Documentation updated (API docs, README, component docs - Section 0.1.V)
- [ ] No `console.log` or debug statements in committed code
- [ ] Code reviewed (self-review checklist in Section 5.4)
- [ ] Deployed to staging environment and smoke tested
- [ ] PHR created documenting implementation (if >1 hour work - Section 0.1.V)

*Governed By*: Section 0.1.I (Demo Reliability - DONE = demo-able without errors)

### 8.2 Testing Standards (Solo-Optimized) - AUTHORITATIVE

**(This section supersedes Section 3.1.VI and Section 5.3)**

**Philosophy**: Focus on demo reliability, not coverage metrics. *(Section 0.1.I authority)*

#### Critical Path Testing ONLY (MUST)
Focus testing effort on:
1. **RAG Retrieval**: 5 hardcoded test queries with expected citations
2. **API Error Handling**: Chatbot gracefully handles backend downtime
3. **Mobile Rendering**: Manual test on 1 real device (your phone)

#### Deprioritized Testing:
- Unit tests for pure functions (SHOULD - if time allows)
- Authentication flows (COULD - skip if no auth)
- Cross-browser compatibility (COULD - Chrome only is acceptable)
- E2E tests with Playwright/Cypress (WON'T - too time-consuming)

#### Coverage Targets (Realistic for Solo Developer)
- **Backend**: >40% (focus on RAG service and `/api/v1/chat` endpoint only)
- **Frontend**: >20% (focus on Chatbot component only)
- **Integration**: 5 test queries passing with citations = sufficient

**Rationale**: 5 working test queries demonstrated live during demo > 70% test coverage with buggy features. *(Section 0.1.I: Demo Reliability)*

#### Test Execution Workflow
- **Pre-Commit**: Linters only (skip tests if >5s)
- **Pre-Push**: Fast unit tests only (<30s)
- **Pre-Deploy**: Manual smoke test (open site, ask 3 chatbot questions, verify citations)

*Governed By*: Section 0.2 (Test Failures - 3 consecutive failures → roll back)

#### Unit Test Requirements (Minimal Examples)

```python
# Example: Python backend - ONLY test critical RAG logic
def test_rag_retrieval_returns_relevant_chunks():
    """Test that RAG returns chunks matching query keywords."""
    query = "What are the main components of a humanoid robot?"
    results = rag_service.retrieve(query, top_k=3)

    assert len(results) == 3
    assert any("actuator" in r.text.lower() for r in results)
    assert all(r.score > 0.5 for r in results)
```

```typescript
// Example: React component - ONLY test error handling
test('Chatbot displays error message when API fails', async () => {
  server.use(
    http.post('/api/v1/chat', () => HttpResponse.error())
  );

  render(<Chatbot />);
  await userEvent.type(screen.getByRole('textbox'), 'test query');
  await userEvent.click(screen.getByText('Send'));

  expect(await screen.findByText(/unable to connect/i)).toBeInTheDocument();
});
```

#### Integration Test Requirements
- **API Tests**: Use FastAPI TestClient, in-memory SQLite for tests
- **Frontend Tests**: React Testing Library + MSW (Mock Service Worker) for API mocking
- **E2E Tests**: Manual only (no Playwright/Cypress due to time constraints)

#### Manual Testing Checklist (Pre-Deploy) - CRITICAL
- [ ] Chatbot responds to 5 test queries correctly (citations present and clickable)
- [ ] Authentication flow works (sign up, log in, log out) - if implemented
- [ ] Textbook loads on Chrome (primary), Firefox (optional), Safari (optional)
- [ ] Mobile responsive on 1 real device (your phone) - verify no horizontal scroll
- [ ] All internal links functional (no 404s)
- [ ] Footer displays correct copyright and version
- [ ] Backend `/health` endpoint returns 200 status

### 8.3 Performance Standards

*Governed by Section 0.2 (Performance Degradation threshold: >5s p95)*

| Metric | Target | Measurement Method | Fallback | Authority |
|--------|--------|-------------------|----------|-----------|
| Page Load Time | <3s (desktop) | Lighthouse CI or manual stopwatch | Optimize images, lazy load chatbot | Section 0.2 |
| Chatbot Response | <5s (p95) | Backend logging | Reduce embedding size, cache aggressively | Section 0.2 |
| API Uptime | >95% during demo | Render status page | Static fallback UI | Section 0.1.IV |
| Mobile Lighthouse Score | >80 | Manual audit | Accept >60 if functionality works | |

### 8.4 Accessibility Standards

**Minimum Compliance**: WCAG 2.1 Level A (hackathon minimum)

- [ ] All images have alt text
- [ ] Color contrast ratio >4.5:1 for body text
- [ ] Keyboard navigation works (chatbot, menu)
- [ ] Screen reader tested (macOS VoiceOver minimum) - optional
- [ ] Focus indicators visible

**Defer to Post-Hackathon**: Level AA compliance, full ARIA labels

---

## 9. Ethical Guidelines

**Governing Principles**: Section 0.1 (V)
**Overrides**: None
**Superseded By**: Section 0 (Universal Principles)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 9.1 Content Ethics

#### Academic Integrity
- **No Plagiarism**: All content original or properly attributed
- **Citation Standards**: IEEE or ACM format for academic papers
- **License Compliance**: Images and diagrams use CC-BY or public domain only

*Governed By*: Section 0.1.V (Explicit Over Implicit - cite all sources)

#### Bias Mitigation
- **Inclusive Examples**: Use diverse names, avoid stereotypes
- **Neutral Language**: "users" not "guys," "they" for singular
- **Global Perspective**: Include non-Western robotics research examples (e.g., Chinese humanoid robots)

### 9.2 AI Usage Ethics

#### Transparency
- **AI-Generated Content**: Watermark AI-generated diagrams (e.g., DALL-E, Midjourney)
- **Chatbot Disclaimer**: "Powered by OpenAI. Responses may contain errors. Verify with textbook citations."
- **Prompt Engineering**: Document system prompts in codebase (for reproducibility)

*Governed By*: Section 0.1.V (Explicit Over Implicit)

#### Data Privacy
- **User Data**: Chat history stored only with consent (opt-in banner)
- **Anonymization**: No PII in logs; hash user IDs for analytics
- **Data Retention**: Chat history deleted after 30 days (automated job)

### 9.3 Open Source Compliance

#### Licensing
- **Project License**: MIT (permissive, allows commercial use)
- **Dependency Auditing**: Check all npm/pip packages for compatible licenses
- **Attribution**: `NOTICE.md` file lists all third-party libraries

#### Contribution Policy
- **Post-Hackathon**: Add `CONTRIBUTING.md` with code style guide
- **Issue Templates**: Bug report, feature request (GitHub templates)

---

## 10. Success Metrics

**Governing Principles**: Section 0.1 (I)
**Overrides**: None
**Superseded By**: Section 0 (Universal Principles)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 10.1 Hackathon Scoring Alignment

| Category | Max Points | Target Points | Key Deliverables |
|----------|-----------|---------------|------------------|
| **Functionality** | 80 | 70 | Textbook + RAG chatbot working |
| **AI Integration** | 60 | 55 | RAG with citations, OpenAI ChatKit SDK |
| **UX/Design** | 40 | 35 | Docusaurus polish, responsive design |
| **Innovation** | 30 | 20 | Interactive learning with cited answers |
| **Code Quality** | 30 | 20 | Tests for critical paths, clean Git history |
| **Deployment** | 20 | 20 | Live URL, no errors during demo |
| **Presentation** | 20 | 18 | Clear 90-sec video |
| **Bonus Features** | 200 | 50-100 | 1-2 bonus features (auth + personalization) |
| **Total Base** | 280 | 238 | Without bonus features |
| **Total with Bonus** | 480 | 288-338 | With 1-2 bonus features |

### 10.1.1 Judging Reality Check

**What Judges Actually Score Heavily**:

1. **Live Demo Quality** (30% of total score)
   - Does it work without errors during demo? *(Section 0.1.I: Demo Reliability)*
   - Can judges interact with it themselves?
   - **Current Plan**: ✅ MVP-0 through MVP-3 ensure always demo-able

2. **Problem-Solution Fit** (25% of total score)
   - Does the chatbot actually help users learn?
   - Are citations accurate and useful?
   - **Current Plan**: ⚠️ Add user testing in Week 2 (2 external testers minimum)

3. **Technical Impressiveness** (20% of total score)
   - RAG with citations is impressive ✅
   - University-level content is differentiated ✅
   - **Current Plan**: ✅ Well-positioned

4. **Presentation Quality** (15% of total score)
   - Storytelling > feature list
   - **Current Plan**: ⚠️ Add demo script template in Week 3

5. **Code Quality** (10% of total score)
   - Judges rarely review code deeply in hackathons
   - **Current Plan**: Focus on clean README + deployment instructions

### 10.2 User Experience Metrics (Post-Launch)

- **Chatbot Engagement**: >40% of page visitors interact with chatbot
- **Citation Click-Through**: >10% of chatbot responses result in citation clicks
- **Content Completion**: >30% of users read 2+ modules (via scroll depth analytics)
- **Error Rate**: <2% of chatbot queries return errors

### 10.3 Technical Health Metrics

- **Test Coverage**: >40% for backend, >20% for frontend (Section 8.2 authority)
- **Lighthouse Score**: >85 performance, >80 accessibility, >90 best practices
- **Zero Critical Bugs**: No showstoppers in production
- **API Latency**: p95 <5s for chatbot, p50 <2s

---

## 11. Decision Log (ADR Template)

**Governing Principles**: Section 0.1 (V)
**Overrides**: None
**Superseded By**: Section 0.3 (Hierarchy of Authority - explicit ADRs can override constitution)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 11.1 Architecture Decision Record (ADR) Format

*Implements Section 0.1.V (Explicit Over Implicit)*

Use this template for all significant architectural decisions:

```markdown
# ADR-XXX: [Decision Title]

**Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-YYY]
**Date**: YYYY-MM-DD
**Deciders**: [Names or roles]
**Context**: [Describe the problem requiring a decision]
**Governing Principle**: Section 0.1.[I-VII] that applies

## Decision
[State the decision clearly]

## Options Considered
1. **Option A**: [Description]
   - Pros: [Bullet list]
   - Cons: [Bullet list]
2. **Option B**: [Description]
   - Pros: [Bullet list]
   - Cons: [Bullet list]

## Rationale
[Explain why this option was chosen over alternatives]

## Consequences
- **Positive**: [Expected benefits]
- **Negative**: [Expected drawbacks or technical debt]
- **Neutral**: [Trade-offs or side effects]

## Compliance
- [ ] Aligns with Constitution Section 0.1 principles
- [ ] Tested or validated
- [ ] Documented in relevant specs
- [ ] Does NOT violate Section 0.2 (Universal Decision Framework)
```

### 11.2 ADR Triggers (When to Create an ADR)

Create an ADR when ALL three conditions are met:
1. **Impact**: Decision has long-term consequences (affects architecture, data model, security)
2. **Alternatives**: Multiple viable options exist with significant trade-offs
3. **Scope**: Decision is cross-cutting (affects multiple modules or future features)

**Examples**:
- ✅ Choice of vector database (Qdrant vs Pinecone vs Weaviate)
- ✅ Authentication strategy (JWT vs session cookies vs OAuth-only vs skip auth)
- ✅ RAG retrieval algorithm (semantic search vs hybrid search vs keyword)
- ✅ Stack simplification decision (FastAPI + Render vs Next.js API routes)
- ✅ **Constitution override** (deviating from Section 0.2 thresholds)
- ❌ Button color choice (trivial, no architectural impact)
- ❌ Variable naming convention (codified in style guide)

### 11.3 ADR Storage and Versioning

- **Location**: `history/adr/`
- **Naming**: `ADR-NNN-short-decision-title.md` (NNN = zero-padded sequential number)
- **Linking**: Reference ADRs in specs, tasks, and PHRs
- **Updates**: If decision is superseded, update status and add superseding ADR link

---

## 12. Communication Standards

**Governing Principles**: Section 0.1 (V)
**Overrides**: None
**Superseded By**: Section 0 (Universal Principles)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 12.1 Documentation Requirements

*Implements Section 0.1.V (Explicit Over Implicit)*

#### README Files (MUST)
- **Root README**: Project overview, setup instructions, demo link, tech stack table
- **Frontend README**: Local development (`npm start`), build commands, environment variables
- **Backend README**: API documentation link (`/docs`), database setup, testing commands

#### API Documentation
- **OpenAPI Spec**: Auto-generated from FastAPI (available at `/docs`)
- **Response Examples**: Include in docstrings
- **Error Codes**: Document all HTTP status codes and error formats

#### Code Comments
- **When Required**:
  - Complex algorithms (e.g., RAG retrieval logic, embedding generation)
  - Non-obvious business logic
  - Workarounds or hacks (with explanation of why and link to issue/ADR)
- **When NOT Required**:
  - Self-explanatory code (good naming is better than comments)
  - Type signatures (redundant with TypeScript/Python type hints)

### 12.2 Commit Message Standards

**Format**: `<type>(<scope>): <description>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no functional change)
- `refactor`: Code restructuring (no functional change)
- `test`: Adding or updating tests
- `chore`: Build config, dependencies, tooling

**Examples**:
- `feat(chatbot): add citation links to RAG responses`
- `fix(auth): resolve token refresh infinite loop`
- `docs(readme): add deployment instructions for Render`
- `test(api): add integration tests for chat endpoint`

### 12.3 Prompt History Records (PHR)

*Implements Section 0.1.V (Explicit Over Implicit)*

**Purpose**: Document all user prompts and AI responses for learning and traceability.

**When to Create**:
- After every `/sp.*` command execution
- After significant implementation work (>1 hour)
- After debugging sessions that resolved critical issues
- After architectural discussions or spec changes

**Storage**:
- Constitution-related: `history/prompts/constitution/`
- Feature-specific: `history/prompts/<feature-name>/`
- General: `history/prompts/general/`

**Required Fields** (per template):
- ID, Title, Stage, Date, Model, Feature, Branch, User, Command
- Prompt text (verbatim), Response summary
- Files modified, Tests added, Outcome evaluation

---

## 13. Project Milestones

**Governing Principles**: Section 0.1 (I, III)
**Overrides**: Individual task priorities
**Superseded By**: Section 0 (Universal Principles), Section 2.1 (MUST HAVE)
**Related**: Section 7.1 (Time Budget - authoritative hours source)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 13.1 Timeline Overview

*Implements Section 0.1.III (Incremental Validation via MVP gates)*

| Week | Focus | Deliverables | Success Gate | Hours |
|------|-------|--------------|-------------|-------|
| **Week 1** (Feb 8-14) | Foundation + MVP-0 | Docusaurus + Module 1 + Backend scaffold | MVP-0: Demo-able Module 1 + chatbot | 40h |
| **Week 2** (Feb 15-21) | Core Features + MVP-1 | RAG integration + Modules 2-3 | MVP-1: Multi-module retrieval working | 40h |
| **Week 3** (Feb 22-28) | Content Complete + MVP-2 | Module 4 + Capstone + Testing | MVP-2: All content + performance optimized | 40h |
| **Week 4** (Mar 1-7) | Polish + MVP-3 | Bonus features + Video + Deployment | MVP-3: Demo-ready with 1+ bonus features | 40h |

### 13.2 Detailed Milestone Breakdown

*Note: Hours reference Section 7.1 (Time Budget) as single source of truth*

#### Milestone 1: Foundation + MVP-0 (Week 1 - 40 hours)

**Deliverables**:
- [ ] Docusaurus project initialized with custom theme (6h) *[Section 7.1: Frontend]*
- [ ] GitHub Pages deployment pipeline functional (2h) *[Section 7.1: DevOps]*
- [ ] Backend FastAPI project scaffolded (4h) *[Section 7.1: Backend]*
- [ ] Neon Postgres database provisioned with schema (2h) *[Section 7.1: Backend]*
- [ ] Qdrant Cloud vector database configured (2h) *[Section 7.1: Backend]*
- [ ] **Module 1 content written** (20h) *[Section 7.1: Content]* ⭐ **PRIMARY FOCUS**
- [ ] Module 1 indexed in Qdrant (2h) *[Section 7.1: Backend]*
- [ ] Landing page with project overview (1h) *[Section 7.1: Frontend]*
- [ ] Chatbot component embedded (4h) *[Section 7.1: Frontend]*
- [ ] 3 test queries passing with citations (1h) *[Section 7.1: Testing]*
- [ ] Environment setup documentation (1h) *[Section 7.1: Frontend]*

**Success Criteria (MVP-0)** *(Section 0.1.I: Demo Reliability)*:
- [ ] Site accessible at `<username>.github.io/<repo-name>`
- [ ] Backend `/health` endpoint returns 200 status
- [ ] Module 1 readable on mobile and desktop (responsive)
- [ ] Chatbot answers 3 test queries correctly with citations to Module 1
- [ ] **Demo-able**: Can show judges end-to-end flow for Module 1

**Blockers If Not Met** *(Section 0.2 authority)*:
- Deployment issues: Switch to Netlify backup plan (1 hour max debugging)
- Content delay: Use AI-generated placeholder content (mark as draft, must replace by Week 2)
- Chatbot integration issues: Fallback to simple text input (no ChatKit SDK)

#### Milestone 2: Core Integration + MVP-1 (Week 2 - 40 hours)

**Deliverables**:
- [ ] RAG pipeline optimized (6h) *[Section 7.1: Backend]*
- [ ] `/api/v1/chat` endpoint functional (4h) *[Section 7.1: Backend]*
- [ ] `/api/v1/chat/selection` endpoint (2h) *[Section 7.1: Backend]*
- [ ] Citation links functional (2h) *[Section 7.1: Frontend]*
- [ ] **Modules 2-3 published** (22h) *[Section 7.1: Content]* ⭐ **PRIMARY FOCUS**
- [ ] Modules 2-3 indexed in Qdrant (4h) *[Section 7.1: Backend]*
- [ ] Integration tests for RAG endpoint (2h) *[Section 7.1: Testing]*
- [ ] API error handling and rate limiting (2h) *[Section 7.1: Frontend]*
- [ ] Frontend gracefully handles backend downtime (2h) *[Section 7.1: Frontend]*

**Success Criteria (MVP-1)**:
- [ ] 10 sample queries answered correctly with citations (from all modules)
- [ ] Response time <5 seconds for all test queries *(Section 8.3 authority)*
- [ ] No API errors in 20 consecutive queries
- [ ] Selected-text query feature functional
- [ ] **Demo-able**: Show multi-module retrieval + selected-text feature

**Blockers If Not Met**:
- RAG quality issues: Spend 6 hours tuning retrieval parameters
- API cost overrun: Implement aggressive caching *(Section 7.2)*
- Integration issues: Activate Section 14.3 contingency plan

#### Milestone 3: Content Complete + MVP-2 (Week 3 - 40 hours)

**Deliverables**:
- [ ] **Module 4 published** (8h) *[Section 7.1: Content]*
- [ ] **Capstone module published** (8h) *[Section 7.1: Content]*
- [ ] All modules reviewed for accuracy (4h) *[Section 4.1.5 checklist]*
- [ ] Module 4 + Capstone indexed in Qdrant (2h) *[Section 7.1: Backend]*
- [ ] Full integration testing (20 test queries) (2h) *[Section 7.1: Testing]*
- [ ] Mobile UX audit and fixes (4h) *[Section 7.1: Frontend]*
- [ ] Performance optimization (4h) *[Section 7.1: Frontend]*
- [ ] Demo video script written (2h) *[Section 7.1: Video]*
- [ ] External user testing (4h) *[Section 7.1: Testing]*

**Success Criteria (MVP-2)**:
- [ ] All acceptance criteria from Week 1-2 still met
- [ ] Test coverage >40% backend, >20% frontend *(Section 8.2 authority)*
- [ ] Lighthouse scores >80 *(Section 8.3)*
- [ ] No critical bugs in issue tracker
- [ ] **Demo-able**: Full textbook experience + optimized performance

**Blockers If Not Met**:
- Content incomplete: Reduce capstone scope to simple tutorial (2-3 pages)
- Performance issues: Accept lower scores if functionality works *(Section 0.1.I: Demo Reliability wins)*
- Testing incomplete: Skip coverage metrics, focus on manual smoke tests

#### Milestone 4: Polish + MVP-3 (Week 4 - 40 hours)

**Deliverables**:
- [ ] Content review and final edits (12h) *[Section 7.1: Content]*
- [ ] At least 1 SHOULD HAVE feature (16h) *[Section 7.1: Backend/Frontend]* (auth OR personalization)
- [ ] Demo video recorded (90 seconds) (4h) *[Section 7.1: Video]*
- [ ] Final deployment to production (2h) *[Section 7.1: DevOps]*
- [ ] Submission materials prepared (2h) *[Section 7.1: DevOps]*
- [ ] Post-demo fixes (2h) *[Section 7.1: Buffer]*
- [ ] Buffer for unexpected issues (2h) *[Section 7.1: Buffer]*

**Success Criteria (MVP-3)**:
- [ ] Demo video clearly shows all MUST HAVE features
- [ ] At least 1 bonus feature functional (50 points)
- [ ] Production site has zero console errors
- [ ] API monitoring shows >95% uptime during demo period
- [ ] All submission requirements met per hackathon rules
- [ ] **Demo-ready**: Can confidently present to judges

**Contingency**:
- If bonus features incomplete: Ship without them (base score still 238 points) *(Section 0.1.I authority)*
- If video quality low: Prioritize clear audio over fancy editing
- If auth blocking: Skip auth, focus on content quality + chatbot reliability *(Section 0.2: 6-hour kill switch)*

---

## 14. Contingency Planning

**Governing Principles**: Section 0.1 (I, VI)
**Overrides**: None
**Superseded By**: Section 0 (Universal Principles)
**Related**: Section 0.2 (Universal Decision Framework)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 14.1 Feature Cut Priority (If Time Runs Short)

*Implements Section 0.1.I (Demo Reliability - polished subset > broken superset)*

**Priority 1 (NEVER CUT)**:
1. Textbook Modules 1-3 (minimum content to claim "university-level textbook")
2. Deployed Docusaurus site
3. RAG chatbot with 5 working test queries

**Priority 2 (CUT IF NEEDED - Week 3+)**:
4. Module 4 (replace with shorter "Coming Soon" page)
5. Capstone module (replace with external resource links)
6. Selected-text query feature (nice-to-have, not critical)

**Priority 3 (CUT IF NEEDED - Week 4)**:
7. Authentication (accept anonymous usage only)
8. Content personalization
9. Urdu translation
10. Advanced Claude Code integrations (subagents/skills)

### 14.2 Technical Failure Scenarios

*Governed by Section 0.2 (Universal Decision Framework)*

#### Scenario: Qdrant Free Tier Exceeded
- **Detection**: Error "Quota exceeded" from Qdrant API or >1GB storage used
- **Response**:
  1. Reduce vector dimensions (768 → 384) - reindex all content
  2. Implement chunking strategy (only embed summary paragraphs, not full text)
  3. If still exceeded: Switch to keyword search (PostgreSQL full-text search with `tsvector`)

#### Scenario: OpenAI API Cost Exceeds Budget
- **Detection**: Daily cost monitoring shows >$15 spent *(Section 0.2 threshold)*
- **Response**:
  1. Disable chatbot for general public usage
  2. Enable only for demo queries (whitelist 20 hardcoded test questions)
  3. Add banner: "Chatbot temporarily limited for cost management"
  4. For judges: Provide demo video showing chatbot working

#### Scenario: Render Backend Unavailable During Demo
- **Detection**: `/health` endpoint returns 5xx or times out
- **Response**:
  1. Trigger manual wake-up endpoint 10 minutes before demo
  2. If still down after 5 minutes: Show static fallback UI *(Section 0.1.IV: Progressive Enhancement)*
  3. Emphasize textbook content quality in demo narration
  4. Play backup demo video showing chatbot working

#### Scenario: GitHub Pages Deployment Fails
- **Detection**: Build action fails or site shows 404
- **Response**:
  1. Check build logs for Docusaurus errors (common: broken MDX syntax, missing imports)
  2. If unfixable in <1 hour: Deploy to Netlify backup (drag-and-drop `build/` folder)
  3. Update submission link to Netlify URL
  4. Document deployment issue in README (transparency++)

#### Scenario: Better-Auth Integration Blocking Progress
- **Detection**: >6 hours spent on auth integration without working login flow *(Section 0.2 threshold)*
- **Response**:
  1. Immediately abandon Better-Auth *(Section 0.2: 6-hour kill switch)*
  2. Ship without authentication (anonymous usage)
  3. Focus remaining time on content quality + chatbot reliability
  4. Rationale: 238 base points > 200 points with broken auth *(Section 0.1.I authority)*

### 14.3 Schedule Slip Mitigation

*Governed by Section 0.2 (Schedule Slip: 2 consecutive days)*

#### Trigger: >2 days behind schedule at any milestone
**Actions**:
1. **Triage**: Identify must-fix vs nice-to-have tasks (use MUST/SHOULD/COULD framework - Section 2)
2. **Scope Reduction**: Move non-critical features to "Future Work" section in README
3. **Time Reallocation**: Reduce buffer time from future weeks, work extra 2 hours/day
4. **Help Request**: Post in hackathon Discord for quick debugging help (set 30-min time limit)

*Implements*: Section 0.1.VII (Human as Tool - escalate when blocked)

#### Trigger: Milestone 2 (MVP-1) not met by Day 14
**Escalation**:
- Abandon all SHOULD HAVE features (auth, personalization)
- Focus 100% on MUST HAVE deliverables (textbook + chatbot)
- Accept technical debt (document in ADR for post-hackathon cleanup)
- Target: 180-200 base points (still respectable)

*Implements*: Section 0.3 (Hierarchy - MUST HAVE overrides SHOULD HAVE)

#### Trigger: Developer Burnout (detected Week 3)
**Actions**:
- Mandatory 1 full day off (do NOT work)
- Reduce Module 4 + Capstone to "Coming Soon" stubs
- Ship 3 modules + chatbot (160-180 points, but sustainable)
- Document lessons learned in PHR for future projects

*Implements*: Section 0.1.II (Single-Threaded Focus requires rest to maintain)

---

## 15. Handoff & Maintenance

**Governing Principles**: Section 0.1 (V)
**Overrides**: None
**Superseded By**: Section 0 (Universal Principles)
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 15.1 Deployment Documentation

#### Production Environment
- **Frontend URL**: `https://<username>.github.io/<repo-name>` (or custom domain)
- **Backend URL**: `https://<app-name>.onrender.com`
- **Admin Access**: GitHub repository settings → Pages
- **Monitoring**: Render dashboard for logs and uptime

#### Environment Variables (`.env`)
```bash
# Backend (.env)
DATABASE_URL=postgresql://...          # Neon Postgres connection string
QDRANT_URL=https://...                 # Qdrant Cloud endpoint
QDRANT_API_KEY=***                     # Qdrant API key
OPENAI_API_KEY=sk-***                  # OpenAI API key (for ChatGPT + ChatKit)
BETTER_AUTH_SECRET=***                 # Better-Auth secret (if auth implemented)
CORS_ORIGINS=https://<frontend-url>    # Frontend URL for CORS

# Frontend (Docusaurus config or .env)
BACKEND_API_URL=https://<backend-url>  # Backend API base URL
```

#### Deployment Commands
```bash
# Frontend (GitHub Pages)
cd frontend
npm run build          # Build static site
git push origin main   # Triggers auto-deploy via GitHub Actions

# Backend (Render - manual deploy)
cd backend
git push render main   # Or use Render dashboard "Deploy Latest Commit"
```

#### Wake-Up Script (For Demo Day)
```bash
# Run 10 minutes before demo to wake up Render backend
curl https://<app-name>.onrender.com/health
```

### 15.2 Maintenance Runbook

#### Daily Checks (During Hackathon Period)
- [ ] Check Render backend status (uptime dashboard at render.com)
- [ ] Review OpenAI API spend (https://platform.openai.com/usage) *(Section 7.2)*
- [ ] Test chatbot with 1 sample query (verify citations work)

#### Weekly Checks (Post-Hackathon)
- [ ] Review error logs (Render logs for 5xx errors)
- [ ] Audit database size (Neon dashboard - ensure <500MB)
- [ ] Check Qdrant vector count (ensure not approaching 1M vectors)

#### Monthly Maintenance
- [ ] Update npm dependencies (`npm outdated`, `npm update`)
- [ ] Update Python dependencies (`pip list --outdated`, `pip install -U`)
- [ ] Rotate Better-Auth secrets (if auth implemented)
- [ ] Clean up old chat history (>30 days) - run cleanup script

### 15.3 Known Limitations & Future Work

#### Technical Debt (To Address Post-Hackathon)
- **No Automated E2E Tests**: Add Playwright for critical flows (chatbot, auth if implemented)
- **Limited Error Recovery**: Improve retry logic for API failures (exponential backoff)
- **Hardcoded Embeddings**: Implement incremental embedding updates (don't re-embed all content on changes)
- **No A/B Testing**: Add feature flags for personalization experiments

#### Feature Roadmap (Community-Driven, Post-Hackathon)
1. **Interactive Simulations**: Embed robotics simulations (Unity WebGL, Gazebo Web)
2. **Instructor Dashboard**: Analytics for educators (page views, chatbot usage, student progress)
3. **Community Forum**: Q&A platform integrated with chatbot (Stack Overflow-style)
4. **Offline Mode**: PWA with service worker for textbook caching (works offline)
5. **Multi-Language Support**: Expand beyond Urdu (Arabic, Spanish, Chinese, etc.)

### 15.4 Handoff Checklist (If Transferring Ownership)

- [ ] Repository access granted (GitHub collaborator or org transfer)
- [ ] Environment variables documented in secure password manager (1Password, LastPass)
- [ ] Admin access shared for:
  - [ ] Render account (or API key for deployment)
  - [ ] Neon database (connection string + admin panel access)
  - [ ] Qdrant Cloud (API key + cluster URL)
  - [ ] OpenAI account (API key or separate project)
- [ ] Walkthrough video recorded (architecture overview + deployment demo) - 15 minutes
- [ ] Known issues documented in GitHub Issues (with priority labels)
- [ ] Contact information for original developer archived in README

---

## 16. Constitution Health ⭐ WEEKLY REVIEW

**Governing Principles**: Section 0.4 (Constitution as Living Document)
**Overrides**: None
**Superseded By**: None
**Last Updated**: 2026-02-08 (Version 1.2.0)

### 16.1 Weekly Constitution Review (Sundays, 5 minutes)

*Implements Section 0.4 (Adaptation Principle)*

**Every Sunday (5 minutes)**:
- [ ] Did I reference the constitution when making decisions this week?
- [ ] Did I discover any contradictions or gaps? (Document in ADR)
- [ ] Are time budgets still realistic? (Update Section 7.1 if >20% variance)
- [ ] Are principles being followed or just documented? (Honest assessment)
- [ ] Did I invoke Section 0.1.VII (Human as Tool) when stuck, or did I waste time?

**Trigger Amendment If**:
- Found >3 contradictions in one week → Schedule constitution review session
- Violated same principle >2 times → Principle is wrong or unrealistic, amend it
- External feedback challenges core assumptions → Update assumptions + document in ADR
- Time budgets off by >20% for 2 consecutive weeks → Revise Section 7.1

### 16.2 Constitution Effectiveness Metrics

**Track Weekly** (2 min):
- **Adherence Rate**: % of decisions that referenced constitution (target: >80%)
- **Principle Violations**: Count of principle violations (target: <3 per week)
- **Time Accuracy**: Actual vs planned hours per activity (target: within 20%)
- **MVP Success**: Did we meet this week's MVP gate? (Green/Yellow/Red)

**If Metrics Degrade**:
- Yellow (1 metric off target): Reflect in evening stand-up, adjust next week
- Red (2+ metrics off target): Schedule 30-min constitution review session, create ADR

### 16.3 Amendment Log (Track All Changes)

| Version | Date | Type | Key Changes | Rationale |
|---------|------|------|-------------|-----------|
| 1.0.0 | 2026-02-08 | NEW | Initial ratification | Baseline governance |
| 1.1.0 | 2026-02-08 | MINOR | Expert recommendations integrated | Time budget +70h content, MVP strategy, risk analysis |
| 1.2.0 | 2026-02-08 | **MAJOR** | Universal Principles added (Section 0), testing consolidated, hierarchy of authority | Structural reorganization for consistency |

---

## Governance

### Amendment Procedure

1. **Proposal**: Create ADR documenting proposed change + rationale
2. **Justification**: Explain why amendment necessary (new constraint, lesson learned, expert feedback)
3. **Impact Analysis**: List affected specs, tasks, or code modules
4. **Approval**: Solo developer decision (or team vote if expanded post-hackathon)
5. **Implementation**: Update constitution + increment version (MAJOR/MINOR/PATCH)
6. **Propagation**: Update dependent templates and notify stakeholders (if team expands)

### Version Control

**Current Version**: 1.2.0 (Second major amendment)

**Version History**:
- 1.0.0 (2026-02-08): Initial ratification
- 1.1.0 (2026-02-08): Expert recommendations, MVP strategy, time reallocation (content: 50h→70h), testing revised (40%/20%)
- **1.2.0 (2026-02-08)**: **BREAKING** - Section 0 (Universal Principles) added, testing consolidated (single source: Section 8.2), hierarchy of authority, cross-references added

**Versioning Rules**:
- **MAJOR**: Backward-incompatible changes (removed principles, scope reductions, fundamental philosophy changes, structural reorganization)
- **MINOR**: New principles, sections, or expanded guidance (additive changes)
- **PATCH**: Clarifications, typo fixes, formatting improvements

### Compliance

- All development work MUST reference this constitution *(Section 0.1.V: Explicit Over Implicit)*
- Deviations require explicit ADR justification *(Section 0.3: Hierarchy of Authority)*
- PHRs MUST document adherence to principles *(Section 12.3)*
- Weekly review: Are we following our own rules? *(Section 16)*

**Version**: 1.2.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08

---

**End of Constitution**

*This document is the single source of truth for all project decisions. When in doubt, return to Section 0: Universal Principles.*

*Excellence in fundamentals > breadth of features. Ship working software.* *(Section 0.1.I)*
