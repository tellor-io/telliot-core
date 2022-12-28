# Contributing

## Development Environment Setup

### Prerequisites
- Python (version >=3.9 & <3.10)

Clone the repository to a local working directory:

    git clone https://github.com/tellor-io/telliot-core.git

Create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) in that cloned repo. In this example, the virtual environment is called `tenv`:

=== "Linux"

    ```
    python3 -m venv tenv
    source tenv/bin/activate
    ```

=== "Windows"

    ```
    py -m venv tenv
    tenv\Scripts\activate
    ```

Install the project using using an [editable installation](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs).

    pip install -e .
    pip install -r requirements-dev.txt

## Test Environment

Make sure you've [configured Telliot](https://tellor-io.github.io/telliot-feed-examples/getting-started/) before continuing.

Verify the development environment by running `pytest` and ensure that all tests pass.

    pytest

## Making Contributions

Once your dev environment is set up, make desired changes, create new tests for those changes,
and conform to the style & typing format of the project. To do so, in the project home directory:

Run all unit tests:

    pytest

Check code typing:

    tox -e typing

Check style (you may need run this step several times):

    tox -e style

Once all those pass, you're ready to make a pull request to the project's main branch.

Link any related issues, tag desired reviewers, and watch the [#telliot-core](https://discord.gg/URXVQdGjAT) channel in the
community discord for updates.

## New Release Process/Checklist

For manually creating a new package version release:

1. Ensure all tests are passing on main.
2. Remove "dev" from **version** in the main package's **init**.py . Example: **version** = "0.0.5dev" --> **version** = "0.0.5".
3. On Github, go to Releases-->Draft a new release-->Choose a tag
4. Write in a new tag that corresponds with the version in **init**.py. Example: v.0.0.5
5. If the tag is v.0.0.5, the release title should be Release 0.0.5.
6. Click Auto-generate release notes.
7. Check the box for This is a pre-release.
8. Click Publish release.
9. Navigate to the Actions tab from the main page of the package on github and make sure the release workflow completes successfully.
10. Check to make sure the new version was released to test PyPI [here](https://test.pypi.org/project/telliot-core/).
11. Test downloading and using the new version of the package from test PyPI ([example](https://stackoverflow.com/questions/34514703/pip-install-from-pypi-works-but-from-testpypi-fails-cannot-find-requirements)).
12. Navigate back to the pre-release you just made and click edit (the pencil icon).
13. Uncheck the This is a pre-release box.
14. Publish the release.
15. Make sure the release github action goes through.
16. Download and test the new release on PyPI official [here](https://pypi.org/project/telliot-core/).
17. Change the package version in **init**.py to be the next development version. For example, if you just released version 0.0.5, change **version** to be "0.0.6dev0".
