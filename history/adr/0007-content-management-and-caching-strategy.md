# ADR-0007: Content Management and Caching Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Proposed
- **Date:** 2026-02-12
- **Feature:** 001-rag-chatbot
- **Context:** Managing textbook content lifecycle (initial indexing, incremental updates, version tracking) and optimizing OpenAI API costs through caching (query cache, embedding cache) to reduce $39/month baseline to $20-25/month while maintaining answer quality.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - affects content update workflow, cost management, operational complexity
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - full re-index vs incremental, Redis vs in-memory, different cache strategies
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - impacts indexing pipeline, API layer, monitoring, cost control
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Adopt **Git-Based Incremental Indexing + Python LRU Cache + 24-Hour TTL** as integrated content and caching strategy:

**Content Indexing & Updates (FR-036):**
- **Initial Index:** Full MDX file scan on first deployment (Phase 1), ~30-45 minutes for Module 0
- **Change Detection:** Git diff against last indexed commit (`git diff <commit-hash> HEAD -- frontend/docs/`)
- **Incremental Re-Index:** Process only changed files (5-10 minutes for 1-2 chapters vs 30+ for full re-index)
- **Upsert Strategy:** Qdrant upsert by document ID (replaces existing chunks, not append)
- **Version Tracking:** Store `content_version` (semantic version), `git_commit` hash, `indexed_at` timestamp in Qdrant metadata
- **Invalidation:** Clear query cache when content version changes (event-based invalidation)

**Query Caching (30-50% cost reduction):**
- **Implementation:** Python `functools.lru_cache` (in-memory, per Vercel instance)
- **Cache Key:** `hash(question_text.lower().strip())` (normalized for case/whitespace)
- **Cache Value:** JSON object with `{answer, citations, confidence, cached_at, ttl}`
- **TTL:** 24 hours (time-based expiration, balances freshness vs cost)
- **Max Size:** 128 entries (128 × 2KB = 256KB RAM per instance, acceptable for serverless)
- **Invalidation:** Automatic TTL expiry + manual `/api/cache/clear` endpoint (admin only)

**Embedding Cache:**
- **Strategy:** Store question embeddings in Qdrant "question_cache" collection (separate from content)
- **Benefit:** Avoid re-embedding identical questions (saves 50% embedding costs for repeat queries)
- **Lookup:** Hash question → search question_cache collection → return cached vector if exists
- **Fallback:** Generate new embedding if not cached, store for future use
- **Size:** ~1KB per cached question embedding (1000 cached questions = 1MB << 1GB Qdrant limit)

**Content Versioning UI (FR-037):**
- **Display:** Chatbot footer shows "Content last updated: Feb 12, 2026 (Module 0 v1.2)"
- **Data Source:** `/api/content-status` endpoint returns `{last_updated, content_version, indexed_modules, total_chunks}`
- **New Module Banner (FR-039):** When `indexed_modules` array changes, show banner: "🎉 Module 1: ROS 2 now searchable!"
- **Dismiss:** localStorage flag `dismissed_module_1_banner` (per-user, per-module)

## Consequences

### Positive

- **Incremental indexing efficiency:** 5-10 minutes for content updates (vs 30+ for full re-index), enables frequent updates
- **Git-based tracking:** Leverages existing version control, no separate change tracking system needed, audit trail built-in
- **Cost optimization:** Query cache 30-50% savings, embedding cache 50% savings on repeat questions (target: $20-25/month from $39 baseline)
- **Zero external dependencies:** Python LRU cache built-in (no Redis), Qdrant handles embedding cache (no separate storage)
- **Content version transparency:** Users see when content updated (builds trust), admin can correlate answers with content version
- **Graceful cache invalidation:** TTL-based expiry prevents stale answers, event-based clear on content updates ensures accuracy
- **Serverless-friendly:** In-memory LRU cache per Vercel instance (no shared state needed), 256KB RAM << 512MB limit

### Negative

- **Git dependency:** Incremental indexing requires Git repo, manual uploads (not via CMS) won't trigger re-index
  - Mitigation: All content updates via Git (enforced workflow), no manual Qdrant uploads allowed
- **LRU cache per-instance limitation:** Vercel spins up multiple instances, each has separate cache (30-40% hit rate vs 50-60% with Redis)
  - Accepted Tradeoff: Redis adds $5-10/month cost + complexity, LRU cache sufficient for free tier
- **24-hour TTL tradeoff:** Stale answers possible if content updated mid-day (users see old answers for up to 24h)
  - Mitigation: Event-based cache clear on content updates, manual `/api/cache/clear` if urgent
- **Embedding cache storage:** 1000 cached questions = 1MB, 10K questions = 10MB (approaching Qdrant 1GB limit faster)
  - Mitigation: Set max 5K cached embeddings, LRU eviction policy (delete oldest if full)
- **Manual re-index trigger:** No GitHub Action automation (Phase 1 scope), requires manual script execution
  - Accepted Tradeoff: Automation deferred to Phase 7, manual workflow acceptable for MVP
- **Upsert complexity:** Must maintain consistent document IDs across re-indexes (e.g., `module-0-chapter-1-section-2`), ID collisions break updates
  - Mitigation: Generate IDs from file path + heading structure (deterministic, no random UUIDs)

### Key Risks

**Risk 1: Git Diff Misses Content Changes (P2)**
- **Likelihood:** Low-Medium (Git diff reliable for file changes, but complex renames may confuse)
- **Impact:** Content updated but not re-indexed, chatbot gives outdated answers
- **Mitigation:** Test incremental workflow with Module 0 updates in pilot phase, validate re-indexed chunks match new content
- **Kill Switch:** If incremental fails, fallback to full re-index (30+ minutes acceptable if rare)

**Risk 2: Cache Hit Rate Lower Than Expected (<20%) (P2)**
- **Likelihood:** Medium (depends on query diversity)
- **Impact:** Cost savings only 10-15% (not 30-50%), budget at risk
- **Mitigation:** Measure cache hit rate in Phase 2 testing (20 sample questions), adjust cache strategy if <20%
- **Fallback:** Upgrade to Redis (Upstash free tier 10K requests/day) if LRU cache insufficient

**Risk 3: Stale Answers Due to 24h TTL (P3)**
- **Likelihood:** Low (content updates infrequent, ~1-2x per module)
- **Impact:** Users get outdated answers for up to 24 hours after content update
- **Mitigation:** Document cache clear procedure in runbook, add "Content updated" notice in chatbot UI
- **Accepted Tradeoff:** 24h staleness acceptable for educational content (not time-critical)

**Risk 4: Document ID Collisions During Re-Index (P1)**
- **Likelihood:** Medium (deterministic ID generation brittle if file structure changes)
- **Impact:** Upsert fails, old chunks not replaced, duplicate content in Qdrant
- **Mitigation:** Test ID generation with Module 0, validate no collisions, add uniqueness assertion in indexing script
- **Fallback:** Delete entire Qdrant collection and full re-index (30-45 minutes downtime)

**Risk 5: Embedding Cache Grows Beyond 1GB Qdrant Limit (P3)**
- **Likelihood:** Very Low (10K cached questions = 10MB << 1GB)
- **Impact:** Qdrant write failures, embedding cache disabled
- **Mitigation:** Set max 5K cached embeddings with LRU eviction, monitor Qdrant storage via dashboard
- **Fallback:** Disable embedding cache, fall back to OpenAI API for all embeddings (cost increase acceptable)

## Alternatives Considered

### Alternative A: Full Re-Index on Every Content Update (No Incremental)
**Components:** Delete Qdrant collection, re-index all MDX files, no change detection

**Pros:** Simpler implementation (no Git diff logic), guaranteed consistency (no upsert bugs), no document ID management
**Cons:** 30-45 minutes downtime per update (chatbot unavailable), higher OpenAI embedding costs (re-embed unchanged content), discourages frequent updates
**Key Risk:** Long downtime unacceptable for production (users blocked from asking questions)
**Rejected:** Incremental indexing essential for frequent content updates, downtime too high

### Alternative B: Redis Cache (Upstash or Vercel KV)
**Components:** Redis for query cache + embedding cache, shared across Vercel instances

**Pros:** Higher cache hit rate (50-60% vs 30-40% LRU), persistent across deployments, shared state across instances
**Cons:** External dependency (Upstash $5-10/month or Vercel KV $10/month), network latency (Redis query adds 10-50ms), complexity (connection management, error handling)
**Key Risk:** Cost increase offsets cache savings (save $10-15 on OpenAI, spend $5-10 on Redis)
**Rejected:** LRU cache sufficient for MVP, Redis deferred to Phase 7 if hit rate insufficient

### Alternative C: Webhook-Triggered Re-Index (GitHub Actions)
**Components:** GitHub Action triggers on push to main, runs indexing script, deploys updated Qdrant

**Pros:** Fully automated (no manual script execution), immediate content updates (no delay), CI/CD integration
**Cons:** 12-20 hour implementation (GitHub Actions workflow, secret management, error handling), requires Vercel/Qdrant credentials in GitHub Secrets
**Key Risk:** Automation complexity high, Phase 1 scope constraint (automation deferred to Phase 7)
**Rejected:** Manual workflow acceptable for MVP, automation valuable but not critical path

### Alternative D: CMS-Based Content Management (Contentful, Sanity)
**Components:** Headless CMS stores textbook content, webhook triggers re-index on content save

**Pros:** Non-technical editors can update content (no Git), visual editing UI, versioning built-in
**Cons:** Requires content migration from MDX to CMS (8-12 hours), CMS learning curve, external dependency (CMS pricing tiers)
**Key Risk:** Migration effort too high, loses MDX benefits (React components, code examples)
**Rejected:** MDX + Git workflow already established, CMS unnecessary for single-author project

### Alternative E: CDN Edge Caching (Cloudflare Workers KV)
**Components:** Cache OpenAI responses at CDN edge, geographically distributed

**Pros:** Global cache (low latency worldwide), higher hit rates (shared across all users globally), CDN-native
**Cons:** Cloudflare Workers KV complexity (Workers script, KV bindings), vendor lock-in (Cloudflare-specific), cost ($5/month KV minimum)
**Key Risk:** Complexity vs benefit unclear for single-region users (GitHub Pages US-centric)
**Rejected:** LRU cache simpler, edge caching overkill for educational use case (not global scale)

## References

- Feature Spec: `/home/salim/Desktop/hackathine_1/specs/001-rag-chatbot/spec.md` (FR-036, FR-037, FR-038, FR-039, Cost Analysis section)
- Implementation Plan: `/home/salim/Desktop/hackathine_1/specs/001-rag-chatbot/plan.md` (lines 408-436: Cost Analysis, lines 722-834: Content Update Workflow, Cache Strategy)
- Related ADRs: ADR-0004 (Backend Stack - Vercel serverless, Qdrant), ADR-0005 (RAG Architecture - embedding model)
- Constitution Alignment: Section 0.1.V (Explicit Over Implicit - Git diff over magic CMS), Section 7.1 (Time Budget - automation deferred to Phase 7)
