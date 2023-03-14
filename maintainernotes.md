# Maintainer's build notes

```
git clean -fdx --dry-run
tox
git commit
bumpver update --patch
# Check the colab demo!
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```

## test:

```
pip uninstall -y phagetrix quantiphy python_codon_tables

pip uninstall phagetrix -y; poetry build; pip install dist/*.whl

python -m pip cache purge

pip install phagetrix

pip install --force-reinstall dist/*.whl

poetry build; pip install --force-reinstall dist/*.whl; rehash
```
