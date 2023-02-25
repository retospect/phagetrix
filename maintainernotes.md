# Maintainer's build notes

```
git commit 
git clean -fdx --dry-run
tox
bumpver update --patch
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```

## test:
```
pip uninstall -y phagetrix
python -m pip cache purge

pip install phagetrix

pip install --force-reinstall dist/*.whl
```
