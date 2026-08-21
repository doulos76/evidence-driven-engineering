# Contributing

This repository follows [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/).

## Branch model at a glance

```mermaid
%%{init: { 'gitGraph': { 'mainBranchName': 'main', 'showCommitLabel': false } } }%%
gitGraph
    commit tag: "v0.1.0"
    branch develop order: 2
    checkout develop
    commit
    branch feature/example order: 3
    checkout feature/example
    commit
    commit
    checkout develop
    merge feature/example
    branch release/0.2.0 order: 1
    checkout release/0.2.0
    commit
    checkout main
    merge release/0.2.0 tag: "v0.2.0"
    checkout develop
    merge main
    checkout main
    branch hotfix/urgent-fix order: 1
    checkout hotfix/urgent-fix
    commit
    checkout main
    merge hotfix/urgent-fix tag: "v0.2.1"
    checkout develop
    merge main
```

- `main` only ever receives merges from `release/*` or `hotfix/*`, each tagged.
- `develop` receives merges from `feature/*`, `chore/*`, `docs/*`, `test/*` branches, and is synced back from `main` after every release or hotfix.
- Both `main` and `develop` are branch-protected: no direct pushes, no force-push, no deletion — all changes go through a PR.

The same flow, as a base-branch summary per workflow:

```mermaid
flowchart LR
    subgraph Regular work
        A["feature/* · chore/* · docs/* · test/*"] -->|"branch from"| D1[develop]
        A -->|"PR into"| D1
    end
    subgraph Release
        D2[develop] -->|"branch from"| R["release/x.y.z"]
        R -->|"PR into, then tag"| M1[main]
        M1 -->|"merge back"| D2
    end
    subgraph Hotfix
        M2[main] -->|"branch from"| H["hotfix/*"]
        H -->|"PR into, then tag"| M2
        M2 -->|"merge back"| D3[develop]
    end
```

## Branches

- `main` — always releasable. Every commit on `main` corresponds to a tagged
  version (`vX.Y.Z`). Never commit to `main` directly.
- `develop` — integration branch for the next release. This is the default
  branch and the base for new work.
- `feature/<name>` — new functionality or content (e.g. new reference docs,
  new scenarios, SKILL.md changes). Branch from `develop`, PR back into
  `develop`.
- `release/<version>` — release stabilization. Branch from `develop` when
  `develop` is ready to ship. Only bug fixes, version bumps, and CHANGELOG
  updates belong here — no new features. PR into `main` (tag the merge) and
  also merge back into `develop`.
- `hotfix/<name>` — urgent fix against a released version. Branch from
  `main`, PR into `main` (tag the merge) and also merge back into `develop`.
- `chore/<name>`, `docs/<name>`, `test/<name>` — non-feature work (tooling,
  docs-only changes, test runs). Same flow as `feature/*`: branch from
  `develop`, PR back into `develop`.

## Workflow

```mermaid
flowchart LR
    subgraph Regular work
        A["feature/* · chore/* · docs/* · test/*"] -->|"branch from"| D1[develop]
        A -->|"PR into"| D1
    end
    subgraph Release
        D2[develop] -->|"branch from"| R["release/x.y.z"]
        R -->|"PR into, then tag"| M1[main]
        M1 -->|"merge back"| D2
    end
    subgraph Hotfix
        M2[main] -->|"branch from"| H["hotfix/*"]
        H -->|"PR into, then tag"| M2
        M2 -->|"merge back"| D3[develop]
    end
```

### Regular work (features, fixes, docs, tests, chores)

```bash
git checkout develop
git pull origin develop
git checkout -b feature/short-description
# ... work, commit ...
git push -u origin feature/short-description
gh pr create --base develop --head feature/short-description
```

Merged branches are auto-deleted on GitHub. Delete your local branch too:

```bash
git checkout develop && git pull origin develop
git branch -d feature/short-description
```

### Cutting a release

```bash
git checkout develop
git pull origin develop
git checkout -b release/X.Y.Z
# bump version references, finalize CHANGELOG.md
git push -u origin release/X.Y.Z
gh pr create --base main --head release/X.Y.Z --title "release: vX.Y.Z"
# after merge:
git checkout main && git pull origin main
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin vX.Y.Z
# merge the release changes back into develop
git checkout develop && git pull origin develop
git merge main --no-edit
git push origin develop
```

### Hotfixing a released version

```bash
git checkout main
git pull origin main
git checkout -b hotfix/short-description
# ... fix, commit ...
git push -u origin hotfix/short-description
gh pr create --base main --head hotfix/short-description
# after merge, tag main (e.g. vX.Y.Z+1), then sync back into develop as above
```

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/) style
(`feat:`, `fix:`, `chore:`, `docs:`, `test:`, `release:`).

## Skill content changes

Changes to `SKILL.md` are the highest-leverage changes in this repo — they
alter agent behavior directly. For any non-trivial change to `SKILL.md`:

- Run (or re-run) the relevant scenarios in `tests/scenarios.md` with-skill
  vs. baseline, and record the result under `tests/results/`.
- Note in the PR description whether the change is expected to affect any
  existing behavioral test result.
