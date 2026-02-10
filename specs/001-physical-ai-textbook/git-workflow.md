# Git Workflow Documentation

**Project**: Physical AI & Humanoid Robotics Educational Textbook
**Last Updated**: 2026-02-10
**Version**: 1.0

---

## Table of Contents

1. [Overview](#overview)
2. [Branch Naming Conventions](#branch-naming-conventions)
3. [Commit Message Format](#commit-message-format)
4. [Pull Request Process](#pull-request-process)
5. [Code Review Criteria](#code-review-criteria)
6. [Merge Strategy](#merge-strategy)
7. [Release Process](#release-process)
8. [Common Workflows](#common-workflows)

---

## Overview

This document defines the Git workflow for the Physical AI textbook project, ensuring consistency, traceability, and quality across all contributions.

### Principles

- **Single-threaded focus**: One module at a time (FR-046)
- **Incremental validation**: Each module validated before next (FR-047)
- **Quality gates**: All changes reviewed before merge (FR-048)
- **Traceability**: All commits linked to tasks/issues

---

## Branch Naming Conventions

### Format

```
<type>/<scope>-<description>
```

### Types

| Type | Purpose | Example |
|------|---------|---------|
| `feature/` | New module, chapter, or functionality | `feature/module-0` |
| `fix/` | Bug fixes | `fix/broken-diagram-rendering` |
| `docs/` | Documentation updates | `docs/update-readme` |
| `refactor/` | Code refactoring (no behavior change) | `refactor/sidebar-structure` |
| `test/` | Test additions or modifications | `test/add-validation-checks` |
| `chore/` | Build, dependencies, tooling | `chore/update-docusaurus` |
| `hotfix/` | Critical production fixes | `hotfix/security-patch` |

### Examples

✅ **Good**:
- `feature/module-0-intro`
- `feature/module-1-ros2`
- `fix/mermaid-diagram-rendering`
- `docs/add-contributor-guide`
- `chore/update-dependencies`

❌ **Bad**:
- `my-branch` (no type)
- `fix` (no description)
- `feature/everything` (too broad)
- `temp` (non-descriptive)

### Special Branches

- **`main`**: Production branch (protected)
- **`gh-pages`**: Auto-generated deployment branch (do not modify manually)
- **`001-physical-ai-textbook`**: Feature branch for initial textbook development

---

## Commit Message Format

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Components

#### Type (Required)

| Type | Description | When to Use |
|------|-------------|-------------|
| `feat` | New feature | Adding new module/chapter/section |
| `fix` | Bug fix | Fixing broken links, typos, errors |
| `docs` | Documentation | README, specs, ADRs, guides |
| `style` | Formatting, CSS | Styling changes (no logic change) |
| `refactor` | Code refactoring | Restructuring without behavior change |
| `test` | Test additions | Adding validation, test scripts |
| `chore` | Maintenance | Dependencies, build config, tooling |
| `perf` | Performance | Optimization improvements |
| `revert` | Revert previous commit | Rolling back changes |

#### Scope (Optional but Recommended)

Identifies the area of change:

- `module-0`, `module-1`, ..., `module-5` - Content modules
- `chapter-X` - Specific chapter
- `ci` - CI/CD pipeline
- `deps` - Dependencies
- `config` - Configuration files
- `templates` - Content templates
- `docs` - Documentation

#### Subject (Required)

- **Max 50 characters**
- **Imperative mood** ("add" not "added" or "adds")
- **No period at end**
- **Lowercase** (except proper nouns)

#### Body (Optional)

- **Wrap at 72 characters**
- Explain **what** and **why** (not how)
- Separate from subject with blank line

#### Footer (Optional)

- Reference issues/tasks: `Closes #123`, `Implements T042`
- Breaking changes: `BREAKING CHANGE: description`
- Co-authors: `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`

### Examples

#### Simple Commit

```
feat(module-0): add introduction chapter

Implements T022 from Task.md
```

#### Detailed Commit

```
feat(module-1): add ROS 2 architecture chapter

Added comprehensive coverage of ROS 2 architecture including:
- DDS middleware layer
- Node communication patterns
- Quality of Service (QoS) policies
- Python (rclpy) examples with live code playgrounds

Includes 4 Mermaid diagrams and 8 IEEE citations (all open-access).

Implements T045-T048
Closes #12
```

#### Fix Commit

```
fix(module-0): correct broken citation links

Three citations in principles.mdx were returning 404 errors.
Replaced with updated URLs from arXiv and IEEE Xplore.

Fixes #15
```

#### Chore Commit

```
chore(deps): update docusaurus to 3.9.2

Updates Docusaurus and plugins to latest stable versions.
Addresses 2 moderate security vulnerabilities in dependencies.
```

#### Breaking Change

```
refactor(templates): restructure module template format

BREAKING CHANGE: Module template frontmatter structure changed.
Old templates must be updated to new format with assessment section.

Migration guide added to docs/migration.md
```

### AI-Assisted Commits

When AI contributes to commits, include co-author:

```
feat(module-2): add Gazebo simulation chapter

Comprehensive Gazebo coverage with 6 interactive examples.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## Pull Request Process

### 1. Create Feature Branch

```bash
# From main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/module-0-intro
```

### 2. Make Changes

```bash
# Make your changes, add files
git add frontend/docs/module-0/intro.mdx

# Commit with proper format
git commit -m "feat(module-0): add introduction section

Implements T021 from Task.md"
```

### 3. Push to Remote

```bash
# Push feature branch
git push -u origin feature/module-0-intro
```

### 4. Create Pull Request

1. Navigate to GitHub repository
2. Click "Pull requests" → "New pull request"
3. Select base: `main` and compare: `feature/module-0-intro`
4. Fill out PR template (auto-populated from `.github/PULL_REQUEST_TEMPLATE.md`)
5. Complete all checklist items
6. Request review from designated reviewer
7. Add labels: `content`, `module-0`, `in-progress`, etc.

### 5. Address Review Comments

```bash
# Make requested changes
git add <files>
git commit -m "fix(module-0): address review comments"
git push origin feature/module-0-intro
```

### 6. Merge After Approval

- ✅ All checklist items complete
- ✅ CI/CD build passes
- ✅ At least 1 approval (if branch protection enabled)
- ✅ No merge conflicts

Merge methods:
- **Preferred**: "Squash and merge" (clean history)
- **Alternative**: "Merge commit" (preserve detailed history)
- **Avoid**: "Rebase and merge" (can complicate history)

---

## Code Review Criteria (FR-048)

### Content Review

#### Must Have
- [ ] Content completeness (all sections present per template)
- [ ] Technical accuracy (concepts, commands, code verified)
- [ ] Academic standards (appropriate for university-level)
- [ ] Citations in IEEE format (100% open-access per SC-007)
- [ ] Diagrams render correctly (Mermaid, C4, images)
- [ ] Code examples functional (tested in environment)
- [ ] Cross-references work (internal links)

#### Should Have
- [ ] Clear learning objectives
- [ ] Progressive difficulty (builds on prerequisites)
- [ ] Self-assessment questions
- [ ] Practical examples and use cases

### Technical Review

#### Must Have
- [ ] Build completes successfully (`npm run build`)
- [ ] No console errors in browser
- [ ] No broken links (internal or external)
- [ ] No security issues (secrets, vulnerabilities)
- [ ] Performance acceptable (<2s page load per FR-014)

#### Should Have
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Accessibility (WCAG 2.1 AA recommended)
- [ ] SEO optimization (meta descriptions, titles)

### Process Review

#### Must Have
- [ ] Branch naming correct
- [ ] Commit messages follow format
- [ ] PR template complete
- [ ] Linked to task/issue
- [ ] No merge conflicts

---

## Merge Strategy

### Protected Branch Rules (main)

**Requires Human Setup** (T018):
1. Settings → Branches → Add rule for `main`
2. Enable:
   - ✅ Require pull request before merging
   - ✅ Require 1 approval
   - ✅ Require status checks to pass (build, tests)
   - ✅ Do not allow bypassing
3. Disable:
   - ❌ Allow force pushes
   - ❌ Allow deletions

### Merge Commit Message

Auto-generated format:
```
Merge pull request #123 from user/feature/module-0

feat(module-0): add introduction chapter
```

---

## Release Process

### Continuous Deployment (Current)

- **Trigger**: Push to `main` branch
- **Pipeline**: GitHub Actions (`.github/workflows/deploy.yml`)
- **Steps**:
  1. Build Docusaurus site (`npm run build`)
  2. Deploy to GitHub Pages (`gh-pages` branch)
  3. Live at: https://msaleemakhtar.github.io/hackathine_1/

### Versioning (Future)

When project matures:
- Use Git tags for releases: `v1.0.0`, `v1.1.0`
- Follow Semantic Versioning (SemVer)
- Create release notes for each version

---

## Common Workflows

### Starting New Module

```bash
# 1. Ensure on latest main
git checkout main
git pull origin main

# 2. Create module branch
git checkout -b feature/module-1-ros2

# 3. Create module structure
mkdir -p frontend/docs/module-1
cp .specify/templates/module-template.mdx frontend/docs/module-1/index.mdx

# 4. Make edits, then commit
git add frontend/docs/module-1/
git commit -m "feat(module-1): initialize ROS 2 module structure

Implements T045 from Task.md"

# 5. Push and create PR
git push -u origin feature/module-1-ros2
# Then create PR on GitHub
```

### Fixing Broken Link

```bash
# 1. Create fix branch
git checkout -b fix/broken-citation-link

# 2. Fix the link
# Edit the file...

# 3. Commit
git add frontend/docs/module-0/principles.mdx
git commit -m "fix(module-0): correct broken citation link in principles

Citation #3 was returning 404. Updated with working arXiv link.

Fixes #25"

# 4. Push and create PR
git push -u origin fix/broken-citation-link
```

### Updating Dependencies

```bash
# 1. Create chore branch
git checkout -b chore/update-dependencies

# 2. Update packages
cd frontend
npm update
npm audit fix

# 3. Test build
npm run build

# 4. Commit
git add package.json package-lock.json
git commit -m "chore(deps): update npm dependencies

- Updated Docusaurus to 3.9.3
- Fixed 2 moderate vulnerabilities
- All tests passing"

# 5. Push and create PR
git push -u origin chore/update-dependencies
```

### Handling Merge Conflicts

```bash
# 1. Update your branch with latest main
git checkout feature/module-1-ros2
git fetch origin
git rebase origin/main

# 2. Resolve conflicts
# Edit conflicting files...
git add <resolved-files>
git rebase --continue

# 3. Force push (rebase rewrites history)
git push --force-with-lease origin feature/module-1-ros2
```

### Rollback After Bad Merge

```bash
# Option 1: Revert merge commit
git revert -m 1 <merge-commit-sha>
git push origin main

# Option 2: Reset to previous commit (DANGEROUS - requires force push)
# Only use if absolutely necessary and communicate with team
git reset --hard <previous-good-commit-sha>
git push --force origin main  # Requires admin override on protected branch
```

---

## Git Commands Quick Reference

### Daily Commands

```bash
# Check status
git status

# View commit history
git log --oneline --graph --decorate --all

# View changes
git diff                    # Unstaged changes
git diff --staged          # Staged changes
git diff main              # Diff against main

# Stash changes temporarily
git stash                  # Save changes
git stash pop             # Restore changes

# Update from remote
git fetch origin          # Download changes
git pull origin main      # Fetch + merge
```

### Branch Management

```bash
# List branches
git branch -a             # All branches (local + remote)
git branch -vv            # Branches with tracking info

# Delete branch
git branch -d feature/old-branch    # Safe delete (merged only)
git branch -D feature/old-branch    # Force delete

# Rename branch
git branch -m old-name new-name
```

### Undoing Changes

```bash
# Unstage file
git restore --staged <file>

# Discard changes in working directory
git restore <file>

# Amend last commit (only if not pushed)
git commit --amend

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

---

## Best Practices

### Do's ✅

- **Commit early, commit often** - Small, focused commits
- **Write descriptive messages** - Future you will thank you
- **Reference tasks/issues** - Maintain traceability
- **Test before committing** - Run `npm run build` first
- **Review your own changes** - Use `git diff` before committing
- **Keep branches short-lived** - Merge within 1-3 days
- **Rebase frequently** - Keep branch up-to-date with main
- **Use .gitignore** - Never commit .env, node_modules, build/

### Don'ts ❌

- **Don't commit secrets** - API keys, passwords, tokens
- **Don't commit binary files** - Large images, videos (use Git LFS if needed)
- **Don't commit generated files** - build/, .docusaurus/, node_modules/
- **Don't force push to main** - Destroys team's history
- **Don't work directly on main** - Always use feature branches
- **Don't merge your own PRs** - Wait for review (unless solo)
- **Don't ignore merge conflicts** - Resolve carefully
- **Don't use generic messages** - "fix stuff", "update", "wip"

---

## Troubleshooting

### "Your branch is ahead of origin/main by X commits"

```bash
# If you meant to create a new branch:
git checkout -b feature/my-new-feature
git push -u origin feature/my-new-feature

# If you accidentally committed to main:
git checkout -b feature/my-changes
git push -u origin feature/my-changes
git checkout main
git reset --hard origin/main
```

### "Failed to push - rejected"

```bash
# Usually means remote has changes you don't have
git pull --rebase origin main
git push origin feature/my-branch
```

### "Merge conflict"

```bash
# 1. Identify conflicting files
git status

# 2. Open files, resolve conflicts (look for <<<<<<<, =======, >>>>>>>)

# 3. Stage resolved files
git add <resolved-files>

# 4. Complete merge/rebase
git rebase --continue  # If rebasing
git commit             # If merging
```

---

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Writing Good Commit Messages](https://cbea.ms/git-commit/)

---

**Version History**:
- **1.0** (2026-02-10): Initial workflow documentation
