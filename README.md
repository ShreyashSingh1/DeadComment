# Code Cleaner

A web application that processes source code files to automatically remove comments, console/log statements, and dead code, regardless of the programming language used.

## Features

- Upload ZIP files containing source code
- Automatically detects programming language based on file extensions
- Removes comments (single-line and multi-line)
- Removes console/log statements
- Removes dead code (using Ollama LLM)
- Supports multiple programming languages including Python, JavaScript, Java, C/C++, Go, Ruby, PHP, and more
- Downloads processed code as a ZIP file

## Requirements

- Python 3.7+
- Flask
- LangChain
- Ollama (optional, for enhanced dead code removal)

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. (Optional) Install Ollama for enhanced dead code removal:
   - Follow the instructions at [Ollama's website](https://ollama.ai/)
   - Pull the llama2 model: `ollama pull llama2`

## Usage

1. Start the application:

```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`
3. Upload a ZIP file containing your source code
4. Wait for the processing to complete
5. Download the processed ZIP file

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