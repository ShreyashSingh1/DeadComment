# Code Cleaner

A tool that processes source code files to automatically remove comments and console/log statements, regardless of the programming language used. Available as both a command-line tool and a web application.

## Features

- Automatically detects programming language based on file extensions
- Removes comments (single-line and multi-line)
- Removes console/log statements
- Supports multiple programming languages including Python, JavaScript, Java, C/C++, Go, Ruby, PHP, and more
- Available as both a CLI tool and web application

## Requirements

- Python 3.6+

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
3. Wait for the processing to complete
4. Download the processed ZIP file

## How It Works

1. The application extracts the uploaded ZIP file
2. It detects the programming language of each file based on its extension
3. For each supported file, it removes:
   - Comments using regular expressions tailored to each language
   - Console/log statements using language-specific patterns
   - Dead code using LLM analysis (if Ollama is available)
4. The processed files are packaged into a new ZIP file for download

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

## License

MIT