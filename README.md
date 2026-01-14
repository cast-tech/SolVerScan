# SolVerScan

SolVerScan is a tool for automatically detecting the required Solidity compiler version from Solidity source code.
It can be used both as a library in Python projects and as a command-line tool.
The tool outputs the oldest and the newest versions of the compiler that can be used to compile the files.

## Installation

Install SolVerScan in editable mode for development:

```bash
git clone https://github.com/cast-tech/solverscan.git
pip install ./solverscan
```

## Usage

### Command-line usage

Scan a single file:

```bash
solverscan path/to/MyContract.sol
```

Scan an entire directory:

```bash
solverscan path/to/contracts/
```

### Library usage

```python
from solverscan import detect_version

version = detect_version(["path/to/MyContract.sol"])
print(version)  # e.g., ((0, 8, 13), (0, 8, 14))
```

## Requirements

* Python 3.8 or higher
* Linux, macOS, Windows

## License

MIT License. See LICENSE for details.

## Repository

GitHub: [https://github.com/cast-tech/solverscan](https://github.com/cast-tech/solverscan)

