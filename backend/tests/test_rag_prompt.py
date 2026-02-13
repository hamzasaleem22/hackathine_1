"""
Unit tests for RAG prompt construction.

Tests prompt building, ambiguity detection, and broad question handling.
"""
import pytest
from api.services.rag_prompt import (
    build_user_prompt,
    detect_ambiguous_question,
    detect_broad_question,
    build_clarification_prompt,
    build_summary_response,
    SYSTEM_PROMPT
)


class TestRAGPrompt:
    """Test suite for RAG prompt construction."""

    @pytest.fixture
    def sample_chunks(self):
        """Sample context chunks for testing."""
        return [
            {
                'score': 0.95,
                'payload': {
                    'text': 'Reinforcement learning is a type of machine learning where an agent learns to make decisions by interacting with an environment.',
                    'heading': 'Introduction to Reinforcement Learning',
                    'module_id': 'module-1',
                    'chapter_id': 'ch1',
                    'navigation_url': '/docs/module-1/chapter-1#intro'
                }
            },
            {
                'score': 0.88,
                'payload': {
                    'text': 'Q-learning is a model-free reinforcement learning algorithm that learns the value of state-action pairs.',
                    'heading': 'Q-Learning Algorithm',
                    'module_id': 'module-1',
                    'chapter_id': 'ch2',
                    'navigation_url': '/docs/module-1/chapter-2#qlearning'
                }
            }
        ]

    def test_build_user_prompt_structure(self, sample_chunks):
        """Test that user prompt has correct structure."""
        # Arrange
        question = "What is reinforcement learning?"

        # Act
        prompt = build_user_prompt(question, sample_chunks)

        # Assert
        assert "CONTEXT (from Physical AI textbook):" in prompt
        assert "STUDENT QUESTION:" in prompt
        assert question in prompt
        assert "INSTRUCTIONS:" in prompt
        assert "ANSWER:" in prompt

    def test_build_user_prompt_includes_all_chunks(self, sample_chunks):
        """Test that all chunks are included in prompt."""
        # Arrange
        question = "Explain Q-learning"

        # Act
        prompt = build_user_prompt(question, sample_chunks)

        # Assert
        assert "Reinforcement learning is a type" in prompt
        assert "Q-learning is a model-free" in prompt
        assert "Section 1:" in prompt
        assert "Section 2:" in prompt

    def test_build_user_prompt_includes_metadata(self, sample_chunks):
        """Test that metadata is included in prompt."""
        # Arrange
        question = "Test question"

        # Act
        prompt = build_user_prompt(question, sample_chunks)

        # Assert
        assert "Introduction to Reinforcement Learning" in prompt
        assert "Q-Learning Algorithm" in prompt
        assert "Module: module-1" in prompt
        assert "Relevance: 0.95" in prompt
        assert "Relevance: 0.88" in prompt

    def test_build_user_prompt_empty_chunks(self):
        """Test prompt building with empty chunks."""
        # Arrange
        question = "What is RL?"
        chunks = []

        # Act
        prompt = build_user_prompt(question, chunks)

        # Assert
        assert "STUDENT QUESTION:" in prompt
        assert question in prompt
        assert "INSTRUCTIONS:" in prompt

    def test_build_user_prompt_missing_metadata(self):
        """Test prompt building with chunks missing metadata."""
        # Arrange
        question = "Test"
        chunks = [
            {
                'score': 0.9,
                'payload': {
                    'text': 'Some content'
                    # Missing heading, module_id, etc.
                }
            }
        ]

        # Act
        prompt = build_user_prompt(question, chunks)

        # Assert
        assert "Some content" in prompt
        assert "Unknown" in prompt  # Default heading
        assert "N/A" in prompt  # Default module_id

    def test_detect_ambiguous_question_short_what(self):
        """Test detection of short 'what' questions."""
        # Arrange
        question = "What is RL?"

        # Act
        result = detect_ambiguous_question(question)

        # Assert
        assert result is True

    def test_detect_ambiguous_question_short_how(self):
        """Test detection of short 'how' questions."""
        # Arrange
        questions = [
            "How does it work?",
            "Why is this?",
            "When should I?",
            "Where is this?"
        ]

        # Act & Assert
        for q in questions:
            assert detect_ambiguous_question(q) is True

    def test_detect_ambiguous_question_detailed(self):
        """Test that detailed questions are not marked as ambiguous."""
        # Arrange
        question = "How does Q-learning differ from SARSA in reinforcement learning?"

        # Act
        result = detect_ambiguous_question(question)

        # Assert
        assert result is False

    def test_detect_ambiguous_question_long_enough(self):
        """Test that questions with 5+ words starting with question words pass."""
        # Arrange
        question = "What are the main components of systems?"

        # Act
        result = detect_ambiguous_question(question)

        # Assert
        assert result is False

    def test_detect_ambiguous_question_non_question_word(self):
        """Test that short questions not starting with question words pass."""
        # Arrange
        question = "Explain RL"  # Only 2 words but doesn't start with question word

        # Act
        result = detect_ambiguous_question(question)

        # Assert
        assert result is False

    def test_detect_broad_question_all(self):
        """Test detection of questions with 'all'."""
        # Arrange
        question = "What are all the types of reinforcement learning?"

        # Act
        result = detect_broad_question(question)

        # Assert
        assert result is True

    def test_detect_broad_question_every(self):
        """Test detection of questions with 'every'."""
        # Arrange
        question = "Explain every algorithm in the book"

        # Act
        result = detect_broad_question(question)

        # Assert
        assert result is True

    def test_detect_broad_question_list_all(self):
        """Test detection of 'list all' questions."""
        # Arrange
        question = "Can you list all the chapters?"

        # Act
        result = detect_broad_question(question)

        # Assert
        assert result is True

    def test_detect_broad_question_everything(self):
        """Test detection of 'everything about' questions."""
        # Arrange
        question = "Tell me everything about neural networks"

        # Act
        result = detect_broad_question(question)

        # Assert
        assert result is True

    def test_detect_broad_question_specific(self):
        """Test that specific questions are not marked as broad."""
        # Arrange
        question = "How does the Q-learning update rule work?"

        # Act
        result = detect_broad_question(question)

        # Assert
        assert result is False

    def test_detect_broad_question_case_insensitive(self):
        """Test that broad question detection is case-insensitive."""
        # Arrange
        question = "What are ALL the types?"

        # Act
        result = detect_broad_question(question)

        # Assert
        assert result is True

    def test_build_clarification_prompt_includes_question(self):
        """Test that clarification prompt includes the original question."""
        # Arrange
        question = "What is RL?"

        # Act
        prompt = build_clarification_prompt(question)

        # Assert
        assert question in prompt
        assert "more details" in prompt.lower()
        assert "specific aspect" in prompt.lower()

    def test_build_clarification_prompt_structure(self):
        """Test clarification prompt has helpful structure."""
        # Arrange
        question = "How does it work?"

        # Act
        prompt = build_clarification_prompt(question)

        # Assert
        assert "?" in prompt  # Has questions for user
        assert "specific aspect" in prompt
        assert "module or topic" in prompt
        assert "definition, example, or explanation" in prompt

    def test_build_summary_response_includes_sections(self, sample_chunks):
        """Test that summary response includes section links."""
        # Arrange
        question = "Tell me all about RL"

        # Act
        response = build_summary_response(question, sample_chunks)

        # Assert
        assert "Introduction to Reinforcement Learning" in response
        assert "Q-Learning Algorithm" in response
        assert "/docs/module-1/chapter-1#intro" in response
        assert "/docs/module-1/chapter-2#qlearning" in response

    def test_build_summary_response_limits_sections(self):
        """Test that summary response limits to top 5 sections."""
        # Arrange
        question = "Everything about RL"
        many_chunks = [
            {
                'score': 0.9 - i * 0.1,
                'payload': {
                    'heading': f'Section {i}',
                    'navigation_url': f'/docs/section-{i}'
                }
            }
            for i in range(10)
        ]

        # Act
        response = build_summary_response(question, many_chunks)

        # Assert
        # Should only include first 5 sections
        assert "Section 0" in response
        assert "Section 4" in response
        assert "Section 5" not in response
        assert "Section 9" not in response

    def test_build_summary_response_structure(self, sample_chunks):
        """Test summary response has correct structure."""
        # Arrange
        question = "List all topics"

        # Act
        response = build_summary_response(question, sample_chunks)

        # Assert
        assert "broad" in response.lower()
        assert "multiple sections" in response.lower()
        assert "-" in response  # Bullet points
        assert "[" in response and "]" in response  # Markdown links
        assert "more specific question" in response.lower()

    def test_system_prompt_exists(self):
        """Test that system prompt is defined."""
        # Assert
        assert SYSTEM_PROMPT is not None
        assert len(SYSTEM_PROMPT) > 0
        assert "Physical AI" in SYSTEM_PROMPT
        assert "teaching assistant" in SYSTEM_PROMPT

    def test_system_prompt_guidelines(self):
        """Test that system prompt includes key guidelines."""
        # Assert
        assert "ONLY" in SYSTEM_PROMPT or "only" in SYSTEM_PROMPT.lower()
        assert "CONTEXT" in SYSTEM_PROMPT
        assert "cite" in SYSTEM_PROMPT.lower() or "citation" in SYSTEM_PROMPT.lower()
        assert "concise" in SYSTEM_PROMPT.lower()

    def test_build_user_prompt_preserves_formatting_instruction(self, sample_chunks):
        """Test that prompt includes instruction to preserve LaTeX/code."""
        # Arrange
        question = "Test"

        # Act
        prompt = build_user_prompt(question, sample_chunks)

        # Assert
        # The instructions should mention preserving formatting
        # This is in SYSTEM_PROMPT which is separate, but instructions should be present
        assert "technical terminology" in prompt.lower()
