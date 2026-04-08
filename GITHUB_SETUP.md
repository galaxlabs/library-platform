# GitHub Setup for library-platform

This repository is prepared for Galaxlabs.

## Repository name
- `library-platform`

## Contact
- **Email:** galaxylab2020@gmail.com

## GitHub Actions
A CI workflow has been added at:
- `.github/workflows/ci.yml`

It runs on push and pull request events for `main` and `master`, and includes:
- Backend dependency installation
- Django system checks
- Frontend dependency installation
- Frontend linting
- Frontend production build

## Issue and PR workflow
Issue templates are created in:
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`

Pull request template is created in:
- `.github/PULL_REQUEST_TEMPLATE.md`

## Suggested GitHub repository settings
- Enable branch protection for `main` / `master`
- Require status checks to pass before merge
- Enable code owners if you add a `CODEOWNERS` file later
- Enable required reviewers for PRs

## Release automation
A release workflow has been added at:
- `.github/workflows/release.yml`

It creates a GitHub release when a tag matching `v*` is pushed.

## How to use
1. Push code to GitHub.
2. Open a pull request.
3. GitHub Actions runs CI automatically.
4. Merge when CI passes.

## Notes
- Update the workflow if you add real tests.
- Replace the default contact email with the GitHub organization or team if needed.
- Add a `CODEOWNERS` file once the team is finalized.
