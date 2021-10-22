# Developer's Guide


## Environment Setup

Clone the repository:

    git clone https://github.com/tellor-io/pytelliot.git

Create a virtual environment:

    python -m venv env

Activate the virtual environment

=== "Linux"

    ```
    source env/bin/activate
    ```

=== "Windows"

    ```
    .\venv\Scripts\activate.bat
    ```

Install dependencies and project

    pip install -r requirements-dev.txt
    pip install -e .

## Verify Environment

Run pytest to make sure that all tests pass:

    pytest

## Contributing


Once your dev environment is set up, make desired changes, create new tests for those changes,
and conform to the style & typing format of the project. To do so, in the project home directory:

Run tests:

    pytest

Check typing:

    mypy src --strict --implicit-reexport --ignore-missing-imports --disable-error-code misc

Check style (you may need run this step several times):

    tox -e style


Once all those pass, you're ready to make a pull request to the project's main branch.

Link any related issues, tag desired reviewers, and watch the [#pytelliot](https://discord.gg/URXVQdGjAT) channel in the
community discord for updates.