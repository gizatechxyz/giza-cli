# Installation

* [Installation](Installation.md#-installation)
  * [Recommended installation with pipx](Installation.md#recommended-installation-with-pipx)
  * [Install from PyPi](Installation.md#install-from-pypi)
  * [Installing from source](Installation.md#installing-from-source)

## Handling Python versions with Pyenv

As we are using Python 3.11, it's recommended to use [Pyenv](https://github.com/pyenv/pyenv) to manage your Python versions. Here are the steps to install Pyenv and set Python 3.11 as your local version:

1. First, we need to get pyenv, for information about how to install it, please refer to the [official documentation](https://github.com/pyenv/pyenv)

2. Install Python 3.11 with Pyenv:

```bash
pyenv install 3.11.5
```

3. Set Python 3.11 as the local version for your project:

```bash
pyenv local 3.11.5
```

Now, your terminal session will use Python 3.11 for this project.

## Recommended installation with pipx

[pipx](https://pypa.github.io/pipx/) allows the installation of the dependency in an isolated environment. With this, we can make sure that it does not conflict with any of our installed dependencies.

```bash
pipx install giza-cli
```

## Install from PyPi

For the latest release:

```bash
pip install giza-cli
```

## Installing from source

Clone the repository and install it with `pip`:

```bash
git clone git@github.com:gizatechxyz/giza-cli.git
cd giza-cli
pip install .
```

Or install it directly from the repo:

```bash
pip install git+ssh://git@github.com/gizatechxyz/giza-cli.git
```
