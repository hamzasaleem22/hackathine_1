# Validation Failures Directory

This directory stores validation failure reports for modules that do not pass the 12-point review checklist on first attempt.

**Purpose**: Enable structured documentation of errors, root cause analysis, and recovery procedures per the Rollback & Recovery Procedures section of plan.md.

**When to Create Files**: When a module receives >5 factual errors during validation OR fails 3+ checklist criteria.

## File Naming Convention

```
module-{N}-YYYYMMDD.md
```

**Examples**:
- `module-0-20260215.md` - Module 0 validation failure on Feb 15, 2026
- `module-3-20260225.md` - Module 3 validation failure on Feb 25, 2026

## File Template

Use this template when documenting validation failures:

```markdown
# Module {N} Validation Failure Report

**Date**: YYYY-MM-DD
**Validator**: [Name/Role]
**Module**: Module {N}: {Module Title}
**Validation Attempt**: First / Second / Third

## Summary
- **Total Errors Found**: __ (__ critical, __ major, __ minor)
- **Checklist Failures**: __/12 criteria failed
- **Estimated Repair Time**: __h

## Critical Errors ({count})
1. {Error description} - **Severity**: Critical - **Est. fix**: {time}
   - **Location**: {file:line or section}
   - **Impact**: {why this matters}
   - **Proposed fix**: {how to resolve}

2. {Error description} - **Severity**: Critical - **Est. fix**: {time}
   ...

## Major Errors ({count})
1. {Error description} - **Severity**: Major - **Est. fix**: {time}
   ...

## Minor Errors ({count})
1. {Error description} - **Severity**: Minor - **Est. fix**: {time}
   ...

## Checklist Failures

| Category | Validation Question | Status | Issue Description |
|----------|---------------------|--------|-------------------|
| {Category} | {Question} | ❌ FAIL | {Why it failed} |
| {Category} | {Question} | ❌ FAIL | {Why it failed} |

## Root Cause Analysis

**Primary Root Cause**: {e.g., "Outdated framework versions used in code examples"}

**Contributing Factors**:
1. {Factor 1 - e.g., "AI tool training data from 2023, not current"}
2. {Factor 2 - e.g., "Version verification step skipped"}

**Preventable?**: YES / NO
- {Explanation of how this could have been prevented}

## Decision (Per Rollback & Recovery Procedures)

**Total Estimated Repair Time**: __h

**Decision Matrix Check**:
| Scenario | Repair Time | Error Count | Decision |
|----------|-------------|-------------|----------|
| {Current scenario} | __h | __ errors | {Option A/B/C} |

**Selected Option**: {A/B/C} - {Description}
- **Option A**: Fix errors → Re-validate
- **Option B**: Fix IF buffer hours available
- **Option C**: Replace with placeholder OR split into 2 chapters

**Justification**: {Why this option was chosen}

## Resource Reallocation

**Original Resource Allocation** (from plan.md):
- Content: __h
- Diagrams: __h
- Code Examples: __h
- Validation: __h
- **Total**: __h

**Revised Allocation** (if fixing):
- Error fixes: +__h
- Re-validation: +__h
- **New Total**: __h
- **Buffer hours used**: __h / 5h available

**Timeline Impact**:
- Original completion: Week {N} Day {M}
- Revised completion: Week {N} Day {M+X}
- **Critical path delayed?**: YES / NO

## Action Plan

**Immediate Actions** (next 2 hours):
1. [ ] STOP work on Module {N+1}
2. [ ] Update Progress Tracking Dashboard (set status to 🔴 Red)
3. [ ] {Specific fix action 1}
4. [ ] {Specific fix action 2}

**Repair Tasks** (sequential):
1. [ ] {Task 1} - Est: __h
2. [ ] {Task 2} - Est: __h
3. [ ] {Task 3} - Est: __h
4. [ ] Re-run validation checklist
5. [ ] Update communication-log.md with outcome

**Resume Criteria**:
- [ ] All critical errors fixed
- [ ] All checklist criteria pass
- [ ] Re-validation shows 0 critical errors
- [ ] Progress dashboard updated to 🟢 Green

## Lessons for Continuous Improvement

**Update lessons-learned.md with**:
1. {What went wrong - specific failure}
2. {Root cause - why it happened}
3. {Prevention - how to avoid in future modules}

**Template/Workflow Changes Needed**:
- [ ] Update chapter-template.mdx: {Specific change}
- [ ] Update review-checklist.md: {Additional validation step}
- [ ] Create automation script: {Script purpose}
- [ ] Document in quickstart.md: {New best practice}

## Sign-Off

**Validator**: {Name} - {Date}
**Content Creator**: {Name} - {Date}
**Resolution Status**: OPEN / IN PROGRESS / RESOLVED
**Final Validation Result**: PASS / FAIL / PENDING
```

## Expected Files

This directory should remain **empty** if all modules pass validation on first attempt (target: 100% first-attempt pass rate).

**If non-empty**: Each file represents a deviation from the planned workflow requiring root cause analysis and process improvement.

## Related Documentation

- **plan.md**: Section "Rollback & Recovery Procedures" - Scenario 1
- **lessons-learned.md**: Document learnings from validation failures
- **communication-log.md**: Update weekly status to 🔴 Red if validation fails
