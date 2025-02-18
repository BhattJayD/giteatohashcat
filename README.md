# Gitea To Hash Extractor

## Description

This tool extracts PBKDF2 password hashes from a Gitea SQLite database and formats them for use with Hashcat.

## Features

- Extracts usernames and PBKDF2 password hashes.
- Supports error handling for missing files and unknown hash algorithms.
- Provides color-coded output for better readability.

## Installation

To set up the environment and install dependencies, follow these steps:

```sh
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

To extract hashes from a Gitea SQLite database, run:

```sh
python gitea_hash_extractor.py <path_to_gitea.db>
```

### Example:

```sh
python gitea_hash_extractor.py gitea.db
```

## Dependencies

- Python 3
- `sqlite3` (included in Python standard library)
- `base64` (included in Python standard library)
- `argparse` (included in Python standard library)
- `os` (included in Python standard library)
- `termcolor`

To install missing dependencies:

```sh
pip install termcolor
```

## Author

Jay Bhatt (SplitUnknown).
