# Maintainer's build notes

```
git clean -fdx --dry-run
black tests/*.py src/phagetrix/*.py
tox
git commit 
bumpver update --patch
# Check the colab demo!
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```

## test:
```
pip uninstall -y phagetrix
python -m pip cache purge

pip install phagetrix

pip install --force-reinstall dist/*.whl

poetry build; pip install --force-reinstall dist/*.whl; rehash
```
