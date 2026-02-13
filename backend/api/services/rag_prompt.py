"""
RAG prompt templates and construction.
"""
from typing import List, Dict


SYSTEM_PROMPT = """You are a teaching assistant for the Physical AI & Humanoid Robotics textbook.

Answer student questions using ONLY the provided context from the textbook.

Rules:
- Use ONLY information from the CONTEXT
- If answer not in CONTEXT, say so
- Cite sections: [Module X: Section Title]
- Be concise: 2-3 paragraphs max
- Use textbook terminology
- Preserve LaTeX/code formatting
"""


def build_user_prompt(question: str, context_chunks: List[Dict], conversation_history: List[Dict] = None) -> str:
    """
    Build user prompt with context chunks, question, and optional conversation history (T085).

    Args:
        question: User's question
        context_chunks: List of retrieved chunks with metadata
        conversation_history: Optional list of previous Q&A pairs [{'question': '...', 'answer': '...'}, ...]

    Returns:
        Formatted user prompt string
    """
    # Format conversation history if provided (T085)
    history_text = ""
    if conversation_history and len(conversation_history) > 0:
        history_parts = []
        for i, qa_pair in enumerate(conversation_history, 1):
            history_parts.append(f"""Q{i}: {qa_pair.get('question', '')}
A{i}: {qa_pair.get('answer', '')}""")
        history_text = "\n\n".join(history_parts)
        history_section = f"""
PREVIOUS CONVERSATION:
{history_text}
"""
    else:
        history_section = ""

    # Format context chunks
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        payload = chunk['payload']
        score = chunk['score']

        context_part = f"""---
Section {i}: {payload.get('heading', 'Unknown')}
Module: {payload.get('module_id', 'N/A')}
Relevance: {score:.2f}
---
{payload.get('text', '')}
"""
        context_parts.append(context_part)

    context_text = "\n\n".join(context_parts)

    user_prompt = f"""CONTEXT:
{context_text}
{history_section}
QUESTION: {question}

INSTRUCTIONS:
1. Answer using ONLY the CONTEXT above
2. If follow-up question, reference previous conversation
3. If not in CONTEXT: "Information not found. Related: [sections]"
4. Cite: [Module X: Section Title]
5. Be concise: 2-3 paragraphs max

ANSWER:"""

    return user_prompt


def detect_ambiguous_question(question: str) -> bool:
    """
    Detect if question is too ambiguous and needs clarification.

    Args:
        question: User's question

    Returns:
        True if question is ambiguous
    """
    # Very short questions (< 5 words) that are just "what/how/why"
    words = question.split()

    if len(words) < 5:
        starter_words = ['what', 'how', 'why', 'when', 'where', 'who']
        if words[0].lower() in starter_words:
            return True

    return False


def detect_broad_question(question: str) -> bool:
    """
    Detect if question is too broad for a direct answer.

    Args:
        question: User's question

    Returns:
        True if question is very broad
    """
    broad_keywords = ['all', 'every', 'list all', 'everything about']

    question_lower = question.lower()
    return any(keyword in question_lower for keyword in broad_keywords)


def build_clarification_prompt(question: str) -> str:
    """
    Build prompt asking for clarification.

    Args:
        question: Ambiguous question

    Returns:
        Clarification request
    """
    return f"""I'd be happy to help! However, your question "{question}" is quite brief. Could you please provide more details or context? For example:

- What specific aspect are you interested in?
- Is this related to a particular module or topic?
- Are you looking for a definition, example, or explanation?

This will help me provide a more accurate answer."""


def build_summary_response(question: str, context_chunks: List[Dict]) -> str:
    """
    Build summary response for broad questions.

    Args:
        question: Broad question
        context_chunks: Retrieved chunks

    Returns:
        Summary with section links
    """
    sections = []
    for chunk in context_chunks[:5]:  # Top 5 relevant sections
        payload = chunk['payload']
        sections.append(f"- [{payload.get('heading', 'Unknown')}]({payload.get('navigation_url', '#')})")

    sections_text = "\n".join(sections)

    return f"""Your question is quite broad. The textbook covers this topic across multiple sections. Here are the most relevant sections you can explore:

{sections_text}

Would you like me to answer a more specific question about any of these topics?"""
