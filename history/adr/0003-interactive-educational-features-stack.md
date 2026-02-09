# ADR-0003: Interactive Educational Features Stack

- **Status:** Accepted
- **Date:** 2026-02-09
- **Feature:** Physical AI & Humanoid Robotics Educational Textbook
- **Context:** Educational textbook requiring browser-based Python code execution, C4/Mermaid diagrams, IEEE citation formatting, 3-5 diagrams per chapter, 30-second code timeout, progressive enhancement (content readable without JavaScript)

## Decision

Adopt **Browser-Based Interactive Stack** with static fallbacks for progressive enhancement:

**Interactive Code Execution:**
- **Plugin:** @docusaurus/theme-live-codeblock (official Docusaurus plugin)
- **Runtime:** Pyodide (Python 3.x in WebAssembly, browser-sandboxed)
- **Timeout:** 30 seconds enforced (FR-051)
- **Fallback:** Static syntax-highlighted code blocks (no execution) if JavaScript disabled

**Diagram Rendering:**
- **Primary:** Mermaid.js (flowcharts, sequence diagrams, class diagrams)
- **Secondary:** Structurizr plugin (C4 architecture diagrams for system overviews)
- **Tertiary:** draw.io integration (complex robotics illustrations)
- **Fallback:** PNG/SVG exports committed to `/static/img/` (lazy-loaded, <100KB per image)

**Citation System:**
- **Component:** CitationLink.tsx (custom React component)
- **Format:** IEEE style enforcement (superscript numbers, footnote links)
- **Validation:** Open-access URL verification during review checklist (SC-007)
- **Fallback:** Plain markdown footnote links (works without React)

**Performance:**
- Lazy loading for below-fold diagrams
- Code playground initializes on user interaction (not on page load)
- Image optimization via TinyPNG (<100KB per image)
- Target: <2s page load (SC-004)

## Consequences

### Positive

- **Browser-sandboxed execution:** No server-side code execution eliminates security risks (XSS, code injection), read-only filesystem prevents malicious modifications
- **Official Docusaurus plugins:** @docusaurus/theme-live-codeblock maintained by Meta, reduces maintenance burden
- **Progressive enhancement:** Static fallbacks ensure content readable without JavaScript (constitution Section 0.1.IV)
- **Zero backend cost:** All execution browser-side, no Lambda/serverless functions needed
- **Diagram versioning:** Mermaid code committed to Git (versioned), PNG fallbacks provide portability
- **Academic citation standard:** IEEE format matches university requirements (SC-007)
- **Performance budget:** <100KB images + lazy loading supports <2s page load (SC-004)

### Negative

- **Browser compatibility:** Pyodide requires WebAssembly (unavailable in IE11, older mobile browsers) - acceptable: 95%+ modern browser support
- **Code execution limitations:** Pyodide cannot run ROS 2 native code (C++), only pure Python - acceptable: examples demonstrate concepts, not production code
- **30-second timeout constraint:** Complex simulations cannot run in browser (e.g., Gazebo simulations) - mitigation: static screenshots or video demonstrations
- **Diagram rendering performance:** Mermaid can slow page load if 5+ diagrams on one page - mitigation: PNG fallbacks for complex diagrams
- **Plugin dependency risk:** @docusaurus/theme-live-codeblock breaking changes require migration - mitigation: lock to major version, test upgrades before deploying
- **Citation maintenance:** Manual URL validation required (no automated accessibility checks) - mitigation: 12-point checklist includes citation validation

### Key Risks

**Risk 1: Pyodide Unavailable in Target Browsers (P2)**
- **Likelihood:** Low (WebAssembly 97%+ browser support)
- **Impact:** Code playgrounds non-functional for <3% users
- **Mitigation:** Graceful degradation to static code blocks with "Run this code locally" instructions
- **Accepted Tradeoff:** 3% user impact acceptable for 97% interactive experience

**Risk 2: Code Playground Security Vulnerability (P1)**
- **Likelihood:** Very Low (browser sandbox + 30s timeout)
- **Impact:** XSS or denial-of-service attack via malicious code examples
- **Mitigation:** Pyodide sandboxed (no network access, no file system writes), timeout enforced, code examples human-reviewed before publication
- **Kill Switch:** Disable @docusaurus/theme-live-codeblock plugin if critical vulnerability found (fallback: static code blocks)

**Risk 3: Diagram Rendering Failure Breaks Page Load (P2)**
- **Likelihood:** Low-Medium (Mermaid syntax errors cause render failures)
- **Impact:** Blank page or broken layout if diagram fails to render
- **Mitigation:** PNG/SVG fallbacks for all diagrams (committed to `/static/img/`), test all diagrams before commit
- **Fallback:** If Mermaid breaks, replace with `<img src="/img/diagram.png" />` in MDX

**Risk 4: Citation URL Rot (Links Die Over Time) (P3)**
- **Likelihood:** Medium (academic papers move, journals reorganize URLs)
- **Impact:** 12-point validation fails if >20% citations inaccessible
- **Mitigation:** Prefer DOI links (persistent identifiers), use Wayback Machine snapshots for non-DOI sources
- **Accepted Tradeoff:** Some URL rot expected over 3-5 years, acceptable for v1.0

**Risk 5: Performance Degradation (Slow Code Playground Init) (P2)**
- **Likelihood:** Medium (Pyodide ~10MB download on first load)
- **Impact:** First code playground interaction takes 5-10 seconds, degrades UX
- **Mitigation:** Lazy-load Pyodide (only download when user clicks "Run"), browser caching amortizes cost across pages
- **Accepted Tradeoff:** First-run delay acceptable for subsequent fast execution

## Alternatives Considered

### Alternative A: Server-Side Code Execution (Lambda/Cloud Functions)
**Components:** AWS Lambda (Python 3.x runtime), API Gateway, code execution service

**Pros:** No browser compatibility issues, can run ROS 2 native code (C++), no WebAssembly dependency
**Cons:** Security risk (arbitrary code execution), cost ($50-200/month for 500 concurrent users), 2-hour debugging limit per constitution Section 0.2, requires backend infrastructure (violates ADR-0001 static site decision)
**Key Risk:** Code injection vulnerability, expensive at scale, violates static site architecture
**Rejected:** Security risk too high, cost prohibitive, adds backend complexity

### Alternative B: Static Code Blocks Only (No Interactive Execution)
**Components:** Syntax highlighting only (Prism.js or highlight.js), no execution

**Pros:** Maximum security (no code execution), zero performance overhead, 100% browser compatible
**Cons:** Fails FR-050 (code playground requirement), worse learning experience (students cannot experiment)
**Key Risk:** Misses interactive learning goal, reduces textbook value
**Rejected:** Blocking requirement (FR-050 mandates code execution)

### Alternative C: JupyterLab Embed (Full Notebook Environment)
**Components:** JupyterLab embedded iframe, Jupyter server (Binder or MyBinder.org)

**Pros:** Full Python environment with package installation (pip), industry-standard data science tool
**Cons:** Heavy (15-30 second load time per notebook), requires external Binder service (uptime risk), complex setup, violates 30-second timeout (FR-051)
**Key Risk:** Binder outage breaks all code playgrounds, load time exceeds performance budget
**Rejected:** Too slow, external dependency risk, over-engineered for simple examples

### Alternative D: CodeSandbox/StackBlitz Embed
**Components:** CodeSandbox or StackBlitz iframe embeds, cloud-based IDE

**Pros:** Professional IDE experience, supports package installation, debugging tools
**Cons:** External service dependency (CodeSandbox outage breaks all examples), requires account creation for editing (violates "no authentication" per FR-020), heavy embeds (slow page load)
**Key Risk:** Service outage, privacy concerns (user tracking), performance impact
**Rejected:** External dependency risk, slower than Pyodide, privacy concerns

### Alternative E: Custom WebAssembly Execution Engine
**Components:** Custom-built Python interpreter in WebAssembly, bespoke sandbox

**Pros:** Full control over execution environment, optimized for textbook use cases
**Cons:** 20-40 hour implementation effort (exceeds 107h project budget), untested security, maintenance burden, reinventing wheel
**Key Risk:** Implementation timeline risk, security vulnerabilities in custom code
**Rejected:** Time budget exceeded, security risk, Pyodide already solves problem

## Operational Impact

**Code Playground Workflow:**
1. Author writes Python code examples in MDX using `@docusaurus/theme-live-codeblock` syntax
2. Test code locally: `npm run build && npm run serve`
3. Verify execution completes <30 seconds (manual testing)
4. Validation checklist: "Do all code examples execute correctly?" (FR-029)
5. Deploy to GitHub Pages (code runs in user's browser, no server execution)

**Diagram Workflow:**
1. Author writes Mermaid diagram code in MDX (fenced code block with `mermaid` language tag)
2. Test rendering locally: `npm start` (hot reload shows diagram)
3. Export PNG fallback: Use Mermaid Live Editor → Export → Save to `/static/img/`
4. Add fallback: `![Diagram fallback](/img/diagram-name.png)` below Mermaid code
5. Validation checklist: "Are diagrams captioned with figure numbers?" (FR-029)

**Citation Workflow:**
1. Author adds citation in IEEE format to `docs/references.md`
2. Link from text: `[^1]` inline reference
3. Validation checklist: "Do citations include accessible URLs/DOIs?" (FR-029)
4. Manual test: Click each citation URL, verify open-access (SC-007)

**Monitoring:**
- **Code Playground Performance:** Track first-run init time after Module 0 deployment (target <10s first load, <2s cached)
- **Diagram Rendering:** Manual visual inspection before commit (no automated tests)
- **Citation Accessibility:** Manual check during validation (no automated link checker)

## Security & Compliance Impact

**Code Execution Security:**
- **Attack Surface:** Browser-sandboxed (Pyodide cannot access file system, network, or DOM)
- **Denial of Service:** 30-second timeout prevents infinite loops, browser tab crash at worst (no server impact)
- **XSS Risk:** Minimal (Pyodide output sanitized by @docusaurus/theme-live-codeblock)
- **Malicious Code:** Human review of all code examples prevents malicious insertions
- **Data Exfiltration:** Impossible (no network access, read-only filesystem)

**Privacy:**
- **No Tracking:** Code execution entirely local, no analytics on code run (unless Docusaurus analytics enabled separately)
- **No User Data:** Code examples do not collect or process user input

**Accessibility:**
- **Keyboard Navigation:** Docusaurus default theme WCAG 2.1 AA compliant
- **Screen Readers:** Static code fallbacks readable by screen readers
- **Color Contrast:** Diagrams use high-contrast colors (validation during review)

**Academic Integrity:**
- **Citation Format:** IEEE style enforced via CitationLink.tsx component
- **Open Access:** SC-007 requires 100% accessible citations (manual validation)
- **Plagiarism:** Diagrams original (created via Mermaid/draw.io, not copied)

## Consequences If Decision Fails

**Failure Scenario 1: Pyodide Critical Vulnerability Found**
- **Probability:** Very Low (<1% annually)
- **Response:** Disable @docusaurus/theme-live-codeblock plugin immediately, fallback to static code blocks
- **Impact:** Loss of interactive feature, textbook still functional
- **Reversal Cost:** Low (1-hour plugin disable, add "Run locally" instructions)

**Failure Scenario 2: Mermaid Rendering Breaks Across All Pages**
- **Probability:** Low (Mermaid stable library)
- **Response:** Replace Mermaid diagrams with PNG fallbacks (already committed to `/static/img/`)
- **Impact:** Diagrams static instead of editable, still functional
- **Reversal Cost:** Low (2-hour find-and-replace to swap Mermaid code with `<img>` tags)

**Failure Scenario 3: Citation Links Mass Rot (>50% Die)**
- **Probability:** Low (DOI links persistent)
- **Response:** 4-hour research blitz to find alternative URLs or Wayback Machine snapshots
- **Impact:** Validation fails if >50% citations inaccessible
- **Reversal:** Use framework documentation only (ROS 2, NVIDIA, Unity official docs)

**Failure Scenario 4: Code Playground Performance Unacceptable (>15s Init)**
- **Probability:** Low-Medium (Pyodide ~10MB download)
- **Response:** Disable autoload, require user to click "Initialize Python Environment" button
- **Impact:** Extra user action required, acceptable degradation
- **Reversal Cost:** Low (1-hour config change)

**Failure Scenario 5: @docusaurus/theme-live-codeblock Breaking Change in Docusaurus 4.x**
- **Probability:** Medium (major version upgrades often break plugins)
- **Response:** Lock to Docusaurus 3.x LTS, delay upgrade until post-hackathon
- **Impact:** Delayed feature updates, security patches may lag
- **Reversal:** Migrate to Alternative B (static code blocks only) if plugin abandoned

**Reversal Cost:** Low-Medium (2-8 hours to switch to static fallbacks)

## References

- Feature Spec: `/home/salim/Desktop/hackathine_1/specs/001-physical-ai-textbook/spec.md` (FR-011, FR-042, FR-050, FR-051, SC-004, SC-007)
- Implementation Plan: `/home/salim/Desktop/hackathine_1/specs/001-physical-ai-textbook/plan.md` (lines 115-133: Source Code Structure, lines 186-198: Research Questions)
- Related ADRs: ADR-0001 (Static Site Architecture - no backend execution), ADR-0002 (Content Workflow - diagram/code validation)
- Constitution Alignment: Section 0.1.IV (Progressive Enhancement - static fallbacks), Section 0.2 (2-hour debugging limit for tooling), Section 8.2 (Testing - manual validation)
