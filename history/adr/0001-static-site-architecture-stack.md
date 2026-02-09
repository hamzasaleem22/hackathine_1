# ADR-0001: Static Site Architecture Stack

- **Status:** Accepted
- **Date:** 2026-02-09
- **Feature:** Physical AI & Humanoid Robotics Educational Textbook
- **Context:** Educational textbook requiring static site generation, no backend, public access only, <2s page load, GitHub Pages deployment with CI/CD automation

## Decision

Adopt **Docusaurus 3.x + TypeScript + GitHub Pages** as integrated static site architecture:

- **Static Site Generator:** Docusaurus 3.x (React-based, academic-optimized)
- **Type Safety:** TypeScript 5.x (config files, custom components)
- **Deployment Platform:** GitHub Pages (CDN, 95% uptime SLA, 500+ concurrent users)
- **CI/CD:** GitHub Actions (automated build-test-deploy)
- **Content Format:** MDX (Markdown + React components)
- **Package Manager:** npm/yarn (Node.js 18+)
- **Version Control:** Git (single-branch workflow per constitution Section 0.1.II)

## Consequences

### Positive

- **Zero infrastructure cost:** GitHub Pages free hosting eliminates operational expenses and scaling concerns
- **Academic-optimized tooling:** Docusaurus designed for documentation with built-in versioning, search, sidebar navigation
- **Progressive enhancement alignment:** Server-side rendered HTML works without JavaScript (constitution Section 0.1.IV)
- **Type safety:** TypeScript config prevents runtime errors in Docusaurus setup, catches plugin misconfigurations at build time
- **Mature ecosystem:** React-based, extensive plugin library (@docusaurus/theme-live-codeblock, Mermaid, etc.)
- **CI/CD automation:** GitHub Actions integrated with GitHub Pages, <5 minute deploy time
- **CDN performance:** GitHub Pages global CDN supports <2s page load requirement (SC-004)
- **No database complexity:** Content as MDX files in Git provides version control, no migration burden

### Negative

- **GitHub dependency:** 100% reliance on GitHub availability (mitigation: 95% SLA acceptable per spec SC-004)
- **Limited dynamic features:** Static site cannot support user authentication, commenting, or analytics without third-party integrations
- **Build time scaling:** Large sites (>500 pages) may exceed 60s build target (risk mitigation: textbook scope limited to 90-120 pages)
- **TypeScript learning curve:** Team must understand TypeScript config syntax (mitigation: official Docusaurus TypeScript guide, 30-minute debugging limit per constitution Section 0.2)
- **Plugin compatibility risk:** Third-party plugins may break across Docusaurus major versions (mitigation: lock to Docusaurus 3.x, test upgrades in isolated branch)
- **GitHub Pages HTTPS only:** No HTTP fallback, requires HTTPS-compatible browsers (acceptable: all modern browsers support HTTPS)

### Key Risks

**Risk 1: GitHub Pages Outage (P2)**
- **Likelihood:** Low (historical 99%+ uptime)
- **Impact:** Complete site unavailability during outage
- **Mitigation:** Document emergency deployment procedure to Vercel (can re-deploy Docusaurus build within 30 minutes)
- **Accepted Tradeoff:** Cost savings outweigh outage risk (spec allows 95% uptime)

**Risk 2: TypeScript Configuration Complexity Blocks Setup (P1)**
- **Likelihood:** Medium (common for first-time Docusaurus TypeScript users)
- **Impact:** Infrastructure setup delayed beyond 3-day Phase 0 target
- **Mitigation:** 30-minute debugging limit per constitution, fallback to JavaScript config if blocked
- **Kill Switch:** If TypeScript blocks >2 hours, revert to `docusaurus.config.js`

**Risk 3: Build Performance Degradation (P3)**
- **Likelihood:** Low (90-120 pages << 500 page threshold)
- **Impact:** CI/CD deploys exceed 5-minute target, developer experience degraded
- **Mitigation:** Lazy-load diagrams, disable unused plugins, monitor build time after Modules 0/3/6
- **Accepted Tradeoff:** Docusaurus SSG fast enough for 120-page scope

**Risk 4: Plugin Security Vulnerabilities (P2)**
- **Likelihood:** Low-Medium (npm ecosystem supply chain risk)
- **Impact:** XSS, dependency vulnerabilities flagged by Dependabot
- **Mitigation:** Use only official @docusaurus/* plugins where possible, audit third-party plugins with `npm audit`, pin versions in package.json
- **Rollback:** If critical vulnerability unfixable in 2 hours, disable plugin and use fallback (e.g., PNG diagrams instead of Mermaid)

## Alternatives Considered

### Alternative A: Jekyll + Markdown + GitHub Pages
**Components:** Jekyll (Ruby SSG), plain Markdown, GitHub Pages, Liquid templates

**Pros:** Native GitHub Pages integration, simpler than React, no Node.js dependency
**Cons:** No interactive code playgrounds (requirement FR-050), limited React component support, Ruby learning curve
**Key Risk:** Cannot support live code execution (blocking requirement)
**Rejected:** Fails FR-050 (code playground requirement)

### Alternative B: Hugo + Go Templates + Cloudflare Pages
**Components:** Hugo (Go SSG), Go templates, Cloudflare Pages deployment

**Pros:** Fastest SSG (1-5ms per page), single binary, no Node.js
**Cons:** Limited interactive features (no @docusaurus/theme-live-codeblock equivalent), steep templating syntax learning curve, no academic ecosystem
**Key Risk:** Custom code playground implementation required (8-12 hours estimated)
**Rejected:** Higher implementation cost, no time budget for custom playground (constitution Section 7.1)

### Alternative C: Next.js + MDX + Vercel
**Components:** Next.js 14, MDX, Vercel deployment, React components

**Pros:** Maximum flexibility, modern React features (App Router, Server Components), excellent DX
**Cons:** Over-engineered for static content (no API routes needed), higher complexity, Vercel vendor lock-in risk
**Key Risk:** Feature creep temptation (adding unnecessary API routes violates constitution Section 0.1.IV)
**Rejected:** Violates constitution Section 0.1 (Progressive Enhancement) - textbook does not need SSR or API routes

### Alternative D: Gatsby + GraphQL + Netlify
**Components:** Gatsby 5, GraphQL data layer, Netlify deployment

**Pros:** Strong plugin ecosystem, image optimization, React-based
**Cons:** GraphQL overkill for static content (no database queries needed), slower build times than Docusaurus, declining community momentum (fewer updates than Docusaurus)
**Key Risk:** GraphQL learning curve adds complexity without value (constitution Section 0.1.V: Explicit Over Implicit)
**Rejected:** GraphQL data layer unnecessary, slower builds

## Operational Impact

**Deployment Workflow:**
1. Content author commits MDX changes to `001-physical-ai-textbook` branch
2. GitHub Actions triggers on push
3. Build runs: `npm run build` (target <60s)
4. Lighthouse CI validates performance (target >85 score)
5. Deploy to GitHub Pages (target <5min total)
6. Verify deployment at `https://<username>.github.io/<repo-name>`

**Monitoring:**
- GitHub Actions workflow status (email notifications on failure)
- Lighthouse CI performance reports (automated)
- Manual WebPageTest after Modules 0, 3, 6 (spot-check)

**Rollback Procedure:**
- If deployment fails: Git revert last commit, re-trigger GitHub Actions
- If build broken: Identify failing MDX file via logs, fix syntax, re-push
- If infrastructure outage: Emergency deployment to Vercel (30-minute procedure documented in quickstart.md)

## Security & Compliance Impact

**Security Posture:**
- **Attack Surface:** Minimal (static HTML, no server-side code, no user input, no authentication)
- **XSS Risk:** Limited to Docusaurus plugin vulnerabilities (mitigation: official plugins only, npm audit)
- **Data Privacy:** Public content only (FR-020), no user data collected, no GDPR compliance burden
- **Supply Chain:** npm dependencies audited via Dependabot (GitHub automatic security alerts)
- **HTTPS:** Enforced by GitHub Pages (all traffic encrypted)

**Compliance:**
- **Open Access Requirement:** SC-007 requires 100% open-access citations (enforced via manual review checklist)
- **Academic Standards:** IEEE citation format enforced via CitationLink.tsx component
- **Accessibility:** Docusaurus meets WCAG 2.1 AA (default theme compliant)

## Consequences If Decision Fails

**Failure Scenario 1: GitHub Pages Permanently Unavailable**
- **Probability:** Very Low (<0.1% annually)
- **Response:** Migrate to Vercel (requires `vercel.json` config, 1-hour implementation)
- **Data Loss:** None (Git repository intact, static build portable)

**Failure Scenario 2: Docusaurus 3.x Reaches End-of-Life**
- **Probability:** Low (estimated 3-5 years support)
- **Response:** Upgrade to Docusaurus 4.x (breaking changes expected, 8-12 hour migration)
- **Mitigation:** Lock to Docusaurus 3.x LTS, delay upgrade until post-hackathon

**Failure Scenario 3: TypeScript Config Becomes Unmaintainable**
- **Probability:** Low
- **Response:** Convert to JavaScript config (2-hour task, backward compatible)
- **Impact:** Loss of type safety in config files (acceptable degradation)

**Reversal Cost:** Medium (8-12 hours to migrate to Next.js or Hugo)

## References

- Feature Spec: `/home/salim/Desktop/hackathine_1/specs/001-physical-ai-textbook/spec.md`
- Implementation Plan: `/home/salim/Desktop/hackathine_1/specs/001-physical-ai-textbook/plan.md` (lines 13-23, 158-164)
- Related ADRs: ADR-0002 (Content Authoring Workflow), ADR-0003 (Interactive Features Stack)
- Constitution Alignment: Section 0.1.IV (Progressive Enhancement), Section 0.2 (Decision Thresholds), Section 7.1 (Time Budget)
