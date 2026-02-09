# ADR-0002: Content Authoring Workflow with AI Assistance

- **Status:** Accepted
- **Date:** 2026-02-09
- **Feature:** Physical AI & Humanoid Robotics Educational Textbook
- **Context:** Educational content requiring 90-120 pages across 6 modules, 3-5 diagrams per chapter, IEEE citations, university-level academic tone, 4-week timeline with single-author constraint (constitution Section 0.1.II)

## Decision

Adopt **AI-Assisted Template-Based Sequential Workflow** with mandatory human validation:

**Workflow Components:**
- **Content Generation:** Claude Code + SpecKit Plus templates (60-80% AI draft, 20-40% human refinement)
- **Structural Templates:** `module-template.mdx`, `chapter-template.mdx` (4-section format: Intro→Theory→Examples→Summary)
- **Sequential Execution:** One module at a time, no parallelization of content writing (constitution Section 0.1.II)
- **Validation Gate:** 12-point review checklist (FR-029) mandatory between modules, <5 errors or reject (SC-005)
- **Pilot Phase:** Module 0 as prototype (6 success criteria must pass before Module 1 starts)
- **Human Review:** Mandatory review of all AI-generated content before validation (FR-011)
- **Continuous Improvement:** lessons-learned.md updated after each module, templates adjusted based on feedback

**Quality Assurance:**
- 30-minute validation per module (constitution Section 4.1.5)
- Code examples include version comments (FR-011: "# Minimum version: Python 3.8, ROS 2 Humble")
- Citations validated for open-access (SC-007: 100% accessible URLs)
- Diagrams captioned with figure numbers (3-5 per chapter)

**Time Budget:**
- Content creation: 66h (44% of 107h total project time)
- Module complexity tiers: LOW (Module 0: 8h) → MEDIUM (Modules 1,4: 10h) → HIGH (Modules 2,3,5: 12-14h)

## Consequences

### Positive

- **Speed without quality sacrifice:** AI generates 60-80% of content structure, human focuses on accuracy and refinement (target: 1.5-2.0 pages/hour)
- **Consistency enforcement:** Templates ensure uniform 4-section structure across all 6 modules (Intro/Theory/Examples/Summary)
- **Early error detection:** Pilot phase (Module 0) validates workflow before scaling to 6 modules, prevents "90% complete" trap (constitution Section 0.1.III)
- **Compounding efficiency:** lessons-learned.md captures improvements, target 10-15% efficiency gain by Module 5
- **Constitutional alignment:** Sequential workflow prevents context-switching (Section 0.1.II), validation gates prevent rushed work (Section 0.1.III)
- **Single-author feasibility:** AI assistance enables one person to write 90-120 pages in 4 weeks (otherwise requires 3-person team)
- **Audit trail:** PHRs document all AI-assisted content creation, ADRs document workflow changes

### Negative

- **AI hallucination risk:** Without human review, factual errors propagate across modules (mitigation: mandatory validation checklist, <5 errors kill switch)
- **Template rigidity:** 4-section structure may not fit all content (mitigation: flexibility allowed within sections, not structure)
- **Pilot failure delays:** If Module 0 fails validation, 2-day re-work delay cascades to entire project timeline (mitigation: Module 0 chosen for lowest complexity)
- **Human review bottleneck:** Single author must review all AI output, cannot parallelize validation (accepted: aligns with constitution Section 0.1.II)
- **AI tool dependency:** Claude Code outage blocks content generation (mitigation: manual authoring fallback, template provides structure)
- **Over-reliance temptation:** Risk of insufficient human refinement if time pressure mounts (mitigation: 30-minute validation enforced)

### Key Risks

**Risk 1: AI-Generated Content Fails Academic Standards (P0)**
- **Likelihood:** Medium-High (first-time AI content creation)
- **Impact:** Module fails validation, 4-12 hour re-work required
- **Mitigation:** Module 0 pilot tests academic tone before scaling, external review via r/robotics after Module 0
- **Kill Switch:** >5 factual errors = reject module, fix before proceeding (SC-005)
- **Accepted Tradeoff:** Speed gains worth validation risk if pilot succeeds

**Risk 2: Pilot Phase Failure Cascades Project Delay (P1)**
- **Likelihood:** Low-Medium (Module 0 simplest content)
- **Impact:** 2-day delay minimum, potential 5-day delay if workflow needs major revision
- **Mitigation:** Module 0 chosen for lowest technical complexity (theory-heavy, minimal code examples), 6 explicit pilot success criteria
- **Fallback:** If pilot fails twice, switch to manual authoring (loses AI speed advantage)

**Risk 3: Template Structure Inadequate After Pilot (P2)**
- **Likelihood:** Low (templates based on proven academic textbook patterns)
- **Impact:** Template re-work after Module 0-1 validated, affects Modules 2-6 structure
- **Mitigation:** Lock templates after Module 1 validation (plan.md line 630), no structural changes after that point
- **Accepted Tradeoff:** Rigidity acceptable to prevent mid-project churn

**Risk 4: Citation Accessibility Crisis (P1)**
- **Likelihood:** Medium (40% academic papers typically paywalled)
- **Impact:** 4-hour research blitz required per module, potential content re-writing
- **Mitigation:** Validate citations BEFORE writing content (not after), prioritize framework docs (ROS 2, NVIDIA, Unity - all open-access)
- **Fallback:** Reduce to minimum 3 citations per module using only framework docs (FR-035)

**Risk 5: Efficiency Gains Fail to Materialize (P3)**
- **Likelihood:** Low-Medium
- **Impact:** Project overruns 107h budget, timeline extends beyond 4 weeks
- **Mitigation:** Track pages-per-hour after Module 0, activate scope reduction if <1.0 p/h sustained (plan.md line 677)
- **Kill Switch:** >25% time overrun on any module → split into multiple chapters or defer module

## Alternatives Considered

### Alternative A: Manual Authoring (No AI Assistance)
**Components:** Human writes 100% of content, no AI drafting, templates for structure only

**Pros:** Maximum quality control, no hallucination risk, full human oversight
**Cons:** 3x slower (0.5-1.0 pages/hour vs. 1.5-2.0 with AI), requires 8-12 weeks for 90-120 pages, misses 4-week deadline
**Key Risk:** Timeline failure (unacceptable per constitution Section 0.2)
**Rejected:** Cannot meet 4-week constraint with single author

### Alternative B: Parallel Multi-Module Development
**Components:** AI generates 3+ modules simultaneously, human reviews in batch

**Pros:** Faster overall timeline (potential 2-week completion), maximizes AI throughput
**Cons:** Violates constitution Section 0.1.II (Single-Threaded Focus), context-switching between modules, error cascades across multiple modules if template flawed
**Key Risk:** "90% complete" trap - 6 incomplete modules harder to finish than 3 complete modules
**Rejected:** Constitutional violation, higher cognitive load, worse error propagation

### Alternative C: AI-Only with Post-Hoc Review (No Human Loop)
**Components:** AI generates all 6 modules, human reviews after all content complete

**Pros:** Maximum speed (potential 1-week AI generation), minimal human time during drafting
**Cons:** High rework cost if errors discovered late (8-20 hours to fix 6 modules), violates FR-011 (mandatory human review during creation), constitutional Section 0.1.VII (Human as Tool)
**Key Risk:** Catastrophic failure if AI misunderstands requirements, 6 modules need re-writing
**Rejected:** Too risky, violates mandatory human review requirement

### Alternative D: Outsourced Content Creation (Hire Writers)
**Components:** Hire 2-3 technical writers, assign modules, review final output

**Pros:** Parallelization possible, expert human authoring, no AI risk
**Cons:** Cost (3 writers × 4 weeks = $12-20K), coordination overhead, style inconsistency, violates hackathon spirit (self-contained project)
**Key Risk:** Budget constraint (hackathon assumes zero external costs)
**Rejected:** Cost prohibitive, coordination complexity

### Alternative E: Hybrid Multi-Agent AI Workflow
**Components:** Multiple AI agents (content, diagrams, citations) work in parallel, orchestrated by meta-agent

**Pros:** Maximum automation, potential 1.5-2 week timeline, parallel processing
**Cons:** Complex orchestration, higher error rate (multiple AI outputs need reconciliation), violates Single-Threaded Focus, untested workflow adds risk
**Key Risk:** Novel workflow may fail catastrophically, no time for experimentation
**Rejected:** Too complex, pilot phase would take >1 week to validate

## Operational Impact

**Daily Workflow:**
1. Content author works on Module N using `chapter-template.mdx` (4-6h)
2. AI generates 60-80% of Theory and Examples sections (Claude Code prompts)
3. Human refines AI output: fact-check, citation validation, code testing (20-40% effort)
4. After module complete: run 12-point review checklist (30 minutes)
5. If pass: commit to Git, create tag `module-N-validated`, start Module N+1
6. If fail: document in `validation-failures/module-N-YYYYMMDD.md`, fix errors (decision matrix applies)

**Weekly Cadence:**
- **Sunday Review** (15 minutes): Update burndown dashboard, velocity metrics, traffic light status
- **Post-Module Review** (30 minutes): Update lessons-learned.md, adjust templates if needed
- **After Module 0 Pilot** (1 hour): External review via r/robotics, validate workflow before scaling

**Monitoring:**
- Pages per hour: Track after each module (target 1.5-2.0 p/h)
- Validation pass rate: Target 100% first-attempt (re-work indicates template or AI prompt issues)
- Citation accessibility: Target 100% open-access (SC-007)
- Time overruns: Trigger scope reduction if >25% over budget

## Security & Compliance Impact

**AI Content Risks:**
- **Hallucination/Fabrication:** AI may invent citations, framework features, code APIs (mitigation: human verifies all technical claims)
- **Outdated Information:** AI training data may reference deprecated versions (mitigation: version comments in code, validate framework versions during review)
- **Plagiarism Risk:** AI may reproduce training data verbatim (mitigation: Grammarly plagiarism check on Theory sections)
- **Bias:** AI may favor certain frameworks or exclude perspectives (mitigation: human reviews for balanced coverage)

**Academic Integrity:**
- **Authorship:** AI-generated content documented in PHRs (transparency requirement)
- **Citation Quality:** IEEE format enforced, open-access validated (SC-007)
- **Originality:** Human refinement ensures content not copy-paste from sources

**Data Privacy:**
- No user data collected (public content only)
- AI prompts may contain textbook content (acceptable: public educational material)

## Consequences If Decision Fails

**Failure Scenario 1: Pilot Phase Fails Validation Twice**
- **Probability:** Low (Module 0 simplest content)
- **Response:** Switch to manual authoring (Alternative A), extend timeline to 8 weeks or reduce scope to 4 modules
- **Data Loss:** 12-24 hours Module 0 work discarded
- **Reversal Cost:** High (loses AI speed advantage, project timeline at risk)

**Failure Scenario 2: AI Tool Unavailable (Claude Code Outage)**
- **Probability:** Very Low (<1% uptime risk)
- **Response:** Manual authoring fallback using templates, continue with reduced speed
- **Impact:** 2-3x slowdown, may trigger scope reduction
- **Mitigation:** Templates provide structure even without AI

**Failure Scenario 3: Human Review Bottleneck (Author Unavailable)**
- **Probability:** Low (single-author project assumes continuous availability)
- **Response:** Pause content generation, resume when author returns
- **Impact:** Timeline slip, activate scope reduction if >2 days delay

**Failure Scenario 4: Efficiency Gains Fail (<1.0 pages/hour)**
- **Probability:** Medium (untested workflow)
- **Response:** Activate scope reduction (defer Module 4-5 to "Coming Soon" placeholders)
- **Reversal:** Increase AI assistance level (90% AI draft, 10% human refinement) - accept higher error rate

**Reversal Cost:** Low (manual authoring always possible, templates remain useful)

## References

- Feature Spec: `/home/salim/Desktop/hackathine_1/specs/001-physical-ai-textbook/spec.md` (FR-011, FR-029, FR-035, FR-046, SC-005, SC-007)
- Implementation Plan: `/home/salim/Desktop/hackathine_1/specs/001-physical-ai-textbook/plan.md` (lines 519-632: Execution Timeline, Pilot Phase Strategy)
- Related ADRs: ADR-0001 (Static Site Architecture), ADR-0003 (Interactive Features)
- Constitution Alignment: Section 0.1.II (Single-Threaded Focus), Section 0.1.III (Incremental Validation), Section 0.1.VII (Human as Tool), Section 4.1.5 (Content Quality Gates)
