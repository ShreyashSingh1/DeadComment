# Code Cleaner

A powerful tool that processes source code files to automatically remove comments, console/log statements, and optionally dead code, regardless of the programming language used. Available as both a command-line tool and a web application.

## Features

- Automatically detects programming language based on file extensions
- Removes comments (single-line and multi-line)
- Removes console/log statements
- Optional dead code removal using Ollama LLM integration
- Preserves code functionality and structure
- Processes entire projects while maintaining directory structure
- Supports multiple programming languages including Python, JavaScript, Java, C/C++, Go, Ruby, PHP, and more
- Available as both a CLI tool and web application

## Requirements

- Python 3.6+
- For enhanced dead code removal: Ollama with llama3.2 model (optional)

## Installation

### Option 1: Install as a package (recommended)

```bash
# Install from the source code
pip install .

# Or once published to PyPI
# pip install code-cleaner
```

### Option 2: Run without installing

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. (Optional) Install Ollama for enhanced dead code removal in the web interface:
   - Follow the instructions at [Ollama's website](https://ollama.ai/)
   - Pull the llama3.2 model: `ollama pull llama3.2`

## Usage

### Command Line Interface

After installation as a package, you can use the `code-cleaner` command to clean your code:

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

The CLI tool will:
1. Scan your project directory
2. Identify files with supported extensions
3. Process each file to remove comments and log statements
4. Save the cleaned files to the specified output directory

### Web Interface

After installation as a package:

```bash
# Start the web server
code-cleaner-web
```

Or if running without installing:

```bash
python app.py
```

Then:
1. Open your browser and navigate to `http://localhost:5000`
2. Upload a ZIP file containing your source code
3. Configure processing options (if available)
4. Click "Process" to start cleaning your code
5. Wait for the processing to complete
6. Download the processed ZIP file with cleaned code

## How It Works

### Comment and Log Statement Removal

1. The application detects the programming language of each file based on its extension
2. It applies language-specific regular expressions to identify and remove:
   - Single-line comments (e.g., `// comment` in JavaScript, `# comment` in Python)
   - Multi-line comments (e.g., `/* comment */` in C-style languages, `""" comment """` in Python)
   - Console/log statements (e.g., `console.log()` in JavaScript, `print()` in Python)

### Dead Code Detection (Web Interface with Ollama)

When Ollama integration is available:
1. The web interface uses the llama3.2 model to analyze code
2. It identifies potentially unused functions, variables, and code blocks
3. The LLM provides suggestions for code that can be safely removed

### File Processing

1. For CLI: Files are processed in-place or copied to a specified output directory
2. For Web: The uploaded ZIP file is extracted, processed, and repackaged
3. Directory structure is preserved in both cases
4. Binary and non-text files are automatically skipped

## Supported Languages

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C (.c)
- C++ (.cpp)
- C# (.cs)
- Go (.go)
- Ruby (.rb)
- PHP (.php)
- Swift (.swift)
- HTML (.html)
- CSS (.css)
- Shell scripts (.sh)
- Perl (.pl)
- Kotlin (.kt)
- Rust (.rs)

## Contributing

Contributions are welcome! Here are some ways you can contribute:

- Add support for additional programming languages
- Improve the regular expressions for existing languages
- Enhance the web interface
- Add new features or improve existing ones
- Report bugs or suggest improvements

## License

MIT