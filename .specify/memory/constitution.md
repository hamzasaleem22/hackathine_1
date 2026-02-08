# General Project Constitution (v2.0.0)

<!--
Version History:
- v2.0.0 (2026-02-08): **BREAKING** - Generalized from hackathon-specific to universal framework
  - Removed: Project-specific content (Physical AI textbook, hackathon scoring, MVP gates, tech stack prescriptions)
  - Preserved: Universal principles, decision frameworks, resource/risk/quality patterns
  - Optimized: Solo developer workflows, constraint-driven development
  - Target: ~500 lines of actionable governance principles
- v1.2.0 (2026-02-08): Hackathon-specific constitution (1,790 lines) - see constitution-v1.2.0-hackathon-backup.md
-->

> **About This Constitution**: This is a general framework for software project governance. It provides decision-making principles, resource management patterns, and quality standards applicable to any software project (web apps, CLI tools, mobile apps, libraries). For concrete examples in a specific domain, see `constitution-v1.2.0-hackathon-backup.md`.

---

## Table of Contents

0. [Universal Principles](#0-universal-principles) ⭐ **START HERE**
1. [Resource Management Framework](#1-resource-management-framework)
2. [Risk Management Framework](#2-risk-management-framework)
3. [Quality Assurance Framework](#3-quality-assurance-framework)
4. [Governance](#4-governance)

---

## 0. UNIVERSAL PRINCIPLES

*These principles govern ALL work across the entire project. They override individual preferences, implementation details, and tactical decisions. When in doubt, return to these principles.*

### 0.1 Seven Foundational Principles

#### I. Demo Reliability Over Feature Completeness (NON-NEGOTIABLE)
**Rule**: If a feature cannot be demonstrated live without errors, it does not ship. A working subset is always better than a broken superset.

**Application**:
- Deliverables: Ship 3 polished features > 5 buggy features
- Code: 5 test cases passing > 100 tests with 10% failure rate
- Features: Authentication working flawlessly > Auth + Notifications both buggy

**Litmus Test**: "Would I confidently demo this feature to a stakeholder right now without any failures?"

**Rationale**: Stakeholders and users evaluate based on working software. "90% complete" delivers zero value.

---

#### II. Single-Threaded Focus (Solo Developer Constraint)
**Rule**: One task at a time until completion or explicit abandonment. No feature-hopping, no multitasking, no "just quickly checking" side tasks.

**Application**:
- Daily: Select ONE task in morning planning
- Weekly: Focus on ONE milestone or feature
- Decision: If blocked on Task A, either unblock it OR abandon it via kill switch. Do NOT start Task B "while waiting"

**Litmus Test**: "Can I describe my current task in one sentence?"

**Rationale**: Context-switching is the #1 productivity killer for solo developers. Finishing 1 thing beats starting 5 things.

---

#### III. Incremental Validation (MVP Philosophy)
**Rule**: Every deliverable must be independently demo-able. Never have "90% complete" features. Each increment is a complete, working product.

**Application**:
- Features: Each feature validated independently before next feature starts
- Releases: Each release is a shippable product (MVP-0, MVP-1, MVP-2 gates)
- Testing: Test after each feature, not "at the end"

**Litmus Test**: "Can I show this to someone today and get useful feedback?"

**Rationale**: Early validation prevents building the wrong thing for weeks. Small failures are cheap; big failures are catastrophic.

---

#### IV. Progressive Enhancement (Static-First Architecture)
**Rule**: Core functionality MUST work without complex dependencies. Enhance progressively from a solid baseline.

**Application**:
- Architecture: Static-first where applicable (SSG over SSR when possible)
- Features: Platform usable with basic functionality; advanced features add value but aren't required
- External Services: Degrade gracefully when third-party services fail

**Litmus Test**: "Does this work if all external services fail right now?"

**Rationale**: Free-tier services and third-party dependencies can fail during demos or production. Solid baseline = resilient system.

---

#### V. Explicit Over Implicit (Zero Assumptions)
**Rule**: All decisions, assumptions, constraints, and dependencies MUST be documented. If it's not written down, it doesn't exist.

**Application**:
- Decisions: Every architectural decision → ADR (Architecture Decision Record)
- Work: Significant tasks (>1 hour) → Development Journal entry
- Constraints: Budget limits, time boxes, API quotas → explicitly stated

**Litmus Test**: "Could someone else understand this decision 6 months from now without asking me?"

**Rationale**: Solo developer = no team to ask "why did we do it this way?" Documentation is future-you's only teammate.

---

#### VI. Constraint-Driven Development (Constraints as Features)
**Rule**: Treat constraints as design inputs, not limitations. Every constraint forces creative solutions that improve the product.

**Application**:
- Budget: API cost limits → Forces caching (improves UX) + rate limiting (prevents abuse)
- Time: Fixed deadlines → Forces MVP thinking (prevents scope creep)
- Infrastructure: Free-tier limitations → Forces efficient architecture (improves reliability)

**Litmus Test**: "Have I turned this constraint into a feature or just complained about it?"

**Rationale**: Constraints breed creativity. Unlimited resources breed bloat.

---

#### VII. Human as Tool (Escalation Protocol)
**Rule**: Invoke human judgment when facing ambiguity, uncertainty, architectural choices, or blockers. Humans are a specialized tool for decision-making.

**Triggers for Human Escalation**:
1. **Ambiguous Requirements**: User intent unclear → Ask 2-3 clarifying questions
2. **Unforeseen Dependencies**: Discovered new constraint → Surface it and ask for prioritization
3. **Architectural Uncertainty**: Multiple valid approaches with tradeoffs → Present options, get preference
4. **Blockers**: Stuck >30 min → Ask for help or authorization to abandon task

**Litmus Test**: "Am I making assumptions that only a human can validate?"

**Rationale**: Automated processes should not make arbitrary decisions on ambiguous problems. Use human judgment as a tool.

---

### 0.2 Universal Decision Framework

This table standardizes decision thresholds across the entire project. Document any deviations in an ADR.

| Decision Type | Time Limit | Kill Switch Trigger | Notes |
|---------------|-----------|---------------------|-------|
| **Trivial Tool Integration** | 30 min debugging | Not working after 30 min | Example: Linter setup, formatter config |
| **Core Feature Integration** | 6 hours debugging | Not working after 6 hours + ADR documenting failure | Example: Auth system, payment gateway, major library |
| **Quality Standards** | No time limit | >5 critical defects after validation | Quality never compromised for speed |
| **Schedule Slip** | 2 consecutive days | Activate contingency plan | Traffic light goes Red → escalate |
| **Budget Overrun** | 75% of budget spent | Disable feature causing overrun | 90% = hard stop, 75% = warning |
| **Test Failures** | 3 consecutive failing builds | Roll back to last green build | Never ship broken builds |
| **Performance Degradation** | Response time >2x target p95 | Optimize or disable feature | User experience non-negotiable |

**Conflict Resolution**: If project-specific rules conflict with this table, document the deviation in an ADR with clear justification.

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
│  2. PROJECT CORE REQUIREMENTS        │ ← MUST HAVE features
│     - Defined in project scope       │
│     - Non-negotiable deliverables    │
└─────────────────────────────────────┘
           ↓ overrides ↓
┌─────────────────────────────────────┐
│  3. MILESTONE GATES                  │ ← Weekly/Sprint success criteria
│     - Incremental validation points  │
│     - Go/No-Go decisions             │
└─────────────────────────────────────┘
           ↓ overrides ↓
┌─────────────────────────────────────┐
│  4. IMPLEMENTATION DETAILS           │ ← Lowest priority
│     - Code style, tech choices       │
│     - Workflow preferences           │
└─────────────────────────────────────┘
```

**Conflict Resolution Rules**:
1. **Higher level wins**: If Section 0 conflicts with Section 3, Section 0 wins
2. **Later version wins**: If v2.0.0 conflicts with v1.2.0, v2.0.0 wins
3. **Explicit ADR wins**: If an ADR explicitly overrides constitution, ADR wins (but must document why)
4. **All conflicts MUST be documented**: Create ADR explaining resolution + update constitution

---

### 0.4 Constitution as Living Document

**Adaptation Principle**: This constitution is a TEMPLATE, not a rigid contract. It must evolve as you learn.

**When to Update**:
- **After each milestone**: Reflect on what worked/didn't work
- **When discovering new constraints**: External factors (API limits changed, service deprecated)
- **When external feedback challenges assumptions**: User testing reveals different priorities
- **When violating same principle >2 times**: Principle is wrong or unrealistic → amend it

**Amendment Process** (See Section 4: Governance):
1. Create ADR documenting proposed change + rationale
2. Update constitution + increment version (MAJOR/MINOR/PATCH)
3. Update development journal documenting amendment
4. Communicate changes if team expands

**Amendment Speed**: For solo developer, amendments can be lightweight (15-30 min). Do NOT let process paralyze progress.

---

## 1. RESOURCE MANAGEMENT FRAMEWORK

*Governing Principles: Section 0.1 (II, VI)*

### 1.1 Time Budget Allocation Framework

**Step 1: Calculate Total Available Hours**
- Formula: `WEEKS × HOURS_PER_WEEK × TEAM_SIZE`
- Example: 4 weeks × 40 hours × 1 person = 160 hours

**Step 2: Allocate by Activity Category**

| Activity Category | % Range | Use High End When | Use Low End When |
|-------------------|---------|-------------------|------------------|
| **Primary Deliverable** | 35-50% | Novel/complex domain | Well-understood problem |
| **Infrastructure** | 15-25% | New stack/tools | Familiar tech stack |
| **Integration** | 10-20% | Multiple services | Monolithic app |
| **Testing & QA** | 5-15% | High reliability needs | MVP/prototype |
| **Buffer** | 10-20% | First time on stack | Experienced team |

**Rules**:
- Front-load infrastructure (setup early to unblock development)
- Back-load testing (critical path testing throughout, comprehensive testing at end)
- Protect buffer time (never allocate 100% of available hours)

**Example Allocation (4-week project, 160 hours)**:

| Activity | Hours | % | Rationale |
|----------|-------|---|-----------|
| Primary Deliverable | 70 | 44% | Core value proposition (use high end for complex domains) |
| Infrastructure | 25 | 16% | Setup, deployment, CI/CD (moderate complexity) |
| Integration | 20 | 13% | Connecting components (multiple services) |
| Testing & QA | 15 | 9% | Critical path focus (solo developer) |
| Documentation | 10 | 6% | README, API docs, deployment guide |
| Buffer | 20 | 13% | Debugging, revisions, unknown unknowns |
| **Total** | **160** | **100%** | |

*Implements Section 0.1.VI (Constraint-Driven Development - time constraint becomes planning feature)*

---

### 1.2 Cost Management Framework

**Step 1: Establish Budget**
- Define total budget (e.g., $20, $100, $1000)
- Identify all metered services (APIs, cloud hosting, databases)
- Set monitoring thresholds at 75% and 90% of budget

**Step 2: Monitor Costs Daily**

| Service Category | Monitoring Frequency | Alert Threshold | Kill Switch |
|------------------|---------------------|------------------|-------------|
| **API Usage** (OpenAI, etc.) | Daily | 75% of budget | Disable non-critical features |
| **Cloud Hosting** | Weekly | Approaching quota | Optimize or upgrade tier |
| **Storage/Database** | Weekly | 80% of free tier | Archive old data or upgrade |

**Cost Control Patterns**:
- **Caching**: Cache expensive API responses (24-hour TTL typical)
- **Rate Limiting**: Limit queries per user (10/minute typical for free tiers)
- **Fallback Tiers**: Use cheaper models/services when possible (e.g., GPT-4o-mini > GPT-4)
- **Response Limits**: Cap response lengths (300 words typical)

*Governed by Section 0.2 (Budget Overrun threshold: 75%)*

---

### 1.3 Constraint-Driven Development Patterns

**Pattern 1: Turn API Limits into Caching Features**
- Constraint: API has request limits or costs money
- Feature: Implement intelligent caching → Improves response time AND reduces costs
- Example: Cache AI responses for identical queries

**Pattern 2: Turn Free-Tier Downtime into Resilience**
- Constraint: Free-tier service spins down after inactivity
- Feature: Static-first architecture with graceful degradation
- Example: Core content readable even when backend is down

**Pattern 3: Turn Time Limits into MVP Focus**
- Constraint: 4-week deadline
- Feature: Incremental validation prevents scope creep
- Example: Ship working MVP-0 in Week 1, iterate from there

*Implements Section 0.1.VI (Constraints as Features)*

---

## 2. RISK MANAGEMENT FRAMEWORK

*Governing Principles: Section 0.1 (I, VI, VII)*

### 2.1 Risk Assessment Template

Use this template to identify and mitigate risks:

| Risk | Probability | Impact | Mitigation Strategy | Kill Switch | Authority |
|------|------------|--------|---------------------|-------------|-----------|
| **External service cost overrun** | High | High | Rate limiting, caching, daily monitoring | Disable feature if >90% budget spent | Section 0.2 |
| **Free tier storage/quota limits** | Medium | High | Limit data size, optimize usage | Fallback to alternative service or degrade feature | Section 0.2 |
| **Free tier service downtime** | Medium | Medium | Static fallback UI, graceful degradation | Accept degraded UX, communicate in status page | Section 0.1.IV |
| **Deployment pipeline failure** | Low | High | Local build verification, backup deployment method | Manual deployment to alternative platform | Section 0.2 |
| **Third-party integration complexity** | Medium | Low | Time-box integration (6h limit) | Ship without integration if not working | Section 0.2 |

**Risk Categories** (adapt to your project):
- **External Dependencies**: APIs, cloud services, third-party libraries
- **Schedule Risks**: Content bottlenecks, integration delays, scope creep
- **Quality Risks**: Performance degradation, security vulnerabilities, UX issues
- **Team Risks**: Solo developer burnout, skill gaps, communication failures

---

### 2.2 Kill Switch Decision Framework

**When to Activate Kill Switch** (Section 0.2 authority):

1. **30-Minute Rule**: Trivial integrations not working after 30 min debugging
2. **6-Hour Rule**: Core features not working after 6 hours debugging
3. **2-Day Rule**: Schedule slip >2 consecutive days behind plan
4. **75% Budget Rule**: Costs approaching 75% of allocated budget
5. **Quality Rule**: >5 critical defects after validation

**Kill Switch Actions**:
- **Defer Feature**: Move to "Future Work" or next release
- **Simplify Scope**: Reduce feature to minimal viable version
- **Alternative Approach**: Document failure in ADR, try different solution
- **Accept Limitation**: Communicate constraint to users, ship without feature

*Governed by Section 0.1.I (Demo Reliability - ship working subset)*

---

### 2.3 Contingency Planning Patterns

**Pattern 1: Feature Cut Priority Framework**

Define feature priorities BEFORE starting development:

| Priority Level | Description | Cut When |
|----------------|-------------|----------|
| **P0 (Never Cut)** | Core value proposition | Never (define project failure if missing) |
| **P1 (Cut Last)** | Key differentiators | >2 days behind schedule |
| **P2 (Cut Middle)** | Nice-to-have enhancements | >1 week behind schedule |
| **P3 (Cut First)** | Bonus features | Any schedule pressure |

**Pattern 2: Schedule Slip Response**

| Days Behind | Traffic Light | Action |
|-------------|---------------|--------|
| 0-1 days | 🟢 Green | Continue, monitor daily |
| 2-3 days | 🟡 Yellow | Cut P3 features, reallocate buffer time |
| 4+ days | 🔴 Red | Cut P2 features, activate contingency plan, escalate |

*Governed by Section 0.2 (Schedule Slip: 2 consecutive days)*

**Pattern 3: Technical Failure Response**

| Failure Type | Detection | Response | Fallback |
|--------------|-----------|----------|----------|
| **Service Downtime** | Health check fails | Retry 3x with exponential backoff | Static fallback UI |
| **Integration Complexity** | >6h debugging | Abandon integration | Ship without feature |
| **Performance Degradation** | Response time >2x target | Optimize or cache aggressively | Disable feature if can't fix |
| **Budget Overrun** | Daily cost monitoring | Disable expensive features | Accept degraded functionality |

---

### 2.4 Pre-Mortem Exercise Template

**Purpose**: Imagine the project failed. What went wrong?

**Exercise** (15 minutes, run at project start):

1. **Imagine Failure**: "It's [END DATE] and the project scored <50% of goals. What happened?"

2. **List Failure Modes** (5 most likely):
   - Failure Mode 1: [Description] (XX% probability)
   - Cause: [Root cause]
   - Prevention: [How to avoid]

3. **Prioritize Top 3 Risks**: Focus mitigation efforts on highest probability × impact

4. **Create Monitoring Plan**: How will you detect each failure mode early?

**Example Failure Modes** (adapt to your domain):
- Feature returns incorrect results (poor testing)
- Content is low quality (insufficient review)
- Demo day: nothing works (service downtime, no rehearsal)
- Scope creep: 80% complete on everything, 100% on nothing (no MUST/SHOULD/COULD gates)

*Governed by Section 0.1.III (Incremental Validation - catch problems early)*

---

## 3. QUALITY ASSURANCE FRAMEWORK

*Governing Principles: Section 0.1 (I, III)*

### 3.1 Definition of Done (Feature-Level)

A feature is DONE when ALL criteria are met:

- [ ] Acceptance criteria from spec met 100%
- [ ] Code passes all linters and type checks
- [ ] Tests written and passing (see 3.2 for coverage philosophy)
- [ ] Manual testing completed on target platforms
- [ ] Documentation updated (API docs, README, inline comments where needed)
- [ ] No debug statements in committed code
- [ ] Code reviewed (self-review or peer review)
- [ ] Deployed to staging/test environment and smoke tested
- [ ] Development journal entry created (if >1 hour work)

*Governed By: Section 0.1.I (Demo Reliability - DONE = demo-able without errors)*

---

### 3.2 Testing Standards (Solo-Optimized)

**Philosophy**: Focus on demo reliability, not coverage metrics.

**Critical Path Testing ONLY** (MUST):
1. **Core Functionality**: Test the 3-5 features that define your product's value
2. **Error Handling**: Gracefully handle service failures, invalid input, edge cases
3. **Platform Compatibility**: Manual test on 1-2 target platforms (e.g., desktop + mobile)

**Deprioritized Testing**:
- Unit tests for pure functions (SHOULD - if time allows)
- Exhaustive edge case coverage (COULD - diminishing returns)
- Cross-browser/platform compatibility beyond primary targets (COULD)
- E2E tests with heavy frameworks (WON'T - too time-consuming for solo dev)

**Coverage Philosophy** (Realistic for Solo Developer):
- **Backend/API**: >40% coverage focusing on critical business logic
- **Frontend**: >20% coverage focusing on main user flows
- **Integration**: 5-10 test scenarios passing = sufficient for demo

**Rationale**: 5 working features demonstrated live > 70% test coverage with buggy features.

*Governed By: Section 0.1.I (Demo Reliability)*

---

### 3.3 Performance Standards Patterns

**Step 1: Define Performance Targets Per Project**

| Metric | Target | Measurement Method | Fallback |
|--------|--------|-------------------|----------|
| **Page Load Time** | <3s (p95) | Lighthouse CI or browser DevTools | Optimize images, lazy load |
| **API Response Time** | <2s (p95) | Backend logging or APM tool | Caching, query optimization |
| **Uptime** | >95% | Monitoring service (e.g., UptimeRobot) | Status page, graceful degradation |

**Step 2: Monitor and Optimize**

- **Measure First**: Use Lighthouse, WebPageTest, or APM tools to establish baseline
- **Optimize Critical Path**: Focus on slowest 20% of operations (80/20 rule)
- **Set Alerts**: Alert when p95 exceeds 2x target (Section 0.2 threshold)

**Kill Switch**: If performance cannot meet targets after optimization effort, disable or simplify feature.

*Governed by Section 0.2 (Performance Degradation threshold: >2x target p95)*

---

### 3.4 Code Quality Principles

**Principle 1: Self-Documenting Code**
- Good naming > comments (use descriptive variable/function names)
- Type signatures (TypeScript, Python type hints) document intent
- Comments only for non-obvious logic, workarounds, or complex algorithms

**Principle 2: Linting and Formatting**
- Automate formatting (Prettier, Black, etc.)
- Enforce linting rules (ESLint, Ruff/Pylint, etc.)
- Use pre-commit hooks to prevent committing non-compliant code

**Principle 3: Documentation Requirements**

When documentation is REQUIRED:
- **Public APIs**: Docstrings with example requests/responses
- **Components**: JSDoc/docstrings with parameter descriptions
- **Setup Instructions**: README files for root, frontend, backend
- **Deployment**: Step-by-step deployment guide
- **Architecture**: High-level architecture decision records (ADRs)

When documentation is NOT required:
- Self-explanatory functions (good naming is sufficient)
- Private/internal functions (unless complex logic)
- Obvious code (e.g., simple getters/setters)

*Governed By: Section 0.1.V (Explicit Over Implicit)*

---

## 4. GOVERNANCE

*Governing Principles: Section 0.1 (V)*

### 4.1 Architecture Decision Records (ADR)

**ADR Format Template**:

```markdown
# ADR-NNN: [Decision Title]

**Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]
**Date**: YYYY-MM-DD
**Deciders**: [Names or roles]
**Governing Principle**: Section 0.1.[I-VII] that applies

## Context
[Describe the problem requiring a decision]

## Decision
[State the decision clearly in 1-2 sentences]

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
- [ ] Documented in relevant project docs
```

**When to Create an ADR** (3-criteria test):

Create an ADR when ALL three conditions are met:
1. **Impact**: Decision has long-term consequences (affects architecture, data model, security)
2. **Alternatives**: Multiple viable options exist with significant trade-offs
3. **Scope**: Decision is cross-cutting (affects multiple modules or future features)

**Examples**:
- ✅ Choice of database (PostgreSQL vs MongoDB vs SQLite)
- ✅ Authentication strategy (JWT vs sessions vs OAuth)
- ✅ API architecture (REST vs GraphQL vs gRPC)
- ✅ Deployment platform (AWS vs Vercel vs self-hosted)
- ✅ Constitution override (deviating from Section 0.2 thresholds)
- ❌ Button color choice (trivial, no architectural impact)
- ❌ Variable naming (codified in style guide, not architectural)

**ADR Storage**:
- Location: `docs/adr/` or `history/adr/`
- Naming: `ADR-NNN-short-title.md` (NNN = zero-padded sequential number)
- Linking: Reference ADRs in code comments, docs, commit messages

---

### 4.2 Development Journal (Generalized from PHR)

**Purpose**: Track significant decisions, prompts, and outcomes for learning and traceability.

**When to Create Journal Entries**:
- After significant implementation work (>1 hour)
- After debugging sessions that resolved critical issues
- After architectural discussions or spec changes
- When using AI assistance for complex tasks

**Storage**:
- Location: `history/journal/` or `docs/journal/`
- Naming: `YYYY-MM-DD-brief-description.md`

**Minimal Journal Entry Format**:

```markdown
# [Brief Description]

**Date**: YYYY-MM-DD
**Task**: [What you were working on]
**Outcome**: [What was accomplished or learned]

## Context
[Brief context or problem statement]

## Actions Taken
- [Bullet list of key actions]

## Files Modified
- [List of files created/modified]

## Lessons Learned
[Key insights or gotchas for future reference]
```

**Note**: This is optional for non-AI-assisted projects. Valuable for AI-assisted development to track prompt effectiveness and decision rationale.

---

### 4.3 Communication Standards

**Commit Message Format** (Conventional Commits):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no functional change)
- `refactor`: Code restructuring (no functional change)
- `test`: Adding or updating tests
- `chore`: Build config, dependencies, tooling

**Examples**:
- `feat(api): add rate limiting to chat endpoint`
- `fix(auth): resolve token refresh infinite loop`
- `docs(readme): add deployment instructions`
- `test(api): add integration tests for user registration`

---

### 4.4 Constitution Health & Amendment Process

**Weekly Constitution Review** (5 minutes every week):
- [ ] Did I reference the constitution when making decisions this week?
- [ ] Did I discover any contradictions or gaps?
- [ ] Are time budgets still realistic? (Update if >20% variance)
- [ ] Are principles being followed or just documented?
- [ ] Did I invoke Section 0.1.VII (Human as Tool) when stuck?

**Amendment Triggers**:
- Found >3 contradictions in one week → Schedule constitution review
- Violated same principle >2 times → Principle may be wrong, consider amendment
- External feedback challenges core assumptions → Update assumptions in ADR
- Time budgets off by >20% for 2 consecutive weeks → Revise allocation framework

**Amendment Procedure**:
1. Create ADR documenting proposed change + rationale
2. Update constitution + increment version (MAJOR/MINOR/PATCH)
3. Update development journal documenting amendment
4. Communicate changes if team expands

---

### 4.5 Version Control

**Current Version**: 2.0.0 (General Framework)

**Versioning Rules**:
- **MAJOR**: Backward-incompatible changes (removed principles, fundamental philosophy changes)
- **MINOR**: New principles, sections, or expanded guidance (additive changes)
- **PATCH**: Clarifications, typo fixes, formatting improvements

**Version History**:
- **2.0.0 (2026-02-08)**: Generalized from hackathon-specific to universal framework (~500 lines)
- 1.2.0 (2026-02-08): Hackathon-specific constitution (1,790 lines) - archived

---

**End of Constitution**

*This document is the single source of truth for project governance. When in doubt, return to Section 0: Universal Principles.*

*Excellence in fundamentals > breadth of features. Ship working software.* (Section 0.1.I)

**Version**: 2.0.0 | **Ratified**: 2026-02-08 | **Type**: General Framework (~500 lines)
