<!-- markdownlint-disable MD014 -->

# PyILs: Datasets

## Setup

As soon as you clone the repo, follow the steps listed below:

1. Install the latest [Node](https://nodejs.org/en).

2. Install Node packages (development tools only):

   ```bash
   $ npm install
   ```

3. Create Python environment and install dependencies:

   ```terminal
   $ poetry install --sync
   ```

4. In VS Code, select the environment's Python as the default interpreter.
5. Test the tools installed, Ruff and Pytest:

   ```terminal
   $ ruff check .
   $ ruff format
   $ mypy .
   $ pytest
   ```

6. Install and autoupdate Pre-commit and hooks.

   ```terminal
   $ pre-commit install
   $ pre-commit install --hook-type commit-msg
   ```

   If some of the hooks are updated, commit and push the updated
   `.pre-commit-config.yaml` file.
