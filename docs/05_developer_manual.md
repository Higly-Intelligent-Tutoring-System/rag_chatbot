## 🛠️ Development Workflow

Follow these steps when fixing a bug or adding a feature:

1. **Set up the environment.** Follow the instructions in the [user manual](./04_user_manual.md) to install dependencies and configure the project locally. Confirm the application runs before making changes.

2. **Create a branch.** Start from the appropriate base branch and create a separate branch for your work. Use a clear, descriptive name, such as `fix/login-error` or `feat/document-upload`.

3. **Make focused changes.** Keep changes related to one fix or feature where possible. Follow the project’s existing code style and conventions.

4. **Run the tests.** Run the relevant tests, then run the full test suite if available. Make sure your changes do not break existing functionality, and add or update tests for the behaviour you changed.

5. **Write a Conventional Commit.** Use the project’s commit message format:

   ```text
   <type>(optional scope): <short description>
   ```

   Common types include `feat` for a new feature, `fix` for a bug fix, `docs` for documentation, `test` for tests, and `refactor` for code changes that do not add a feature or fix a bug.

6. **Follow Semantic Versioning for releases.** When preparing a release, update the version according to the change: **MAJOR** for incompatible changes, **MINOR** for backwards-compatible features, and **PATCH** for backwards-compatible fixes.

Before submitting your work, ensure the branch is up to date with the project’s base branch and that all applicable tests pass.

This process is suggested even if you make your own fork of the repository, just to maintain a good habit.

### Running Tests
You can run tests for the entire monorepo or specific packages.

```bash
# Run ALL tests
uv run pytest

# Run tests for a specific package
uv run --package document-loader pytest
```

### Adding Dependencies
Because this is a workspace, you must specify which package receives the dependency.
In the examples below you will be guided to add a dependency only to the required one.

```bash
# Add 'pandas' to the document-loader only
uv add pandas --package document-loader

# Add 'httpx' to the shared core library
uv add httpx --package core
```

In case you added one by mistake, you can remove it by typing:

```bash
# Removes 'pandas' to the document-loader only
uv remove <lib> --package <package>
```