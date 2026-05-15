# Cursor Rules for FastApi Template

This directory contains rule files that guide Cursor's AI agents when working on this project. Each `.mdc` file focuses on a specific aspect of the codebase.

## Rule Files

1. **project-overview.mdc** - General project information and technology stack
2. **python-conventions.mdc** - Python coding standards and style guidelines
3. **fastapi-patterns.mdc** - FastAPI-specific patterns and route conventions
4. **database-models.mdc** - SQLAlchemy models and async database operations
5. **api-standards.mdc** - API response formats and HTTP conventions
6. **error-handling.mdc** - Exception handling and error response patterns
7. **testing-standards.mdc** - Testing conventions using pytest
8. **security-best-practices.mdc** - Security guidelines and vulnerability prevention
9. **workflow-guidelines.mdc** - Development workflow and command references

## How Rules Work

- **alwaysApply: true** - Rules that apply to every file (e.g., security, project overview)
- **alwaysApply: false** - Rules that apply only to specific file patterns defined in globs
- **globs** - File patterns that determine when a rule should be considered

## Usage

These rules are automatically picked up by Cursor's AI agents when:
1. You use the AI assistant in files matching the glob patterns
2. You ask questions about the project
3. You request code generation or modifications

The agents will follow these conventions to ensure consistency across the codebase.
