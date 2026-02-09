# Change Requests Directory

This directory stores formal change requests for modifications to the project specification (`spec.md`) after implementation begins (after Week 1 Day 1).

**Purpose**: Enable structured change control per the "Change Control & Scope Management" section of plan.md, preventing scope creep and uncontrolled modifications.

**When to Create Files**: Any time a change to requirements, features, or scope is proposed after Week 1 Day 1 (infrastructure setup completion).

## File Naming Convention

```
CR-{NNN}-{title-slug}.md
```

**Examples**:
- `CR-001-add-interactive-quizzes.md` - Request to add interactive quiz feature
- `CR-002-update-ros2-version.md` - Request to update ROS 2 target version
- `CR-003-reduce-module-5-scope.md` - Emergency scope reduction request

**Numbering**: Sequential (001, 002, 003, ...)

## File Template

Use this template when creating change requests:

```markdown
# Change Request: CR-{NNN}

**Date**: YYYY-MM-DD
**Requested By**: {Name/Role}
**Type**: Feature Addition / Requirement Change / Clarification / Bug Fix
**Priority**: P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)
**Status**: OPEN / APPROVED / DEFERRED / CONDITIONAL / REJECTED

## Description

{Clear, detailed description of what needs to change and why}

## Justification

**Business/Technical Rationale**:
- {Reason 1 - e.g., "ROS 2 Humble reaches EOL before project completion"}
- {Reason 2 - e.g., "User feedback indicates confusion about topic X"}
- {Reason 3 - e.g., "Performance issue discovered during Module 0 testing"}

**Impact if NOT Changed**:
- {What happens if we don't make this change?}

## Impact Assessment (30-minute analysis)

**Time Impact**:
| Factor | Assessment | Details |
|--------|------------|---------|
| **Hours Required** | __h | Breakdown: __h content + __h diagrams + __h validation |
| **Modules Affected** | [Module X, Y] | {Which modules need revision?} |
| **Critical Path Impact** | YES / NO | {Will it delay final deadline?} |
| **Buffer Hours Available** | __h / 5h | {From 5h total project buffer} |
| **Constitution Violation** | YES / NO | {Check Section 0.1 principles} |
| **Template Changes** | YES / NO | {Requires updating chapter-template.mdx?} |

**Quality Impact**:
- Improves quality? YES / NO - {How?}
- Introduces risk? YES / NO - {What risk?}

**Scope Impact**:
- Increases scope? YES / NO - {By how much?}
- Decreases scope? YES / NO - {What is removed?}

## Decision Matrix (Automated Recommendation)

| Hours | Critical Path | Buffer Available | Recommendation |
|-------|---------------|------------------|----------------|
| __h | {YES/NO} | __h | {APPROVE / DEFER / CONDITIONAL / REJECT} |

**Matrix Rules** (from plan.md):
- <2h + No critical path impact + Any buffer = **APPROVE**
- <2h + Critical path impact + >2h buffer = **DEFER**
- 2-8h + No critical path impact + >4h buffer = **CONDITIONAL**
- 2-8h + Critical path impact + <4h buffer = **REJECT**
- >8h + Any scenario = **REJECT** (requires full re-planning via ADR)

## Decision

**Status**: OPEN / APPROVED / DEFERRED / CONDITIONAL / REJECTED

**Decision Rationale**: {Why this decision was made}

**Decision Date**: YYYY-MM-DD
**Decided By**: {Name/Role}

**Conditions** (if CONDITIONAL):
1. {Condition 1 - e.g., "Approve only if Module 0 completes 2h under budget"}
2. {Condition 2 - e.g., "Approve only if no other P0 changes pending"}

**Deferral Target** (if DEFERRED):
- Implement after: {Milestone - e.g., "Module 3 completion"}
- Or: Document as v2.0 enhancement

**Rejection Reason** (if REJECTED):
- {Specific reason - e.g., "Exceeds buffer hours, violates Section 0.1.II (Single-Threaded Focus)"}
- **Alternative**: {Suggest alternative approach or workaround}

## Implementation Plan (if APPROVED)

### Step 1: Update spec.md
- [ ] Increment version number: v{X}.{Y}.{Z} → v{X}.{Y}.{Z+1}
- [ ] Add change to appropriate FR section: {FR-NNN}
- [ ] Update Clarifications section with Q&A: {Question & Answer}
- [ ] Update Success Criteria if affected: {SC-NNN}

### Step 2: Create ADR (if architectural impact)
- [ ] File: `history/adr/{NNN}-{decision-title}.md`
- [ ] Document: Rationale, alternatives considered, consequences
- [ ] **ADR Required?**: YES / NO - {Why?}

### Step 3: Update Affected Modules (if already written)
| Module | Changes Required | Estimated Hours | Validation Status |
|--------|------------------|-----------------|-------------------|
| Module {N} | {Description} | __h | PENDING / IN PROGRESS / COMPLETE |

- [ ] Module {N}: Re-validate with 12-point checklist
- [ ] Module {N}: Update diagrams/code examples as needed

### Step 4: Adjust Resource Allocation
**Original Allocation** (from plan.md Resource Allocation Matrix):
- Module {N}: __h

**Revised Allocation**:
- Module {N}: __h (+__h for change)
- **Buffer used**: __h / 5h

**Timeline Adjustment**:
- Original: Week {N} Day {M}
- Revised: Week {N} Day {M+X}
- **Days added to critical path**: __

### Step 5: Communication
- [ ] Update Progress Tracking Dashboard (plan.md)
- [ ] Create PHR documenting change and impact: `history/prompts/001-physical-ai-textbook/`
- [ ] Update communication-log.md: Weekly status section
- [ ] If constitution compliance affected: Trigger Section 0.1 re-check

## Scope Freeze Compliance Check

**Current Date**: {YYYY-MM-DD}

| Freeze Date | Freeze Type | Status |
|-------------|-------------|--------|
| Week 1 Day 3 | Infrastructure freeze | {BEFORE / AFTER} |
| Week 2 Day 7 | Template structure freeze | {BEFORE / AFTER} |
| Week 4 Day 1 | Content freeze | {BEFORE / AFTER} |

**Enforcement Rule**: Changes after freeze date are automatically **REJECTED** unless P0 (critical bug)

**Freeze Violation?**: YES / NO
- If YES and NOT P0: **AUTO-REJECT**
- If YES and P0: Requires explicit justification

## Constitutional Alignment Check

**Section 0.1.II (Single-Threaded Focus)**: PASS / FAIL
- {Does this change maintain single-threaded focus or introduce context switching?}

**Section 0.1.III (Incremental Validation)**: PASS / FAIL
- {Can this change be validated incrementally?}

**Section 0.2 (Universal Decision Framework)**: PASS / FAIL
- {Does this follow the 30-minute decision threshold?}

**Overall Constitution Compliance**: PASS / FAIL

## Alternatives Considered

**Alternative 1**: {Description}
- **Pros**: {Benefits}
- **Cons**: {Drawbacks}
- **Why not chosen**: {Reason}

**Alternative 2**: {Description}
- **Pros**: {Benefits}
- **Cons**: {Drawbacks}
- **Why not chosen**: {Reason}

**Do Nothing (Status Quo)**:
- **Pros**: {No time investment, maintains schedule}
- **Cons**: {Problem persists}
- **Risk**: {What's the risk of not changing?}

## Sign-Off

**Requested By**: {Name} - {Date}
**Reviewed By**: {Name} - {Date}
**Approved By**: {Name} - {Date}
**Implementation Status**: NOT STARTED / IN PROGRESS / COMPLETE / CANCELLED
```

## Expected Usage Pattern

**Healthy Project**: 0-3 change requests total (minimal scope changes)
**Warning**: 4-6 change requests (scope creep risk)
**Red Flag**: >6 change requests (indicates inadequate initial planning)

**Target**: Zero change requests after scope freeze dates (Week 1 Day 3, Week 2 Day 7, Week 4 Day 1)

## Common Change Request Types

### 1. Technical Changes
- Framework version updates (e.g., ROS 2 Humble → Jazzy)
- Tool changes (e.g., Gazebo → Isaac Sim)
- Platform changes (e.g., Desktop → Mobile optimization)

### 2. Content Changes
- Module scope adjustments (add/remove topics)
- Assessment format changes
- Diagram style changes

### 3. Quality Changes
- Additional validation criteria
- Performance threshold adjustments
- Citation requirements changes

### 4. Schedule Changes
- Deadline adjustments
- Resource reallocation
- Scope reduction (emergency)

## Related Documentation

- **plan.md**: Section "Change Control & Scope Management"
- **spec.md**: Source of truth for all requirements (updated when CRs approved)
- **communication-log.md**: Weekly tracking of change impact on schedule
- **history/adr/**: Architectural Decision Records (created if CR has architectural impact)
