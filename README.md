# mdocfile

[![License](https://img.shields.io/pypi/l/mdocfile.svg?color=green)](https://github.com/alisterburt/mdocfile/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mdocfile.svg?color=green)](https://pypi.org/project/mdocfile)
[![Python Version](https://img.shields.io/pypi/pyversions/mdocfile.svg?color=green)](https://python.org)
[![CI](https://github.com/alisterburt/mdocfile/actions/workflows/ci.yml/badge.svg)](https://github.com/alisterburt/mdocfile/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/alisterburt/mdocfile/branch/main/graph/badge.svg)](https://codecov.io/gh/alisterburt/mdocfile)

<p align="center" width="100%">
    <img width="70%" src="https://user-images.githubusercontent.com/7307488/205445941-8db4ad0e-648a-446e-812d-bd1b81ec19b8.png"> 
</p>

*mdocfile* is Python package for working with [SerialEM](https://bio3d.colorado.edu/SerialEM/) mdoc files.

---

# Quickstart

`mdocfile.read()` will return the contents of an mdoc file as a pandas 
dataframe.

```python
import mdocfile

df = mdocfile.read('my_mdoc_file.mdoc')
```

# Installation

pip:

```shell
pip install mdocfile
```
