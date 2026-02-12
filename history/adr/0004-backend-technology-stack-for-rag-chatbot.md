# ADR-0004: Backend Technology Stack for RAG Chatbot

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Proposed
- **Date:** 2026-02-12
- **Feature:** 001-rag-chatbot
- **Context:** Building a production-ready RAG chatbot for the Physical AI textbook that must handle semantic search, LLM-powered answers, chat logging, and serverless deployment with zero existing backend infrastructure.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - defines entire backend architecture
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Django/Express, Redis/Upstash, different vector stores
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - affects all backend development, deployment, cost, scaling
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Adopt **FastAPI + OpenAI + Qdrant Cloud + Neon Postgres + Vercel Serverless** as integrated backend stack:

**Core Components:**
- **API Framework:** FastAPI (Python 3.11+, async-first, type hints)
- **LLM Provider:** OpenAI (gpt-4o-mini for completions, text-embedding-3-small for embeddings)
- **Vector Database:** Qdrant Cloud Free Tier (1GB storage, cosine similarity, 1536 dimensions)
- **Relational Database:** Neon Serverless Postgres (chat logging, analytics, 512MB free tier)
- **Deployment Platform:** Vercel Serverless Functions (Python runtime, CORS-enabled for GitHub Pages)
- **Dependencies:** uvicorn, openai SDK, qdrant-client, psycopg2-binary

**Key Configuration:**
- Rate limiting: 20 requests/minute per IP (in-memory sliding window)
- Timeout: 30 seconds per request (Vercel free tier: 10s, mitigation via streaming)
- CORS: Whitelist `msaleemakhtar.github.io` origin only

## Consequences

### Positive

- **Zero infrastructure management:** Vercel serverless + cloud databases eliminate DevOps burden, auto-scaling included
- **Python ecosystem alignment:** FastAPI enables rapid RAG prototyping, OpenAI SDK mature, Qdrant client well-documented
- **Cost efficiency:** Free tiers sufficient for MVP (Qdrant 1GB = ~100K chunks, Neon 512MB = ~50K messages, Vercel 100GB bandwidth)
- **Type safety:** FastAPI Pydantic models catch API contract errors at development time
- **Async-first design:** FastAPI async/await handles concurrent queries efficiently (target: 50+ concurrent users)
- **GitHub integration:** Vercel auto-deploys from Git, no manual deployment steps
- **OpenAI reliability:** 99.9% uptime SLA, rate limits sufficient (3000 RPM embeddings, 10K RPM completions)
- **Qdrant performance:** Sub-100ms vector search at <100K vectors, cloud-managed backups

### Negative

- **Vendor lock-in risk:** Heavy reliance on OpenAI (embeddings, completions) and Vercel (serverless runtime) - switching costs 12-20 hours
- **Vercel 10-second timeout:** Free tier limits complex queries, may require streaming responses or upgrade to Pro ($20/month)
- **No Redis caching:** In-memory rate limiting not distributed across Vercel instances, cache hit rates lower than Redis-based solution
- **Cold start latency:** Vercel cold starts 1-3 seconds, impacts first query per user (mitigation: keep-alive pings)
- **OpenAI cost scaling:** $39/month @ 1000 queries/day, scales linearly - high usage requires aggressive caching (30-50% savings target)
- **Qdrant free tier limits:** 1GB storage = ~100K chunks, insufficient for 6-module textbook expansion (mitigation: chunking optimization)
- **Postgres connection pooling:** Neon free tier limited to 10 connections, requires careful pool management
- **Python cold start:** Slower than Node.js serverless (mitigation: minimal dependencies)

### Key Risks

**Risk 1: OpenAI API Cost Overrun (P1)**
- **Likelihood:** Medium (viral usage spikes)
- **Impact:** $200+/month bills, budget crisis
- **Mitigation:** OpenAI budget alerts at $20/month, implement query caching (30-50% cost reduction), rate limiting enforced
- **Kill Switch:** If costs exceed $50/month, disable chatbot with maintenance message

**Risk 2: Vercel Timeout Blocks Complex Queries (P2)**
- **Likelihood:** Medium (free tier 10s limit, target 95% queries <5s)
- **Impact:** 429 errors for 5-10% of queries, poor UX
- **Mitigation:** Optimize embedding batch size (100/call), implement streaming responses, consider Vercel Pro upgrade
- **Fallback:** Migrate to Railway or Render (15-30 minute timeout limits)

**Risk 3: Qdrant Free Tier Storage Exhausted (P2)**
- **Likelihood:** Low (Module 0 = ~500 chunks, 6 modules = ~3K chunks << 100K limit)
- **Impact:** Cannot index new content without upgrading ($25/month minimum)
- **Mitigation:** Aggressive chunking (target 500-1000 chunks per module), delete test data regularly
- **Accepted Tradeoff:** Free tier sufficient for 5-6 modules

**Risk 4: Neon Postgres Connection Pool Exhaustion (P3)**
- **Likelihood:** Low (10 connections sufficient for 50 concurrent users with short queries)
- **Impact:** Database errors, failed chat logging
- **Mitigation:** Connection pooling with psycopg2.pool, short-lived connections, async queries
- **Fallback:** Disable chat logging temporarily (chatbot still functional)

## Alternatives Considered

### Alternative Stack A: Django + Anthropic Claude + Pinecone + Supabase + Railway
**Components:** Django REST Framework, Claude API, Pinecone vector DB, Supabase Postgres, Railway deployment

**Pros:** Django batteries-included (admin panel, ORM), Anthropic strong on safety, Pinecone auto-scaling, Supabase generous free tier
**Cons:** Django slower than FastAPI (sync-first), Anthropic API more expensive ($15/1M tokens vs OpenAI $10/1M), Pinecone no free tier ($70/month minimum), Railway 500 hours free tier insufficient
**Key Risk:** Cost prohibitive (Pinecone + Railway = $90+/month)
**Rejected:** Exceeds free tier budget, Django overkill for 3 endpoints

### Alternative Stack B: Express.js + OpenAI + Weaviate + MongoDB Atlas + Netlify Functions
**Components:** Express.js (Node.js), OpenAI, Weaviate Cloud, MongoDB, Netlify Functions

**Pros:** JavaScript full-stack consistency, Weaviate strong on hybrid search, MongoDB flexible schema, Netlify Functions generous limits
**Cons:** Python RAG ecosystem richer (LangChain, LlamaIndex), Weaviate free tier limited (2GB but slower performance), MongoDB vector search beta quality
**Key Risk:** Less mature vector search (MongoDB Atlas Search vector support experimental)
**Rejected:** Python ecosystem advantage for RAG, MongoDB vector search not production-ready

### Alternative Stack C: FastAPI + Local Ollama + ChromaDB + SQLite + Fly.io
**Components:** FastAPI, self-hosted Ollama (Mistral 7B), ChromaDB (embedded), SQLite, Fly.io VMs

**Pros:** Zero LLM API costs, full control, ChromaDB simple embedding, SQLite zero config
**Cons:** Self-hosted Ollama requires GPU (Fly.io $30-50/month), lower answer quality vs OpenAI, ChromaDB scalability issues >10K vectors, SQLite not suitable for concurrent writes
**Key Risk:** Hosting costs + GPU complexity exceed savings, Mistral 7B quality insufficient (80% vs 95% OpenAI)
**Rejected:** Self-hosting complexity violates "zero backend" goal, quality concerns

### Alternative Stack D: LangChain + Supabase Vector + Vercel Edge Functions
**Components:** LangChain framework, Supabase pgvector, Vercel Edge (lighter runtime)

**Pros:** LangChain abstracts RAG boilerplate, Supabase all-in-one (vector + Postgres + auth), Edge Functions faster cold starts
**Cons:** LangChain over-engineered for simple RAG (adds 12-20 hours learning curve), Supabase pgvector slower than Qdrant (100ms vs 30ms), Edge Functions limited Python support
**Key Risk:** LangChain complexity violates "smallest viable change" principle
**Rejected:** LangChain overkill for 3 endpoints, Qdrant vector search faster

## References

- Feature Spec: `/home/salim/Desktop/hackathine_1/specs/001-rag-chatbot/spec.md`
- Implementation Plan: `/home/salim/Desktop/hackathine_1/specs/001-rag-chatbot/plan.md` (lines 47-60, 86-100, 408-436)
- Related ADRs: ADR-0005 (RAG Architecture), ADR-0006 (Frontend Integration)
- Constitution Alignment: Section 0.1.IV (Progressive Enhancement - serverless scales automatically), Section 0.2 (Decision Thresholds - 2-hour debugging limit for tooling)
