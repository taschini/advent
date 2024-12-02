# Installation notes

Install dependencies by running the following commands in a virtual environment:

```shell
pip install --upgrade pip
pip install --upgrade more-itertools parse pre-commit pandas pytest z3-solver 'networkx[default]'
pre-commit install
```

Run tests with:

```shell
pytest -c . --doctest-modules
```
