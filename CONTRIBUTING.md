
# Contributing

## 1. General guidelines

This document defines the conventions for contributing to **Gestor-de-horarios-universitarios**. All contributors should follow these conventions to keep the repository consistent, organized and easy to maintain.

## 2. Branch naming

Branches must have a recognizable prefix that identifies their purpose, followed by a short description using hyphens to separate words.

The following prefixes are established:

- `FEATURE-`: new functionality or implementations intended for users.
- `FIX-`: bug fixes and error corrections.
- `INTERNAL-`: internal project configuration and maintenance, including repository conventions and development workflow.

Examples:

- `FEATURE-login`
- `FIX-missing-semicolon`
- `INTERNAL-Contributing`

Branch names should clearly communicate the purpose of the work.

## 3. Pull request naming

Pull request titles must clearly describe the purpose of the proposed changes.

Use the relevant prefix and a concise description, following the project's established naming conventions. For internal configuration work, use the `INTERNAL-` prefix.

Examples:

- `INTERNAL-001 Standardize contribution conventions`
- `FEATURE-001 Implement login`
- `FIX-001 Correct missing semicolon`

Each pull request must target the appropriate base branch for the work being integrated. When working on a shared integration branch, contributors must select that branch as the pull request's base rather than automatically targeting `main`.

Pull request descriptions must explain the changes made and their purpose. When a pull request resolves an issue, include the appropriate GitHub closing keyword and issue number in the description, preferably in its first line.

Example:

`Closes #7`

GitHub closing keywords should be used in pull request descriptions so that issues are automatically closed when the pull request is merged into the repository's default branch.

## 4. Issue labels

Issues must use labels to identify their purpose and help organize project work.

The following labels and their meanings are established:

- `user-story`: issues representing user stories, needs or problems from the user's perspective.
- `internal-config`: internal repository organization and configuration, including naming conventions, collaborators, Kanban and repository structure.
- `development`: issues directly related to developing product functionality or components.
- `documentation`: tasks focused on documenting concepts, decisions or domain knowledge.
- `tech-stack`: decisions concerning the technology stack, including languages, versions and technologies.
- `tools`: selection or configuration of development tools, dependency managers and code quality tools.

### 4.1. Issue prefixes

Issue prefixes must correspond to their associated labels:

| Prefix | Label | Purpose |
| --- | --- | --- |
| `HU` | `user-story` | User stories |
| `IN` | `internal-config` | Internal configuration |
| `DV` | `development` | Product development |
| `DC` | `documentation` | Documentation |
| `TS` | `tech-stack` | Technology stack |
| `TL` | `tools` | Development tools |

Issues should retain their assigned identifiers and use a concise, descriptive title.

Examples:

- `[HU001] No sé a qué clases de la universidad tengo que ir, a qué hora ni a dónde`
- `[IN005] Establecimiento nomenclatura PR`
- `[DV001] Implementar una nueva funcionalidad`

## 5. Milestone naming

Milestones must follow a consistent naming format:

`[MX]: Brief description of the product content`

The description should summarize the scope or content covered by the milestone.

Example:

`[M00]: Preparación base`

## 6. General contribution workflow

Before submitting a contribution:

1. Identify the issue associated with the work, when applicable.
2. Create a branch using the appropriate naming prefix.
3. Implement the changes within the scope of the issue.
4. Review the changes before submitting them.
5. Create a pull request with a descriptive title and an explanation of the changes.
6. Reference the associated issue using a GitHub closing keyword in the pull request description when the work resolves that issue.
7. Select the correct base branch for the pull request.

Contributors should keep changes focused, follow the established conventions and ensure that the purpose of each branch and pull request is clear.
