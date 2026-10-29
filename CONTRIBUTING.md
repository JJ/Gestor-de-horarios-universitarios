
## Branch naming

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

## Pull request naming

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
