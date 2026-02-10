# Module Validation Checklist

**Module**: {{MODULE_NAME}}
**Reviewer**: {{REVIEWER_NAME}}
**Review Date**: {{REVIEW_DATE}}
**Version**: {{VERSION}}

---

## Instructions

This 12-point checklist validates module content quality against spec requirements. Each criterion must receive a **PASS** or **FAIL** rating.

**Pass Threshold**: ≤4 minor issues OR 0 critical errors
**Critical Errors**: Factual inaccuracies, broken code, missing citations, incorrect technical depth

---

## Validation Criteria

| # | Category | Validation Question | Status | Notes |
|---|----------|---------------------|--------|-------|
| 1 | **Content Completeness** | Does module meet 15-20 page requirement in standard academic format (FR-002)? | [ ] PASS<br>[ ] FAIL | Pages: ___<br>Issues: |
| 2 | **Content Completeness** | Are all specified topics from module requirements covered (FR-023 to FR-028)? | [ ] PASS<br>[ ] FAIL | Missing topics: |
| 3 | **Technical Accuracy** | Do all code examples execute correctly in target environments (SC-002: 90% target)? | [ ] PASS<br>[ ] FAIL | Tested: ___/___<br>Pass rate: ___% |
| 4 | **Technical Accuracy** | Are framework versions current and properly cited (FR-011, FR-045)? | [ ] PASS<br>[ ] FAIL | Outdated versions: |
| 5 | **Citation Quality** | Are all external sources cited in IEEE format (FR-014, FR-015)? | [ ] PASS<br>[ ] FAIL | Missing citations: |
| 6 | **Citation Quality** | Do all citations include accessible URLs or DOI references (100% open-access per SC-007)? | [ ] PASS<br>[ ] FAIL | Paywalled: ___<br>Broken links: ___ |
| 7 | **Diagram Appropriateness** | Does chapter include 3-5 diagrams enhancing understanding (FR-007)? | [ ] PASS<br>[ ] FAIL | Diagrams: ___<br>Missing: |
| 8 | **Diagram Appropriateness** | Are all diagrams properly captioned with figure numbers (FR-008)? | [ ] PASS<br>[ ] FAIL | Uncaptioned: |
| 9 | **Academic Standards** | Does content maintain university-level formal tone throughout (FR-006)? | [ ] PASS<br>[ ] FAIL | Tone issues: |
| 10 | **Academic Standards** | Is technical depth appropriate for upper-division/graduate students (FR-006)? | [ ] PASS<br>[ ] FAIL | Depth issues: |
| 11 | **AI Usage Compliance** | Are AI-generated sections documented per FR-013? | [ ] PASS<br>[ ] FAIL | Undocumented: |
| 12 | **AI Usage Compliance** | Has all AI content undergone mandatory human review (FR-011)? | [ ] PASS<br>[ ] FAIL | Unreviewed: |

---

## Detailed Findings

### Critical Errors (P0 - Must Fix Before Approval)

1. {{CRITICAL_ERROR_1}}
2. {{CRITICAL_ERROR_2}}
3. {{CRITICAL_ERROR_3}}

### Minor Issues (P1 - Fix Before Next Module)

1. {{MINOR_ISSUE_1}}
2. {{MINOR_ISSUE_2}}
3. {{MINOR_ISSUE_3}}

### Suggestions (P2 - Optional Improvements)

1. {{SUGGESTION_1}}
2. {{SUGGESTION_2}}
3. {{SUGGESTION_3}}

---

## Quantitative Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Page Count** | 15-20 pages | ___ pages | {{STATUS}} |
| **Diagrams** | 3-5 per chapter | ___ total | {{STATUS}} |
| **Citations** | IEEE format, 100% accessible | ___ total, ___% accessible | {{STATUS}} |
| **Code Examples** | 90% functional | ___% | {{STATUS}} |
| **Build Time** | <60 seconds | ___ seconds | {{STATUS}} |
| **Checklist Pass Rate** | 12/12 or ≤4 minor issues | ___/12 passed | {{STATUS}} |

---

## Validation Decision

**Overall Assessment**:
- [ ] ✅ **PASS** - Module approved for deployment (0-4 minor issues, 0 critical errors)
- [ ] 🟡 **CONDITIONAL PASS** - Approved with minor revisions required within 24h
- [ ] 🔴 **FAIL** - Module requires significant rework (≥5 issues OR ≥1 critical error)

**Estimated Remediation Time**: {{REMEDIATION_HOURS}} hours

---

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **Content Creator** | {{CREATOR_NAME}} | {{CREATOR_SIG}} | {{CREATOR_DATE}} |
| **Technical Reviewer** | {{REVIEWER_NAME}} | {{REVIEWER_SIG}} | {{REVIEWER_DATE}} |
| **Quality Approver** | {{APPROVER_NAME}} | {{APPROVER_SIG}} | {{APPROVER_DATE}} |

---

## Next Steps

**If PASS:**
1. [ ] Merge module to main branch
2. [ ] Update communication-log.md with completion
3. [ ] Document lessons learned in lessons-learned.md
4. [ ] Proceed to next module

**If FAIL:**
1. [ ] Document issues in `specs/001-physical-ai-textbook/validation-failures/module-{{MODULE_NUM}}-failure-{{DATE}}.md`
2. [ ] Create remediation plan with task breakdown
3. [ ] Schedule re-validation within {{REVAL_DAYS}} days
4. [ ] Update templates/workflow if systemic issues found

---

**Checklist Version**: 1.0
**Aligned with**: spec.md (FR-029, FR-030, FR-031), plan.md (12-point validation)
