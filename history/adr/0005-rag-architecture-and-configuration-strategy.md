# ADR-0005: RAG Architecture and Configuration Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Proposed
- **Date:** 2026-02-12
- **Feature:** 001-rag-chatbot
- **Context:** Designing the core RAG (Retrieval-Augmented Generation) system that chunks textbook content, generates embeddings, retrieves relevant context, and generates accurate answers with citations for 90% of student questions.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - defines answer quality, retrieval accuracy, scalability
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - different chunking strategies, embedding models, retrieval approaches
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - affects indexing, querying, answer generation, citation extraction
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Adopt **Heading-Based Chunking + Dense Retrieval + Low-Temperature Generation** as integrated RAG architecture:

**Content Chunking Strategy:**
- **Chunk Boundaries:** Split by H2/H3 heading boundaries (preserves semantic coherence)
- **Chunk Size:** 500-1500 tokens per chunk (optimized for context window vs granularity)
- **Sub-Chunking:** Sections >1500 tokens split with 200-token overlap
- **Metadata:** Extract module ID, chapter ID, section ID, heading title, file path, navigation URL
- **Indexing Format:** One Qdrant point per chunk with full metadata payload

**Embedding & Retrieval:**
- **Embedding Model:** OpenAI text-embedding-3-small (1536 dimensions, $0.02/1M tokens)
- **Similarity Metric:** Cosine similarity (Qdrant native, range 0-1)
- **Retrieval Parameters:** top_k=5 chunks, similarity_threshold=0.7
- **Selected-Text Boost:** 2x similarity score for chunks containing user-selected text
- **Re-Ranking:** Context-boosted chunks re-ranked after initial retrieval (top-10 → top-5)

**Generation & Prompt Engineering:**
- **LLM Model:** OpenAI gpt-4o-mini ($0.15/1M tokens, balanced cost/quality)
- **Temperature:** 0.3 (low for factual consistency, high enough to avoid robotic tone)
- **Max Tokens:** 800 (limits response length, 2-3 paragraphs target)
- **System Prompt:** "You are a teaching assistant for Physical AI textbook. Answer ONLY using provided context. Cite sections."
- **Context Format:** Top-5 chunks formatted as `Section: Module > Chapter > Heading | Relevance: 0.85 | [text]`
- **Citation Extraction:** Parse LLM output for section references, link to navigation URLs

**Quality Validation:**
- **Confidence Score:** Average similarity of top-5 chunks (0.0-1.0 scale)
- **Low-Confidence Handling:** If avg similarity <0.7, show disclaimer + fallback suggestions
- **Zero-Result Response:** "I couldn't find relevant content. Related topics: [top 3 section titles]"
- **Answer Validation:** Must contain ≥1 citation OR show low-confidence disclaimer

## Consequences

### Positive

- **Semantic coherence:** Heading-based chunking preserves context (entire section in one chunk, not mid-paragraph splits)
- **Citation accuracy:** Chunks mapped to navigation URLs enable precise section links (90% citation rate target)
- **Cost efficiency:** text-embedding-3-small 5x cheaper than text-embedding-3-large with 90% quality (spec target: 95% answer accuracy)
- **Selected-text prioritization:** 2x boost ensures context-aware answers (User Story 2 requirement: prioritize selected text)
- **Factual grounding:** Low temperature (0.3) + "ONLY use context" prompt reduces hallucination risk
- **Graceful degradation:** Confidence scoring + fallback responses handle edge cases (no results, ambiguous questions)
- **Scalability:** top_k=5 limits context window usage (5 chunks × 1000 tokens = 5K context << 128K limit)
- **Retrieval speed:** Cosine similarity on 1536-dim vectors <100ms for <100K chunks (meets <5s response time target)

### Negative

- **Chunk size tradeoff:** 500-1500 tokens may be too granular (misses broader context) or too coarse (retrieves irrelevant paragraphs)
  - Mitigation: 200-token overlap for sub-chunked sections, pilot phase validates with Module 0
- **Heading dependency:** Content without H2/H3 headings (e.g., intro paragraphs) may be skipped or orphaned
  - Mitigation: Manual review during indexing, add synthetic headings if needed
- **Embedding model limitations:** text-embedding-3-small lower quality than text-embedding-3-large (95% vs 98% retrieval accuracy)
  - Accepted Tradeoff: 5x cost savings worth 3% quality drop (spec allows 90% accuracy minimum)
- **Top-k fixed at 5:** Some questions may need >5 chunks (e.g., "Compare all sensor types"), others need <5 (overly verbose answers)
  - Mitigation: Future adaptive top-k based on query complexity (Phase 7 enhancement)
- **No hybrid search:** Pure dense retrieval, no keyword matching (e.g., "ROS 2 Humble" as exact phrase may be missed if paraphrased)
  - Accepted Tradeoff: Dense retrieval sufficient for semantic queries (80-90% of use cases)
- **Selected-text boost heuristic:** Simple 2x multiplier, not ML-trained re-ranker (may over-boost irrelevant selections)
  - Mitigation: Test with 10 sample selected-text queries in Phase 4, adjust boost factor if needed
- **Citation parsing fragility:** LLM may format citations inconsistently (e.g., "Chapter 1" vs "Module 0, Chapter 1"), breaking link extraction
  - Mitigation: Structured prompt with citation format examples, post-processing regex fallback

### Key Risks

**Risk 1: Chunk Boundaries Break Semantic Coherence (P1)**
- **Likelihood:** Medium (H2/H3 sections may be too large or too small)
- **Impact:** Retrieval returns irrelevant chunks, answer quality <90% accuracy
- **Mitigation:** Pilot phase tests with Module 0 (6 success criteria include retrieval validation), adjust chunk size based on results
- **Kill Switch:** If <80% accuracy in pilot, switch to fixed 512-token chunks with 128-token overlap (OpenAI best practice)

**Risk 2: text-embedding-3-small Insufficient Quality (P2)**
- **Likelihood:** Low-Medium (trade-off between cost and quality)
- **Impact:** Similarity scores too low (<0.7), high zero-result rate (>15%)
- **Mitigation:** Test with 20 sample questions in Phase 2, compare top-5 chunks to ground truth
- **Fallback:** Upgrade to text-embedding-3-large ($0.13/1M tokens, 3072 dims) if zero-result rate >15%

**Risk 3: Low Temperature Produces Robotic Answers (P3)**
- **Likelihood:** Low (0.3 temperature validated in similar RAG systems)
- **Impact:** Answers technically correct but unengaging, student satisfaction <70%
- **Mitigation:** Pilot phase includes qualitative review of 10 sample answers, adjust temperature 0.3-0.5 range
- **Accepted Tradeoff:** Prefer correctness over style (constitution: factual accuracy > engagement)

**Risk 4: Selected-Text Boost Over-Prioritizes Context (P2)**
- **Likelihood:** Medium (untested heuristic)
- **Impact:** Answers miss broader context, focus too narrowly on selected text
- **Mitigation:** Phase 4 tests 10 selected-text queries, compare boosted vs non-boosted answers
- **Fallback:** Reduce boost factor 2x → 1.5x or 1.2x if over-prioritization detected

**Risk 5: Citation Extraction Fails Due to LLM Inconsistency (P2)**
- **Likelihood:** Medium (LLMs occasionally ignore formatting instructions)
- **Impact:** Answers without clickable citations, fails 90% citation rate target (SC-002)
- **Mitigation:** Structured prompt with explicit citation format + regex fallback parser
- **Kill Switch:** If citation rate <70%, implement post-processing NLP extraction (spaCy or regex)

## Alternatives Considered

### Alternative A: Fixed 512-Token Chunks with 128-Token Overlap (OpenAI Best Practice)
**Components:** Split all content into fixed-size chunks, 25% overlap, no heading awareness

**Pros:** Simpler implementation, OpenAI-recommended, consistent chunk sizes
**Cons:** Breaks semantic boundaries (mid-paragraph, mid-sentence splits), harder to map to navigation URLs, less citation accuracy
**Key Risk:** Citation extraction ambiguous (which section does chunk belong to?)
**Rejected:** Semantic coherence > simplicity, heading-based aligns with textbook structure

### Alternative B: Dense + Sparse Hybrid Retrieval (BM25 + Vector Search)
**Components:** Combine keyword search (BM25) with vector search, weighted combination (0.7 vector + 0.3 BM25)

**Pros:** Handles exact keyword queries better (e.g., "ROS 2 Humble version"), complementary strengths
**Cons:** 2x retrieval latency (run both searches), BM25 requires separate index (Elasticsearch or Typesense), 12-20 hour implementation
**Key Risk:** Complexity vs benefit unclear, most queries semantic (not keyword-based)
**Rejected:** Pure dense retrieval sufficient for 80-90% queries, hybrid deferred to Phase 7 if needed

### Alternative C: Large Chunks (1500-3000 tokens) with Sliding Window
**Components:** Larger chunks preserve full context, sliding window generates overlapping views

**Pros:** Maximum context per chunk, fewer chunks to manage (lower storage costs)
**Cons:** Higher embedding costs (3-6x more tokens), slower retrieval (more data per chunk), less precise citations (harder to pinpoint exact section)
**Key Risk:** Cost vs quality tradeoff unclear, may exceed context window budget
**Rejected:** Cost inefficient, citation precision degraded

### Alternative D: Recursive Chunking (Summary → Details Hierarchy)
**Components:** Generate summaries for sections, embed both summary and full text, retrieve summary first then expand to details

**Pros:** Better handles multi-part questions (retrieves relevant sections, then drills down), more context-aware
**Cons:** 2x embedding costs (summary + full text), complex implementation (8-12 hours), untested workflow
**Key Risk:** Summary quality depends on LLM accuracy (hallucination risk)
**Rejected:** Complexity vs benefit unclear, pilot phase tests simpler approach first

### Alternative E: LangChain RAG Pipeline with RetrievalQA
**Components:** LangChain framework, pre-built RetrievalQA chain, chromaDB/Qdrant integration

**Pros:** Abstracts boilerplate (retrieval + generation in one call), well-documented
**Cons:** LangChain overhead (12-20 hours learning curve), less control over prompt engineering, heavier dependencies (slower cold starts)
**Key Risk:** Over-abstraction hides important configuration (chunk size, top-k, temperature)
**Rejected:** Direct OpenAI + Qdrant calls more transparent, aligns with "explicit over implicit" principle

## References

- Feature Spec: `/home/salim/Desktop/hackathine_1/specs/001-rag-chatbot/spec.md` (User Story 1-2, FR-001 to FR-010, SC-001, SC-002, SC-006)
- Implementation Plan: `/home/salim/Desktop/hackathine_1/specs/001-rag-chatbot/plan.md` (lines 103-120: Phase 1 Content Indexing, lines 122-140: Phase 2 RAG Functionality, lines 651-721: Prompt Engineering)
- Related ADRs: ADR-0004 (Backend Stack - OpenAI + Qdrant), ADR-0006 (Frontend Integration - selected text detection)
- Constitution Alignment: Section 0.1.III (Incremental Validation - pilot phase tests chunking), Section 0.1.V (Explicit Over Implicit - direct API calls over LangChain)
