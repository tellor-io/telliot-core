## dev setup
- Clone repository
```
git clone https://github.com/tellor-io/pytelliot.git && cd pytelliot
```
- Create virtual environment
```
python -m venv env
```
- Activate virtual environment
```
source env/bin/activate
```
- Install dependencies
```
pip install -r requirements-dev.txt
```
- Once your dev environment is set up, make desired changes, create new tests for those changes,
and conform to the style & typing format of the project. To do so, in the project home directory:

Run tests:
```
pytest
```
Check typing:
```
mypy src --strict --implicit-reexport --ignore-missing-imports --disable-error-code misc
```
Check style:
```
tox -e style
```
(you may need to make changes and run again)
- Once all those pass, you're ready to make a pull request to the project's main branch.
- Link any related issues, tag desired reviewers, and watch the [#pytelliot](https://discord.gg/URXVQdGjAT) channel in the
community discord for updates.