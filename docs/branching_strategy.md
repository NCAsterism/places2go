# Branching Strategy

This document details the recommended Git branching strategy for the Destination Dashboard project.  Following a consistent workflow ensures that contributors can work independently on features, fix issues without disrupting the main code base, and release stable versions with confidence.

## Branches

- **`main`** — The production branch.  Only production‑ready code should be merged here.  Each release is tagged on this branch.
- **`develop`** — The integration branch where features are assembled and tested together.  This branch may be unstable and is not intended for deployment.
- **`feature/<name>`** — Short‑lived branches that contain the work for a specific feature.  Base these on `develop` and merge back into `develop` when complete.
- **`release/<version>`** — Preparation branches created when a stable version of `develop` is ready to be released.  Use these to bump version numbers, update documentation, and perform final testing.  Merge into both `main` and `develop` once the release is finished.
- **`hotfix/<issue>`** — Emergency branches created to address critical issues in production.  Base these on `main` and merge back into both `main` and `develop` after the fix.

## Workflow

1. **Create an issue.**  Before starting any work, open an issue describing the task or bug to be addressed.  Assign it to yourself or the appropriate GitHub agent.
2. **Create a feature branch.**  From `develop`, create a branch named `feature/<short‑description>` (e.g. `feature/weather-data`).  Implement your changes on this branch.
3. **Commit and push.**  Make frequent, small commits with descriptive messages.  Push your branch regularly to ensure your work is backed up and to allow collaboration.
4. **Open a pull request.**  When the feature is ready, open a pull request (PR) from your feature branch into `develop`.  Link the PR to the original issue.
5. **Code review and testing.**  Another contributor or GitHub agent reviews the PR.  Continuous integration runs tests automatically.  Fix any issues uncovered during this process.
6. **Merge.**  Once approved, the PR is merged into `develop`.  Delete the feature branch after merging to keep the repository clean.
7. **Release.**  When `develop` has accumulated enough completed features and passes all tests, cut a `release/<version>` branch and prepare for deployment.  After final checks, merge into `main`, tag the release, and merge back into `develop` to keep branches in sync.

Adhering to this workflow helps avoid merge conflicts, ensures that the `main` branch remains stable, and encourages thorough testing before deployment.