# Lightweight Hyperparameter Optimization 🚀
[![Pyversions](https://img.shields.io/pypi/pyversions/mle-hyperopt.svg?style=flat-square)](https://pypi.python.org/pypi/mle-hyperopt)
[![PyPI version](https://badge.fury.io/py/mle-hyperopt.svg)](https://badge.fury.io/py/mle-hyperopt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RobertTLange/mle-hyperopt/blob/main/examples/getting_started.ipynb)
<a href="docs/logo_transparent.png_2"><img src="docs/logo_transparent.png" width="200" align="right" /></a>

Simple and intuitive hyperparameter optimization API for your Machine Learning Experiments (MLE). We assume that the objective is minimized (multiple by -1 if this is not the case). For a quickstart checkout the [notebook blog](https://github.com/RobertTLange/mle-hyperopt/blob/main/examples/getting_started.ipynb).

## The API 🎮

```python
from mle_hyperopt import RandomSearch

configs = strategy.ask(batch_size=1)
values = [train_network(c) for c in configs]
strategy.tell(configs, values)
from mle_hyperopt import RandomSearch

# Instantiate random search class
strategy = RandomSearch(real={"lrate": {"begin": 0.1,
                                        "end": 0.5}},
                        integer={"batch_size": {"begin": 32,
                                                "end": 128,
                                                "spacing": 32}},
                        categorical={"arch": ["mlp", "cnn"]})

# Simple ask - eval - tell API
configs = strategy.ask(5)
values = [train_network(**c) for c in configs]
strategy.tell(configs, values)
```

|     | Search Types           |   Description          |
| --- |----------------------- | ----------- |
| 📄  |  `GridSearch`          |  Grid search  over list of discrete values               |
| 📄  |  `RandomSearch`        |  Random search over variable ranges                 |
| 📄  |  `SMBOSearch`          |  Sequential model-based optimization                  |
| 📄  |  `CoordinateSearch`    |  Coordinate-wise optimization with defaults                  |
| 📄  |  `NevergradSearch`     |  Multi-objective optimization wrapper of nevergrad                  |


## Installation ⏳

A PyPI installation is available via:

```
pip install mle-hyperopt
```

Alternatively, you can clone this repository and afterwards 'manually' install it:

```
git clone https://github.com/RobertTLange/mle-hyperopt.git
cd mle-logging
pip install -e .
```

## Further Options 🚴

### Saving & Reloading Logs

```python
# Storing & reloading of results from .pkl
strategy.save("search_log.pkl")
strategy = RandomSearch(..., reload_path="search_log.pkl")

# Or manually add info after class instantiation
strategy = RandomSearch(...)
strategy.load("search_log.pkl")
```

### Search Decorators

```python
from mle_hyperopt import hyperopt

@hyperopt(strategy_type="grid",
          num_search_iters=25,
          real={"x": {"begin": 0., "end": 0.5, "bins": 5},
                "y": {"begin": 0, "end": 0.5, "bins": 5}})
def circle_objective(config):
    distance = abs((config["x"] ** 2 + config["y"] ** 2))
    return distance

strategy = circle_objective()
strategy.log
```

### Storing Configuration Files


```python
# Store 2 proposed configurations - eval_0.yaml, eval_1.yaml
strategy.ask(2, store=True)
```

### Retrieving Top Performers & Visualizing Results

```python
# Get the top k best configurations
# Retrieving the best performing configuration
strategy.get_best(top_k=4)
```

## Development & Milestones for Next Release

You can run the test suite via `python -m pytest -vv tests/`. If you find a bug or are missing your favourite feature, feel free to contact me [@RobertTLange](https://twitter.com/RobertTLange) or create an issue :hugs:. Here are some features I want to implement for the next release:

- [ ] Setup general parameter spaces (log uniform)
  - Add assert checks for space dictionaries
  - Add "variable" wrappers (Real, Integer, Categorical)
- [ ] Add tests for core functionality
  - Variable/space classes
  - Individual search strategies (boundary refinement, etc.)
  - Adding new data in `tell` method
  - Top-k subselection
  - Storing + reloading data
- [ ] Add rich pretty update and start-up message
- [ ] Integrate back into `mle-toolbox`
- [ ] Add basic plotting utilities
  - [ ] Grid search plot
- [ ] Easy storage of log results in `MLELogger`, `multi_update` method?
  - Or do simply via log.update(extra_obj=strategy.log, save=True) which would store log in extra/ dir
- [ ] Think about adding search decorators (runs loop with different configs)
- [ ] Add text to notebook
  - [ ] Add visualization for what is implemented
  - [ ] Add grid plot example and decorator routine
- [ ] Add simple MNIST learning rate grid search as .py
- [ ] Example with different types of variables and priors over distributions.
