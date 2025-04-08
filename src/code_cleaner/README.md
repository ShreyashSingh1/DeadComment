# Code Cleaner

A Python package to remove comments and log statements from code files.

## Installation

```bash
# Install from PyPI (once published)
pip install code-cleaner

# Or install from the source code
pip install .
```

## Usage

### Command Line Interface

After installation, you can use the `code-cleaner` command to clean your code:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Clean the code in the current directory
code-cleaner

# Specify an output directory
code-cleaner --output cleaned_code

# Don't process subdirectories
code-cleaner --no-subdirs

# Exclude specific patterns
code-cleaner --exclude node_modules,vendor,.git

# Show help
code-cleaner --help
```

### Web Interface

You can also use the web interface to clean your code:

```bash
# Start the web server
code-cleaner-web
```

Then open your browser and navigate to `http://localhost:5000`.

## Features

- Removes comments from various programming languages
- Eliminates console.log and print statements
- Preserves code functionality
- Supports multiple programming languages
- Processes entire projects with directory structure
- Provides both CLI and web interface

## Supported Languages

- Python
- JavaScript
- Java
- C
- C++
- C#
- Go
- Ruby
- PHP
- Swift
- TypeScript
- HTML
- CSS
- Shell
- Perl
- Kotlin
- Rust

## License

MIT