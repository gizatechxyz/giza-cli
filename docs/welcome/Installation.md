# Installation

* [🚀 Installation](Installation.md#-installation)
  * [Recomended installation with pipx](Installation.md#recomended-installation-with-pipx)
  * [Install from PyPi](Installation.md#install-from-pypi)
  * [Installing from source](Installation.md#installing-from-source)

## Recomended installation with pipx

[pipx](https://pypa.github.io/pipx/) allows to install the dependency in an isolated environment. With ths we can make sure that it does not conflict with any of our installed dependencies.

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
