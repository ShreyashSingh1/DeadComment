# Code Cleaner

A tool that removes comments, console/log statements, and optionally dead code from source files while preserving functionality. Available as both CLI and web application.

## Features

- Detects programming language based on file extensions
- Removes single-line and multi-line comments
- Removes console/log statements
- Optional dead code removal with Ollama LLM
- Preserves code functionality
- Processes entire projects with directory structure
- Supports multiple programming languages

## Requirements

- Python 3.6+
- Ollama with llama3.2 model (optional, for dead code removal)

## Installation

### As a package (recommended)

```bash
# From source code
pip install .

# Or once published to PyPI
# pip install code-cleaner
```

### Without installing

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. (Optional) For dead code removal: Install [Ollama](https://ollama.ai/) and pull the model: `ollama pull llama3.2`

## Usage

### Command Line

```bash
# Basic usage
code-cleaner

# With options
code-cleaner --output cleaned_code --no-subdirs --exclude node_modules,vendor,.git

# Help
code-cleaner --help
```

### Web Interface

```bash
# After package installation
code-cleaner-web

# Or without installing
python app.py
```

Then visit `http://localhost:5000`, upload your code ZIP file, and download the cleaned result.

## How It Works

- Detects language by file extension
- Uses regex patterns to remove comments and logs
- Optionally uses Ollama LLM to identify and remove dead code
- Preserves directory structure
- Skips binary and non-text files

## Supported Languages

Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Ruby, PHP, Swift, HTML, CSS, Shell scripts, Perl, Kotlin, Rust

## Contributing

Contributions welcome! Add language support, improve regex patterns, enhance the UI, or report bugs.

## License

MIT