# Feature Specification: RAG Chatbot for Physical AI Textbook

**Feature Branch**: `001-rag-chatbot`
**Created**: 2026-02-12
**Status**: Draft
**Input**: User description: "Core RAG Chatbot Requirements - Functionality: RAG system embedded within published book to answer questions about book content and user-selected text. Technology Stack: OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, Qdrant Cloud Free Tier. Deployment: Embedded within Docusaurus book on GitHub Pages or Vercel. Integration: Directly integrated into published book interface. Content Source: Exclusively from textbook content on Physical AI & Humanoid Robotics. User-Selected Text Feature: Answer questions based on text selected by users within the book."

## Clarifications

### Session 2026-02-12

- Q: Where should the FastAPI backend API be hosted (frontend will be on GitHub Pages)? → A: Vercel Serverless Functions (backend only, handles API calls from GitHub Pages-hosted chatbot widget)
- Q: Which OpenAI models for embeddings and chat completion? → A: text-embedding-3-small for embeddings, gpt-4o-mini for chat completion (cost-optimized with good quality)
- Q: How should textbook content be chunked for vector indexing? → A: By heading level (H2/H3 sections) to preserve semantic coherence and align with book structure for accurate citations
- Q: How should selected text context be handled (FR-008)? → A: Weight selected text higher in semantic search (2x similarity boost) - searches entire book but prioritizes chunks containing/near selected text
- Q: Retrieval parameters - how many chunks (top-k) and what similarity threshold? → A: Top-k=5 chunks, cosine similarity threshold=0.7 (balanced quality and performance)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - General Book Q&A (Priority: P1)

A reader is studying the Physical AI & Humanoid Robotics textbook and encounters a concept they want to understand better. They open the embedded chatbot, type their question (e.g., "What are the key sensors used in humanoid robots?"), and receive an AI-generated answer based on relevant sections from the book with citations to specific chapters/sections.

**Why this priority**: This is the core MVP functionality - enabling readers to get instant, contextual answers to questions while reading the book. It provides immediate value and improves learning outcomes.

**Independent Test**: Can be fully tested by loading any chapter of the book, asking questions related to that chapter, and verifying that answers are generated from book content with proper citations. Delivers value even without the selected-text feature.

**Acceptance Scenarios**:

1. **Given** a reader is on any page of the published textbook, **When** they click the chatbot widget, **Then** a chat interface opens within the book layout
2. **Given** the chatbot interface is open, **When** the reader types a question about book content and submits, **Then** the system retrieves relevant content from the vector database and generates an answer within a reasonable timeframe
3. **Given** the chatbot has generated an answer, **When** the answer is displayed, **Then** it includes citations referencing specific book sections where the information was sourced
4. **Given** a reader asks a question about a topic covered in the book, **When** the answer is generated, **Then** the answer is accurate and draws exclusively from the textbook content (not external sources)

---

### User Story 2 - Selected Text Q&A (Priority: P2)

A reader encounters a specific paragraph or section that is confusing or requires deeper explanation. They highlight the text directly in the book, right-click or use a button to "Ask about this selection," and the chatbot opens with the selected text as context. The reader can then ask questions specifically about that highlighted passage.

**Why this priority**: This enhances the basic Q&A by providing context-aware assistance. It's a differentiating feature that improves precision but requires the P1 foundation.

**Independent Test**: Can be tested independently by selecting any text passage in the book, triggering the context-specific query interface, and verifying that answers are scoped to the selected text. Delivers enhanced contextual understanding for complex passages.

**Acceptance Scenarios**:

1. **Given** a reader is viewing book content, **When** they select/highlight text on the page, **Then** a "Ask about this" action becomes available (button, context menu, or similar)
2. **Given** text is selected and the "Ask about this" action is triggered, **When** the chatbot opens, **Then** the selected text is displayed as context in the chat interface
3. **Given** the chatbot has the selected text as context, **When** the reader asks a question, **Then** the semantic search applies 2x similarity boost to chunks containing/near the selected text while still searching the entire book
4. **Given** the selected text is very short (e.g., single word or phrase), **When** the reader asks a question, **Then** the semantic search can retrieve relevant surrounding sections beyond the selected text to provide a meaningful answer

---

### User Story 3 - Answer Quality and Navigation (Priority: P3)

A reader receives an answer from the chatbot and wants to verify the source or read more. They click on a citation in the answer, and the book automatically scrolls/navigates to the referenced section. The reader can also provide feedback on answer quality (thumbs up/down).

**Why this priority**: This improves trust and learning by enabling verification and continuous improvement through feedback. It builds on P1 and P2 but is not essential for initial value delivery.

**Independent Test**: Can be tested independently by generating answers with citations, clicking citation links, and verifying navigation behavior. Feedback collection can be validated through logging. Delivers enhanced trust and long-term quality improvement.

**Acceptance Scenarios**:

1. **Given** the chatbot displays an answer with citations, **When** the reader clicks a citation link, **Then** the book navigates to the corresponding section and highlights the referenced content
2. **Given** an answer is displayed, **When** the reader clicks a feedback button (thumbs up/down), **Then** the feedback is recorded for future answer quality improvement
3. **Given** a reader asks a follow-up question in the same chat session, **When** the answer is generated, **Then** the chatbot maintains conversation context and can reference previous questions/answers

---

### Edge Cases

- **What happens when no relevant content is found (all chunks below 0.7 similarity threshold)?** The chatbot should display a message: "I couldn't find relevant content in the textbook to answer this question. Try rephrasing or browse these related topics: [list top 3 closest matches by section title]".
- **How does the system handle ambiguous or very broad questions?** The chatbot should either ask clarifying questions or provide a summary answer with links to multiple relevant sections for deeper exploration.
- **What happens when selected text is too long (entire chapter)?** The system should display an error message: "Selected text is too long (max 2000 characters). Please select a shorter passage."
- **How does the system handle code snippets or mathematical formulas in questions?** The chatbot should recognize and preserve formatting when displaying code/formulas in answers, and retrieve relevant examples from the book.
- **What happens if the chatbot is queried before content is indexed?** The system should display a "Chatbot initializing" message or disable the chatbot until content indexing is complete.
- **How does the system handle concurrent users?** The backend should support multiple simultaneous chat sessions without performance degradation or answer quality issues.
- **What happens during network failures?** Display cached last known state with "Connection lost" banner and auto-retry every 5 seconds.
- **What happens if user submits empty question?** Disable submit button and show inline validation hint "Please enter a question."
- **What happens if API quota is exhausted?** Display maintenance message: "Chatbot temporarily unavailable. Please try again in [TIME]."
- **What happens if user exceeds 50 messages per session?** Automatically archive oldest messages and notify user: "Chat history limit reached. Older messages archived."
- **What happens if user asks questions about images, diagrams, or tables?** Chatbot identifies visual elements by caption/alt-text and directs user to view the figure in context with citation link.
- **What happens if session times out during active conversation?** Display 1-minute warning notification, then clear chat with message: "Session expired due to inactivity. Start a new conversation."

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST embed a persistent chatbot widget in all pages of the published Docusaurus book that readers can open/close
- **FR-002**: System MUST accept free-text questions from readers through the chat interface
- **FR-003**: System MUST retrieve top-5 most relevant content chunks from a vector database based on the user's question using semantic similarity search (cosine similarity, threshold 0.7) with OpenAI text-embedding-3-small model
- **FR-004**: System MUST generate answers using a Retrieval-Augmented Generation (RAG) approach powered by OpenAI gpt-4o-mini model
- **FR-005**: System MUST include citations in generated answers that reference specific book sections (chapter, module, or page identifiers)
- **FR-006**: System MUST allow readers to select/highlight text within the book interface
- **FR-007**: System MUST provide an action (button, context menu, or similar) to initiate a context-specific query based on selected text
- **FR-008**: System MUST weight selected text higher in semantic search (2x similarity boost) when generating answers for context-specific queries, searching the entire book while prioritizing chunks containing or near the selected text
- **FR-009**: System MUST draw answers exclusively from the textbook content on Physical AI & Humanoid Robotics (no external web sources)
- **FR-010**: System MUST handle cases where no relevant content is found and provide helpful fallback responses
- **FR-011**: System MUST maintain chat history within a session to support follow-up questions, where a session is defined as:
  - Single browser tab lifetime (history cleared on tab close)
  - Maximum 2-hour inactivity timeout
  - Maximum 50 messages per session
- **FR-012**: System MUST process and index all textbook content into a vector database by splitting content at H2/H3 heading boundaries before the chatbot becomes available
- **FR-013**: System MUST store chat interaction logs in a persistent database for quality monitoring and improvement
- **FR-014**: System MUST be deployable as part of the static site book platform
- **FR-015**: System MUST provide clickable citation links that smooth scroll to the corresponding book section within the same page when clicked

### Security & Privacy Requirements

- **FR-016**: System MUST sanitize and validate all user input to prevent injection attacks
- **FR-017**: System MUST NOT store personally identifiable information (PII) in chat logs
- **FR-018**: System MUST implement rate limiting (maximum 20 queries per user per minute) to prevent abuse
- **FR-019**: System MUST provide a clear privacy notice about data collection before chat usage
- **FR-020**: Chat logs MUST be retained for no longer than 90 days and then automatically deleted

### Accessibility Requirements

- **FR-021**: Chatbot widget MUST be fully navigable using keyboard only (Tab, Enter, Escape keys)
- **FR-022**: Chatbot MUST provide ARIA labels and landmarks for screen reader compatibility
- **FR-023**: Chatbot interface MUST meet WCAG 2.1 Level AA standards for contrast, text size, and focus indicators
- **FR-024**: Citations MUST be announced by screen readers with context (e.g., "Reference: Chapter 3, Section 2")
- **FR-025**: System MUST support text resizing up to 200% without breaking layout

### Error Handling Requirements

- **FR-026**: System MUST display a user-friendly error message when API fails, with retry option
- **FR-027**: System MUST show a loading indicator during answer generation (minimum 500ms)
- **FR-028**: System MUST handle network timeouts gracefully (maximum 30 seconds wait, then error message)
- **FR-029**: System MUST inform users if selected text is too long (exceeds 2000 characters) and suggest shortening
- **FR-030**: System MUST provide a "Report Issue" button for users to flag incorrect answers

### Mobile-Specific Requirements

- **FR-031**: On mobile devices (screen width <768px), chatbot MUST open as full-screen overlay (not floating widget)
- **FR-032**: Chatbot MUST support touch gestures (swipe down to close, pull-to-refresh for new session)
- **FR-033**: Selected text feature MUST use native mobile text selection (long-press) on touch devices
- **FR-034**: Chat input field MUST auto-focus and trigger keyboard on mobile without requiring additional tap
- **FR-035**: Chatbot MUST minimize when user scrolls the book content on mobile

### Content Management Requirements

- **FR-036**: System MUST support incremental content indexing (add new modules without re-indexing all existing content)
- **FR-037**: System MUST display a "Content last updated: [DATE]" timestamp in chatbot footer
- **FR-038**: System MUST invalidate outdated answers when content is re-indexed
- **FR-039**: Chatbot MUST show a banner when new modules become searchable (e.g., "Module 2 now available!")

### Session Management Requirements

- **FR-040**: System MUST provide a "Clear Chat" button to manually reset session
- **FR-041**: System MUST NOT persist chat history across browser sessions (privacy protection)
- **FR-042**: System MUST warn users before session timeout (1-minute warning notification)

### Key Entities

- **Chat Message**: Represents a single message in a conversation, including user questions and AI-generated answers, with timestamp and session identifier
- **Book Content Chunk**: A segment of the textbook content split by heading level (H2/H3 sections) and indexed in the vector database, including text, text-embedding-3-small embeddings, and metadata (module, chapter, section identifier, heading title)
- **User Query**: The question or prompt submitted by a reader, including optional context (selected text) and session information
- **Generated Answer**: The RAG-generated response, including answer text, source citations, and confidence metadata
- **Source Citation**: A reference to a specific book section used to generate an answer, including section identifier, title, and navigation link
- **Chat Session**: A collection of related messages within a single conversation context, tied to a reader's browsing session
- **Feedback Event**: User feedback on answer quality (thumbs up/down or similar), linked to specific answers for quality improvement

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Readers can submit a question and receive a generated answer within 5 seconds for 95% of queries
- **SC-002**: Generated answers include at least one relevant source citation for 90% of questions that have book content matches
- **SC-003**: The chatbot successfully answers questions about any module or chapter in the textbook with content sourced exclusively from the book
- **SC-004**: Selected text queries generate answers that are contextually relevant to the highlighted passage in 90% of cases (measured through user feedback or manual review)
- **SC-005**: The chatbot interface is accessible and functional on both desktop and mobile devices without breaking the book's layout
- **SC-006**: Generated answers achieve 80%+ accuracy based on human evaluation using the following methodology:
  - **Evaluation Sample**: 100 randomly sampled Q&A pairs per module
  - **Evaluators**: 2 subject matter experts (SMEs) independently rate each answer
  - **Criteria**: Answer is marked "accurate" if it: (1) Correctly addresses the question, (2) Uses information exclusively from correct book sections, (3) Contains no hallucinated or external information
  - **Frequency**: Evaluated after initial launch and after each new module release
- **SC-007**: The system supports at least 50 concurrent users without performance degradation (response time increase >20%)
- **SC-008**: The chatbot successfully answers questions about Module 0 and Module 1 content at launch, with additional modules indexed and made searchable in subsequent releases
- **SC-009**: System blocks 100% of malicious input patterns (SQL injection, XSS, prompt injection attempts) during security testing
- **SC-010**: Rate limiting activates after 20 requests within 60 seconds, with user-friendly error message
- **SC-011**: Chatbot passes automated WCAG 2.1 AA compliance testing (WAVE, axe DevTools) with zero critical violations
- **SC-012**: Users can complete full Q&A workflow using only keyboard navigation (no mouse required)
- **SC-013**: Mobile chatbot loads and becomes interactive within 3 seconds on 4G connection
- **SC-014**: Mobile users can complete Q&A without horizontal scrolling or pinch-zoom
- **SC-015**: Chatbot JavaScript bundle size is less than 50KB (gzipped) for mobile performance
- **SC-016**: Inter-rater agreement between evaluators is greater than 85% (Cohen's Kappa) for answer quality assessment
- **SC-017**: Chatbot widget total JavaScript bundle size is less than 100KB (gzipped) including all dependencies
- **SC-018**: Time to Interactive (TTI) for chatbot widget is less than 2 seconds on desktop, less than 4 seconds on mobile

## Assumptions

1. **Docusaurus Integration**: The current Docusaurus book setup supports embedding custom React components for the chatbot widget
2. **Content Format**: The textbook content is available in a structured format (Markdown, MDX, or HTML) that can be parsed into chunks for vector database indexing
3. **OpenAI API Access**: The project has access to OpenAI API with text-embedding-3-small (~$0.02/1K embeddings) and gpt-4o-mini (~$0.15/1M input tokens) within budget constraints
4. **Deployment Pipeline**: The existing GitHub Pages or Vercel deployment pipeline can accommodate backend API services (FastAPI) or serverless functions
5. **Free Tier Limits**: Qdrant Cloud Free Tier and Neon Serverless Postgres free tier are sufficient for expected usage volumes during initial launch
6. **Text Selection**: Docusaurus supports native browser text selection and JavaScript events to capture selected text
7. **Navigation Linking**: Book sections have unique identifiers or URL fragments that can be linked to for citation navigation
8. **Content Update Frequency**: Book content updates occur no more than once per week, allowing time for re-indexing and validation
9. **Expected Traffic**: Peak concurrent users will not exceed 200 during initial launch phase (4x safety margin above SC-007 target)
10. **Browser Compatibility**: Target browsers support modern JavaScript (ES6+), localStorage, and CSS Grid (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

## Dependencies

1. **Docusaurus Book Deployment**: The chatbot feature depends on the textbook being published and accessible via Docusaurus on GitHub Pages
2. **Textbook Content Finalization**: Content must be finalized (or at least in a stable state) for indexing into the vector database
3. **OpenAI Agents/ChatKit SDK**: Availability and compatibility of OpenAI Agents or ChatKit SDKs for RAG implementation
4. **Qdrant Cloud Account**: Active Qdrant Cloud Free Tier account for vector database hosting
5. **Neon Postgres Account**: Active Neon Serverless Postgres account for storing chat logs and metadata
6. **Backend API Hosting**: Vercel account for deploying FastAPI backend as serverless functions (frontend on GitHub Pages will make CORS-enabled API calls to Vercel backend)

## Out of Scope

- **Multi-language Support**: The chatbot will only support the language in which the textbook is written (assumed to be English)
- **User Authentication**: No user login or account system required; chatbot is accessible to all readers anonymously
- **Advanced Analytics Dashboard**: No admin dashboard for analyzing chat interactions; basic logging to Postgres is sufficient
- **Offline Functionality**: The chatbot requires an internet connection to function (no offline mode)
- **Voice Input/Output**: No speech-to-text or text-to-speech capabilities
- **Custom Model Training**: The chatbot uses OpenAI's pre-trained models; no custom fine-tuning or model training is in scope
- **Integration with External Resources**: Answers are drawn exclusively from the textbook; no external web search or knowledge base integration
- **Advanced Conversation Features**: No support for multi-turn complex reasoning, task automation, or agentic workflows beyond basic Q&A
