# Contributing to Places2Go

Thank you for your interest in contributing! This guide will help you get started.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Pull Request Process](#pull-request-process)
5. [Development Guidelines](#development-guidelines)
6. [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. By participating in this project, you agree to maintain a respectful and harassment-free environment.

### Expected Behavior

- ✅ Be respectful and inclusive
- ✅ Welcome newcomers and help them get started
- ✅ Accept constructive criticism gracefully
- ✅ Focus on what is best for the community
- ✅ Show empathy towards other community members

### Unacceptable Behavior

- ❌ Harassment, discrimination, or offensive comments
- ❌ Personal attacks or trolling
- ❌ Public or private harassment
- ❌ Publishing others' private information
- ❌ Other conduct inappropriate for a professional setting

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- GitHub account
- Git installed
- Python 3.9-3.12
- Familiarity with Python and Git basics

### Initial Setup

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/places2go.git
   cd places2go
   ```

3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/NCAsterism/places2go.git
   ```

4. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\Activate.ps1  # Windows
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run tests to verify setup:**
   ```bash
   pytest
   ```

---

## How to Contribute

### Ways to Contribute

#### 🐛 Report Bugs

Found a bug? Help us fix it!

1. Check [existing issues](https://github.com/NCAsterism/places2go/issues) to avoid duplicates
2. Use the [bug report template](https://github.com/NCAsterism/places2go/issues/new?template=bug_report.md)
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs. actual behavior
   - System information (OS, Python version)
   - Error messages or screenshots

**Example:**
```markdown
**Description:** Dashboard crashes when loading empty CSV

**Steps to Reproduce:**
1. Create empty CSV file in data/
2. Run `python scripts/dashboard.py`
3. See error

**Expected:** Graceful error message
**Actual:** Stack trace crash

**Environment:**
- OS: Windows 11
- Python: 3.11.5
```

#### 💡 Suggest Features

Have an idea for improvement?

1. Check [existing feature requests](https://github.com/NCAsterism/places2go/issues?q=is%3Aissue+is%3Aopen+label%3Afeature)
2. Use the [feature request template](https://github.com/NCAsterism/places2go/issues/new?template=feature_request.md)
3. Describe:
   - Problem it solves
   - Proposed solution
   - Alternative approaches
   - Additional context

#### ✅ Improve Tests

Help us reach 90%+ coverage!

1. Use the [test request template](https://github.com/NCAsterism/places2go/issues/new?template=test_request.md)
2. Focus on:
   - Untested functions
   - Edge cases
   - Error handling
   - Integration tests

#### 📖 Improve Documentation

Documentation is always welcome!

- Fix typos or unclear sections
- Add examples
- Improve wiki pages
- Update README
- Add code comments

#### 💻 Write Code

Ready to code? Great!

1. **Find an issue:**
   - Browse [good first issues](https://github.com/NCAsterism/places2go/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
   - Look for issues in current [milestone](https://github.com/NCAsterism/places2go/milestones)
   - Check [Phase 2 tasks](https://github.com/NCAsterism/places2go/issues?q=is%3Aissue+is%3Aopen+label%3Aphase-2)

2. **Comment on the issue:**
   ```markdown
   I'd like to work on this issue. ETA: 3 days.
   ```

3. **Wait for assignment** (maintainer will assign it to you)

4. **Create feature branch:**
   ```bash
   git checkout develop
   git pull upstream develop
   git checkout -b feature/issue-number-description
   ```

5. **Make changes** following our [Development Guide](Development-Guide)

6. **Test thoroughly:**
   ```bash
   pytest --cov=scripts --cov=tests
   black scripts/ tests/
   flake8 scripts/ tests/
   ```

7. **Commit with conventional commit format:**
   ```bash
   git commit -m "feat(dashboard): add temperature filter"
   ```

8. **Push and create PR:**
   ```bash
   git push origin feature/issue-number-description
   ```

---

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows our [Code Style](Code-Style)
- [ ] All tests pass (`pytest`)
- [ ] Code is formatted (`black`)
- [ ] Linting passes (`flake8`)
- [ ] Added tests for new functionality
- [ ] Updated documentation
- [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] Branch is up-to-date with `develop`

### Creating the PR

1. **Push your branch to your fork**
2. **Go to GitHub and create Pull Request**
3. **Target:** `develop` branch (not `main`)
4. **Title:** Clear, descriptive (use conventional commit format)
5. **Description:** Use the PR template

**PR Template:**
```markdown
## Description
Brief description of changes

## Related Issue
Closes #42

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code formatted with Black
- [ ] Flake8 passes
- [ ] All tests pass
```

### Review Process

1. **Automated checks run** (CI pipeline)
2. **Maintainer reviews code**
3. **Feedback provided** (if needed)
4. **You address feedback** and push updates
5. **PR approved and merged**

### After Merge

- Your branch will be deleted
- Changes appear in `develop` branch
- Closes related issues automatically
- You'll be added to contributors list! 🎉

---

## Development Guidelines

### Code Style

- **Python:** Black formatter (88 char line length)
- **Linting:** Flake8
- **Type hints:** Required (Phase 2+)
- **Docstrings:** Google style

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Formatting
- `chore:` Maintenance
- `ci:` CI/CD changes

**Examples:**
```bash
feat(dashboard): add weather filter component
fix(data): handle missing CSV columns gracefully
docs(wiki): update installation guide
test(dashboard): add chart generation tests
```

### Testing Standards

- **Coverage:** 90%+ for new code
- **Test types:** Unit, integration, edge cases
- **Naming:** `test_<function>_<scenario>`
- **Assertions:** Use descriptive assertions

### Documentation

- **Code:** Docstrings for all public functions/classes
- **README:** Keep updated with features
- **Wiki:** Add/update relevant pages
- **Comments:** Explain why, not what

---

## Community

### Communication Channels

- **Issues:** [GitHub Issues](https://github.com/NCAsterism/places2go/issues)
- **Discussions:** [GitHub Discussions](https://github.com/NCAsterism/places2go/discussions)
- **Pull Requests:** [GitHub PRs](https://github.com/NCAsterism/places2go/pulls)

### Getting Help

- 📖 **Documentation:** Browse this wiki
- 🤔 **Questions:** Open a [discussion](https://github.com/NCAsterism/places2go/discussions)
- 🐛 **Bugs:** Report an [issue](https://github.com/NCAsterism/places2go/issues/new?template=bug_report.md)
- 💬 **Chat:** Comment on relevant issues/PRs

### Recognition

We value all contributions! Contributors are:
- Added to `CONTRIBUTORS.md`
- Credited in release notes
- Eligible for "Contributor" badge
- Part of our community

---

## Development Phases

### Current: Phase 2 (v0.2.0)
**Focus:** Testing & Code Quality  
**Timeline:** October 4-18, 2025

**Active Issues:**
- [#1 Comprehensive Test Suite](https://github.com/NCAsterism/places2go/issues/1)
- [#2 Type Hints](https://github.com/NCAsterism/places2go/issues/2)
- [#3 Mypy Integration](https://github.com/NCAsterism/places2go/issues/3)
- [#4 Logging Framework](https://github.com/NCAsterism/places2go/issues/4)
- [#5 Custom Exceptions](https://github.com/NCAsterism/places2go/issues/5)
- [#6 Pydantic Models](https://github.com/NCAsterism/places2go/issues/6)
- [#7 Pre-commit Hooks](https://github.com/NCAsterism/places2go/issues/7)
- [#8 Error Handling](https://github.com/NCAsterism/places2go/issues/8)

See [Roadmap](Roadmap) for future phases.

---

## Quick Links

- 🚀 [Quick Start](Quick-Start)
- 🛠️ [Development Guide](Development-Guide)
- 🧪 [Testing Guide](Testing)
- 🏗️ [Architecture](Architecture)
- 📊 [Roadmap](Roadmap)
- ❓ [FAQ](FAQ)

---

## Thank You!

Your contributions make Places2Go better for everyone. Whether you're fixing a typo, reporting a bug, or adding a major feature, we appreciate your effort! 🙏

**Happy contributing! 🌍✈️**

---

**License:** By contributing, you agree that your contributions will be licensed under the MIT License.
