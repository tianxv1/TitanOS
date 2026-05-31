# Contributing to TitanOS

Thank you for your interest in contributing to TitanOS!

## Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/tianxv1/TitanOS.git
   cd TitanOS
   ```

2. **Setup backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Setup frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Run development servers**
   ```bash
   # Backend (terminal 1)
   cd backend
   python app.py

   # Frontend (terminal 2)
   cd frontend
   npm run dev
   ```

## Project Structure

```
TitanOS/
├── backend/
│   ├── app.py              # FastAPI main entry
│   ├── memory/             # Memory Engine
│   ├── brain/              # Reasoning Engine
│   ├── planner/            # Task Planner
│   ├── skills/             # Skill Store
│   ├── knowledge_graph/    # Knowledge Graph
│   ├── learning/           # Learning Engine
│   ├── digital_twin/        # Digital Twin
│   ├── rag/                # RAG Engine
│   ├── agent/              # Agent Runtime
│   ├── reflection/         # Reflection System
│   └── knowledge_base/     # Personal Knowledge Base
└── frontend/               # Next.js frontend
```

## Coding Guidelines

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused (ideally < 50 lines)

Example:
```python
def calculate_memory_score(
    importance: float,
    access_count: int,
    recent_score: float
) -> float:
    """
    Calculate memory score based on importance, access count, and recency.

    Args:
        importance: Memory importance (0.0 - 1.0)
        access_count: Number of times memory was accessed
        recent_score: Recency score (0.0 - 1.0)

    Returns:
        Calculated memory score
    """
    return importance * 0.6 + access_count * 0.3 + recent_score * 0.1
```

### TypeScript/JavaScript (Frontend)

- Use TypeScript for new components
- Follow existing naming conventions
- Use functional components with hooks
- Keep components modular

## Testing

Run tests before submitting:

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Commit Messages

Use clear, descriptive commit messages:

- `feat: add new feature`
- `fix: resolve bug`
- `docs: update documentation`
- `refactor: restructure code`
- `test: add tests`

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Review

- Be responsive to code review feedback
- Make incremental changes
- Ensure tests pass before requesting review

## Questions?

Open an issue on GitHub for questions or discussions.
