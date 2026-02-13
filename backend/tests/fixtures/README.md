# Test Fixtures

This directory contains test data and mock responses for backend testing.

## Files

### sample_questions.json
- **Purpose**: 20 curated test questions covering various complexity levels
- **Structure**: Each question includes:
  - `id`: Unique identifier (q001-q020)
  - `question`: The test question text
  - `module`: Which module it belongs to
  - `complexity`: basic, intermediate, or advanced
  - `tags`: Categorization tags

### expected_answers.json
- **Purpose**: Ground truth answers for quality validation
- **Structure**: Each answer includes:
  - `question_id`: Links to sample_questions.json
  - `expected_answer`: Reference answer
  - `required_keywords`: Keywords that should appear in RAG response
  - `min_citations`: Minimum number of citations expected

### mock_embeddings.json
- **Purpose**: Pre-computed embeddings to avoid OpenAI API calls during testing
- **Dimension**: 1536 (matches text-embedding-3-small)
- **Generation**: Deterministic based on question ID (reproducible)
- **Usage**: Load in tests instead of calling OpenAI API

### generate_mock_embeddings.py
- **Purpose**: Regenerate mock embeddings if questions change
- **Usage**: `python generate_mock_embeddings.py`
- **Note**: Uses pure Python (no NumPy dependency)

## Usage in Tests

```python
import pytest
from pathlib import Path

# Using pytest fixtures (see conftest.py)
def test_question_answering(sample_questions, mock_embeddings, expected_answers):
    question = sample_questions[0]
    embedding = mock_embeddings[question['id']]
    expected = next(a for a in expected_answers if a['question_id'] == question['id'])

    # Run your test...
```

## Adding New Test Data

1. **Add questions**: Edit `sample_questions.json`
2. **Add expected answers**: Edit `expected_answers.json`
3. **Regenerate embeddings**: Run `python generate_mock_embeddings.py`
4. **Verify**: Run tests to ensure new data works

## Test Coverage Strategy

- **Basic questions** (q001-q010): Core concepts, definitions
- **Intermediate questions** (q011-q015): Relationships, comparisons
- **Advanced questions** (q016-q020): Complex topics, edge cases
