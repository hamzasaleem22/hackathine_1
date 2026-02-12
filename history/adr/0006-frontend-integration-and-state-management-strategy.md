# ADR-0006: Frontend Integration and State Management Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Proposed
- **Date:** 2026-02-12
- **Feature:** 001-rag-chatbot
- **Context:** Integrating the RAG chatbot widget into an existing Docusaurus 3.9.2 textbook site with minimal disruption, ensuring proper state management, session persistence, and mobile responsiveness across all textbook pages.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - affects all future Docusaurus customizations, state patterns
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Redux, Zustand, Jotai vs React Context; different integration methods
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - impacts all pages, affects build process, deployment pipeline
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Adopt **Docusaurus Layout Swizzle + React Context + localStorage Session Management** as integrated frontend strategy:

**Integration Architecture:**
- **Docusaurus Customization:** Swizzle Layout component (`src/theme/Layout/index.tsx`), inject `<ChatbotWidget />` as global component
- **Component Structure:** ChatbotWidget (container) → MessageList, InputField, ChatbotButton (presentation)
- **Styling:** CSS Modules with Docusaurus theme variables (light/dark mode support)
- **Build Integration:** TypeScript components compiled with Docusaurus webpack config (no separate build)

**State Management:**
- **Chat State:** React Context (`ChatbotContext`) with `useChatbot()` hook
  - Messages array (max 50, circular buffer)
  - isOpen boolean (widget visibility)
  - isLoading boolean (API request in progress)
- **Session Management:** Custom `useSessionManager()` hook
  - sessionId generated on first use (UUID v4), stored in localStorage
  - 2-hour timeout tracked via lastActivity timestamp
  - 1-minute warning notification before expiry (FR-042)
- **Text Selection:** Custom `useTextSelection()` hook
  - Listens to `window.getSelection()` API
  - Detects selection >50 chars, shows "Ask about this" button
  - Passes selected text as context field to backend

**API Communication:**
- **HTTP Client:** Native `fetch()` with error handling (no axios dependency)
- **Retry Logic:** Exponential backoff (1s, 2s, 4s) for network failures
- **Timeout:** 30-second request timeout with AbortController
- **Environment Config:** `REACT_APP_API_URL` from `.env` (Vercel backend URL)

**Mobile Responsiveness:**
- **Breakpoint:** <768px triggers full-screen overlay (not floating widget)
- **Auto-Hide:** Chatbot minimizes on scroll down (FR-035), restores on scroll up
- **Touch Gestures:** Swipe-down from top closes chatbot (when scrolled to top of messages)
- **Keyboard Handling:** Virtual keyboard doesn't block input field (viewport height adjustment)

## Consequences

### Positive

- **Minimal Docusaurus disruption:** Swizzling Layout (official customization method) preserves upgrades, no core file modifications
- **React Context simplicity:** No Redux boilerplate, suitable for 3-5 state fields, aligns with "start simple" principle
- **localStorage persistence:** Session survives page navigation, no backend session store needed, works offline
- **Native fetch benefits:** Zero dependencies, smaller bundle (<100KB target), browser-native error handling
- **CSS Modules isolation:** Styles scoped to chatbot, no conflicts with Docusaurus theme, supports light/dark mode
- **Progressive enhancement:** Chatbot fails gracefully if JavaScript disabled (Docusaurus content still readable)
- **Mobile-first design:** Full-screen overlay on mobile avoids positioning issues, auto-hide improves reading experience
- **Type safety:** TypeScript catches prop mismatches, API contract errors at compile time

### Negative

- **Swizzling maintenance burden:** Docusaurus major version upgrades may break swizzled Layout, requires migration testing
- **React Context performance:** Re-renders all consumers on state change (acceptable for 3-5 fields, problematic if >10)
- **localStorage size limits:** 5-10MB browser limit (50 messages × 1KB = 50KB, sufficient but not infinite)
- **No server-side rendering:** Session state only available client-side (acceptable: chatbot is client-only feature)
- **Native fetch limitations:** No automatic JSON serialization (manual JSON.stringify), no request interceptors
- **Text selection fragility:** `window.getSelection()` API inconsistent across browsers (Safari iOS requires workarounds)
- **Mobile gesture conflicts:** Swipe-down gesture may conflict with native browser pull-to-refresh (mitigation: disable when chatbot open)
- **Timeout warning complexity:** 1-minute countdown requires setInterval (potential memory leak if not cleaned up properly)

### Key Risks

**Risk 1: Swizzled Layout Breaks on Docusaurus Upgrade (P2)**
- **Likelihood:** Medium (Docusaurus 3 → 4 migration expected in 1-2 years)
- **Impact:** Chatbot widget disappears after upgrade, 2-4 hours re-swizzling required
- **Mitigation:** Lock Docusaurus to 3.x LTS, test upgrades in separate branch before deploying
- **Fallback:** Inject chatbot via `<script>` tag in custom HTML (less clean but upgrade-proof)

**Risk 2: React Context Performance Degradation (P3)**
- **Likelihood:** Low (3-5 state fields below React Context performance cliff)
- **Impact:** UI lag when sending messages, poor UX on low-end devices
- **Mitigation:** Measure re-render count in Phase 3 testing, split context if >10 fields added
- **Fallback:** Migrate to Zustand (lightweight, <1KB, minimal migration effort)

**Risk 3: localStorage Quota Exceeded (P3)**
- **Likelihood:** Very Low (50 messages = 50KB << 5MB limit)
- **Impact:** Session data write failures, messages not persisted
- **Mitigation:** 50-message circular buffer (delete oldest when full), clear history on "Clear Chat" button
- **Accepted Tradeoff:** 5MB limit sufficient for 100+ sessions

**Risk 4: Text Selection Fails on Safari iOS (P2)**
- **Likelihood:** Medium (Safari selection API quirks documented)
- **Impact:** Selected-text feature non-functional for 15-20% of mobile users (iOS Safari market share)
- **Mitigation:** Test on iOS Safari early (Phase 4), implement fallback "Paste Text" button if native selection broken
- **Fallback:** Manual text paste via input field (degrades UX but maintains functionality)

**Risk 5: Virtual Keyboard Blocks Input Field (P2)**
- **Likelihood:** Medium (common mobile web issue)
- **Impact:** Users cannot see input field when typing, poor mobile UX
- **Mitigation:** Use `visualViewport.height` API to adjust chat container height dynamically
- **Fallback:** Scroll input field into view on focus (less elegant but functional)

## Alternatives Considered

### Alternative A: Redux + Redux Toolkit for State Management
**Components:** Redux store, Redux Toolkit slices, useSelector/useDispatch hooks

**Pros:** Scalable to 20+ state fields, time-travel debugging, dev tools, industry standard
**Cons:** Redux boilerplate (actions, reducers, store config) overkill for 3-5 fields, 8-12 hour learning curve for team, +15KB bundle size
**Key Risk:** Over-engineering violates "start simple" principle, complexity vs benefit unclear
**Rejected:** React Context sufficient for MVP, Redux deferred until >10 state fields needed

### Alternative B: Zustand for State Management
**Components:** Zustand store (lightweight Redux alternative), create() API, vanilla JS integration

**Pros:** Minimal boilerplate (vs Redux), <1KB bundle, no Context re-render issues, TypeScript-friendly
**Cons:** Less familiar than React Context, external dependency, migration effort if switching to Redux later
**Key Risk:** Team unfamiliarity adds learning curve (2-4 hours)
**Rejected:** React Context simpler for 3-5 fields, Zustand viable fallback if performance issues

### Alternative C: Custom `<script>` Tag Injection (No Swizzling)
**Components:** Vanilla JS chatbot injected via `docusaurus.config.ts` scripts array, no React integration

**Pros:** Upgrade-proof (no swizzling), works with any SSG (not Docusaurus-specific), zero Docusaurus coupling
**Cons:** Loses React component benefits (hooks, TypeScript, CSS Modules), harder to maintain (vanilla DOM manipulation), no SSR support
**Key Risk:** Vanilla JS complexity increases for complex UI (50+ messages, loading states, etc.)
**Rejected:** React component architecture cleaner, swizzling risk acceptable

### Alternative D: Separate Chatbot App (iframe Embed)
**Components:** Standalone React app for chatbot, embedded via `<iframe>` in Docusaurus

**Pros:** Complete isolation (no state conflicts), independent deployment, can use any framework (not tied to Docusaurus React)
**Cons:** iframe sandboxing blocks localStorage sharing, cross-origin communication complex (postMessage), 2x bundle size (separate React instance)
**Key Risk:** Session persistence broken across Docusaurus pages (iframes don't share localStorage)
**Rejected:** localStorage isolation breaks session persistence, complexity too high

### Alternative E: Jotai for Atomic State Management
**Components:** Jotai atoms (atomic state units), useAtom hooks, fine-grained reactivity

**Pros:** Atomic updates (no unnecessary re-renders), TypeScript-first, lighter than Redux (<5KB)
**Cons:** Less familiar than React Context, atoms proliferate quickly (harder to track state), learning curve
**Key Risk:** Atomic model overkill for flat state structure (messages, isOpen, isLoading)
**Rejected:** React Context simpler for flat state, Jotai benefits unclear for this use case

## References

- Feature Spec: `/home/salim/Desktop/hackathine_1/specs/001-rag-chatbot/spec.md` (User Story 1-3, FR-014 to FR-028, FR-032, FR-035, FR-040, FR-042, SC-012, SC-015)
- Implementation Plan: `/home/salim/Desktop/hackathine_1/specs/001-rag-chatbot/plan.md` (lines 143-198: Phase 3 Frontend Widget, lines 199-220: Phase 4 Selected Text)
- Related ADRs: ADR-0004 (Backend Stack - Vercel API endpoint), ADR-0005 (RAG Architecture - API contract for query endpoint)
- Constitution Alignment: Section 0.1.IV (Progressive Enhancement - chatbot fails gracefully), Section 0.1.V (Explicit Over Implicit - React Context over magic abstractions)
