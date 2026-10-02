# AI Agent Guidelines

## Project Overview

- Language: Python >=3.12, <3.13
- GUI Framework: wxPython
- Dependency Manager: uv

## Directory Structure

### Source Code
- Write all comments and docstrings in English
- Main project sources: `src/`
- Python package root: `src/outwiker/`
- Wiki notation token classes for wiki pages: `src/outwiker/pages/wiki/parser/`

### Plugins
- Plugin sources: `plugins/`

### Build Tools
- Build package sources: `owbuildtools/`

### Testing
- Test location: `src/outwiker/tests`
- Test runner: pytest
- Wiki notation tests: `src/outwiker/tests/wikiparser/`
- Plugins tests: `src/outwiker/tests/plugins/`
- Activate the virtual environment from `.venv` before running tests
- Run tests without the `-q` flag

### Documentation
- Documentation sources: `doc/`

