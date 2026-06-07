# Git Workflow Guide

Complete guide to using Git for managing your local-ai-packaged repository, including how to revert changes and recover from mistakes.

## Table of Contents

- [Daily Git Commands](#daily-git-commands)
- [Viewing History](#viewing-history)
- [Reverting Changes](#reverting-changes)
- [Branch Management](#branch-management)
- [Working with Remotes](#working-with-remotes)
- [Common Scenarios](#common-scenarios)

---

## Daily Git Commands

### Check Current Status

```bash
# See what files have changed
git status

# See what branch you're on
git branch

# See your recent commits
git log --oneline -10
```

### Making Changes

```bash
# Stage specific files
git add filename.txt

# Stage all changes
git add .

# Commit with a message
git commit -m "Description of what you changed"

# Add and commit in one step (only for tracked files)
git commit -am "Your message"
```

### Pushing to GitHub

```bash
# Push to your current branch
git push

# Push and set upstream (first time)
git push -u origin branch-name
```

---

## Viewing History

### See What Changed

```bash
# View commit history (press 'q' to exit)
git log

# Compact view with one line per commit
git log --oneline

# See last 5 commits
git log --oneline -5

# See changes in a specific file
git log --oneline -- path/to/file

# View detailed changes in a commit
git show COMMIT_HASH
```

### Compare Changes

```bash
# See unstaged changes
git diff

# See staged changes
git diff --staged

# Compare two commits
git diff COMMIT1 COMMIT2

# See changes in a specific file
git diff -- path/to/file
```

---

## Reverting Changes

### Undo Uncommitted Changes

#### Discard changes in a specific file
```bash
# Restore file to last committed version
git restore filename.txt

# Or using checkout (older method)
git checkout -- filename.txt
```

#### Discard ALL uncommitted changes
```bash
# ⚠️ WARNING: This deletes all your uncommitted work!
git restore .

# Or reset everything
git reset --hard HEAD
```

#### Unstage files (keep changes)
```bash
# Remove file from staging area but keep changes
git restore --staged filename.txt

# Unstage all files
git restore --staged .
```

### Undo Committed Changes

#### Undo the last commit (keep changes)
```bash
# Undo commit but keep files staged
git reset --soft HEAD~1

# Undo commit and unstage files (keep changes in working directory)
git reset HEAD~1

# Undo last 3 commits
git reset HEAD~3
```

#### Undo the last commit (delete changes)
```bash
# ⚠️ WARNING: This permanently deletes your changes!
git reset --hard HEAD~1
```

#### Revert a specific commit (creates new commit)
```bash
# This is the SAFE way - creates a new commit that undoes changes
git revert COMMIT_HASH

# Revert without auto-committing (so you can edit)
git revert --no-commit COMMIT_HASH
```

### Go Back to a Previous Version

```bash
# View file as it was in a previous commit
git show COMMIT_HASH:path/to/file

# Restore a file from a previous commit
git restore --source=COMMIT_HASH path/to/file

# Go back to a specific commit (⚠️ detached HEAD state)
git checkout COMMIT_HASH

# Return to your branch
git checkout branch-name
```

---

## Branch Management

### Creating and Switching Branches

```bash
# Create a new branch
git branch new-feature

# Switch to a branch
git checkout new-feature

# Create and switch in one command
git checkout -b new-feature

# Modern way (Git 2.23+)
git switch new-feature
git switch -c new-feature  # create and switch
```

### Viewing Branches

```bash
# List local branches
git branch

# List all branches (including remote)
git branch -a

# See which branch you're on
git branch --show-current
```

### Merging Branches

```bash
# Switch to the branch you want to merge INTO
git checkout main

# Merge another branch into current branch
git merge feature-branch

# If there are conflicts, resolve them then:
git add .
git commit -m "Resolved merge conflicts"
```

### Deleting Branches

```bash
# Delete a local branch (safe - won't delete if unmerged)
git branch -d branch-name

# Force delete a branch
git branch -D branch-name

# Delete a remote branch
git push origin --delete branch-name
```

---

## Working with Remotes

### Fetching and Pulling

```bash
# Download changes without merging
git fetch origin

# Download and merge changes
git pull

# Pull from specific branch
git pull origin main
```

### Pushing Changes

```bash
# Push to current branch
git push

# Push to specific branch
git push origin branch-name

# Push all branches
git push --all

# Force push (⚠️ dangerous - only if you know what you're doing)
git push --force
```

### Managing Remotes

```bash
# View remotes
git remote -v

# Add a remote
git remote add origin https://github.com/username/repo.git

# Change remote URL
git remote set-url origin https://github.com/username/new-repo.git

# Remove a remote
git remote remove origin
```

---

## Common Scenarios

### Scenario 1: "I made changes but want to start over"

```bash
# Discard all uncommitted changes
git restore .

# Or if you have untracked files to delete too
git clean -fd  # -f = force, -d = directories
```

### Scenario 2: "I committed but forgot to add a file"

```bash
# Stage the forgotten file
git add forgotten-file.txt

# Amend the last commit
git commit --amend --no-edit

# Or amend and change the message
git commit --amend -m "New commit message"
```

### Scenario 3: "I pushed bad code and need to undo it"

```bash
# Option 1: Revert (creates new commit - SAFE)
git revert HEAD
git push

# Option 2: Reset and force push (⚠️ dangerous if others are using the repo)
git reset --hard HEAD~1
git push --force
```

### Scenario 4: "I want to see what the code looked like yesterday"

```bash
# Find commits from yesterday
git log --since="yesterday" --oneline

# Checkout a specific commit (read-only)
git checkout COMMIT_HASH

# When done exploring, return to your branch
git checkout main
```

### Scenario 5: "I accidentally deleted a file"

```bash
# If not committed yet
git restore deleted-file.txt

# If already committed the deletion
git restore --source=HEAD~1 deleted-file.txt
```

### Scenario 6: "I want to undo changes to just one file"

```bash
# Restore file to last committed version
git restore path/to/file

# Restore file from a specific commit
git restore --source=COMMIT_HASH path/to/file
```

### Scenario 7: "I need to update my VPS but test locally first"

```bash
# Create a test branch
git checkout -b test-update

# Make your changes and test
# ... edit files ...
git add .
git commit -m "Testing update"

# If it works, merge to main
git checkout main
git merge test-update

# If it doesn't work, just delete the branch
git checkout main
git branch -D test-update
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Check status | `git status` |
| View history | `git log --oneline` |
| Undo uncommitted changes | `git restore .` |
| Undo last commit (keep changes) | `git reset HEAD~1` |
| Undo last commit (delete changes) | `git reset --hard HEAD~1` |
| Revert a commit safely | `git revert COMMIT_HASH` |
| Create new branch | `git checkout -b branch-name` |
| Switch branch | `git checkout branch-name` |
| Push changes | `git push` |
| Pull changes | `git pull` |
| View file from old commit | `git show COMMIT:file` |

---

## Safety Tips

> [!WARNING]
> **Dangerous commands** that can lose work:
> - `git reset --hard` - Permanently deletes uncommitted changes
> - `git push --force` - Can overwrite others' work
> - `git clean -fd` - Permanently deletes untracked files

> [!TIP]
> **Safe alternatives**:
> - Use `git revert` instead of `git reset` when possible
> - Create a backup branch before experimenting: `git branch backup`
> - Test changes locally before pushing to production

> [!IMPORTANT]
> **Before any destructive operation**:
> 1. Check what will be affected: `git status`
> 2. Consider creating a backup branch
> 3. Make sure you're on the right branch: `git branch --show-current`
