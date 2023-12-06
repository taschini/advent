# Installation notes

Install dependencies by running the following command in a virtual environment:

```
pip install --upgrade pip
pip install --upgrade more-itertools parse pre-commit pandas pytest
pre-commit install
```

Run tests with:

```
pytest -c . --doctest-modules
```
