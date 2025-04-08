from flask import Flask, request, render_template, send_file, jsonify
import os
import zipfile
import tempfile
import shutil
import re
import uuid
from werkzeug.utils import secure_filename
from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Create necessary directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Initialize Ollama LLM
try:
    ollama_llm = Ollama(model="llama3.2")
except Exception as e:
    print(f"Warning: Could not initialize Ollama: {e}")
    ollama_llm = None

# Language detection patterns
def detect_language(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cs': 'csharp',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.ts': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.sh': 'shell',
        '.pl': 'perl',
        '.kt': 'kotlin',
        '.rs': 'rust',
    }
    
    return language_map.get(file_extension, 'unknown')

# Comment patterns for different languages
comment_patterns = {
    'python': [
        r'#.*?$',                     # Single line comments
        r'"""[\s\S]*?"""',           # Triple double quotes
        r"'''[\s\S]*?'''",           # Triple single quotes
    ],
    'javascript': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'java': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'c': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'cpp': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'csharp': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'go': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'ruby': [
        r'#.*?$',                     # Single line comments
        r'=begin[\s\S]*?=end',        # Multi-line comments
    ],
    'php': [
        r'//.*?$',                    # Single line comments
        r'#.*?$',                     # Single line comments (alternative)
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'swift': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'typescript': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'html': [
        r'<!--[\s\S]*?-->',           # HTML comments
    ],
    'css': [
        r'/\*[\s\S]*?\*/',           # CSS comments
    ],
    'shell': [
        r'#.*?$',                     # Single line comments
    ],
    'perl': [
        r'#.*?$',                     # Single line comments
        r'=pod[\s\S]*?=cut',          # POD documentation
    ],
    'kotlin': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'rust': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
    ],
    'unknown': [
        r'//.*?$',                    # Single line comments
        r'/\*[\s\S]*?\*/',           # Multi-line comments
        r'#.*?$',                     # Single line comments (alternative)
        r'"""[\s\S]*?"""',           # Triple double quotes
        r"'''[\s\S]*?'''",           # Triple single quotes
    ],
}

# Console/log statement patterns for different languages
log_patterns = {
    'python': [
        r'print\s*\(.*?\)',
        r'logging\.\w+\s*\(.*?\)',
    ],
    'javascript': [
        r'console\.\w+\s*\(.*?\)',
        r'alert\s*\(.*?\)',
    ],
    'java': [
        r'System\.out\.\w+\s*\(.*?\)',
        r'System\.err\.\w+\s*\(.*?\)',
        r'logger\.\w+\s*\(.*?\)',
    ],
    'c': [
        r'printf\s*\(.*?\)',
        r'fprintf\s*\(.*?\)',
    ],
    'cpp': [
        r'std::cout.*?<<',
        r'std::cerr.*?<<',
    ],
    'csharp': [
        r'Console\.\w+\s*\(.*?\)',
        r'Debug\.\w+\s*\(.*?\)',
    ],
    'go': [
        r'fmt\.\w+\s*\(.*?\)',
        r'log\.\w+\s*\(.*?\)',
    ],
    'ruby': [
        r'puts\s+.*?$',
        r'print\s+.*?$',
        r'p\s+.*?$',
    ],
    'php': [
        r'echo\s+.*?;',
        r'print\s+.*?;',
        r'var_dump\s*\(.*?\)',
    ],
    'swift': [
        r'print\s*\(.*?\)',
        r'NSLog\s*\(.*?\)',
    ],
    'typescript': [
        r'console\.\w+\s*\(.*?\)',
    ],
    'shell': [
        r'echo\s+.*?$',
    ],
    'perl': [
        r'print\s+.*?;',
    ],
    'kotlin': [
        r'println\s*\(.*?\)',
    ],
    'rust': [
        r'println!\s*\(.*?\)',
        r'print!\s*\(.*?\)',
    ],
    'unknown': [
        r'console\.\w+\s*\(.*?\)',
        r'print\s*\(.*?\)',
        r'System\.out\.\w+\s*\(.*?\)',
        r'echo\s+.*?$',
    ],
}

# Function to remove comments and log statements from code
def process_file(file_path, language):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        # Remove comments
        for pattern in comment_patterns.get(language, comment_patterns['unknown']):
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # Remove log statements
        for pattern in log_patterns.get(language, log_patterns['unknown']):
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # Use LLM to identify and remove dead code if available
        if ollama_llm and language != 'unknown':
            try:
                content = remove_dead_code_with_llm(content, language)
            except Exception as e:
                print(f"Error using LLM for dead code removal: {e}")
        
        # Write processed content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            
        return True
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False

# Function to use LLM for dead code removal
def remove_dead_code_with_llm(code, language):
    if not ollama_llm:
        return code
        
    prompt = PromptTemplate(
        input_variables=["code", "language"],
        template="""You are an expert code analyzer. Analyze the following {language} code and remove any dead code (code that is never executed or has no effect). 
        Do not remove functional code. Return only the cleaned code without any explanations.
        
        CODE:
        {code}
        
        CLEANED CODE:"""
    )
    
    chain = LLMChain(llm=ollama_llm, prompt=prompt)
    result = chain.run(code=code, language=language)
    
    # If the result is empty or significantly shorter than the original, return the original
    if not result or len(result) < len(code) * 0.5:
        return code
        
    return result

# Process a zip file
def process_zip_file(zip_path):
    # Create a unique ID for this processing job
    job_id = str(uuid.uuid4())
    extract_dir = os.path.join(tempfile.gettempdir(), job_id)
    
    # Ensure the processed folder exists
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    processed_zip = os.path.join(app.config['PROCESSED_FOLDER'], f"{job_id}_processed.zip")
    
    try:
        # Create extraction directory
        os.makedirs(extract_dir, exist_ok=True)
        
        # Extract zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Process each file
        processed_files = 0
        skipped_files = 0
        
        for root, _, files in os.walk(extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                language = detect_language(file_path)
                
                if language != 'unknown':
                    success = process_file(file_path, language)
                    if success:
                        processed_files += 1
                    else:
                        skipped_files += 1
                else:
                    skipped_files += 1
        
        # Create a new zip file with processed files
        with zipfile.ZipFile(processed_zip, 'w') as zipf:
            for root, _, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, extract_dir)
                    zipf.write(file_path, arcname)
        
        return {
            'success': True,
            'processed_zip': processed_zip,
            'processed_files': processed_files,
            'skipped_files': skipped_files,
            'job_id': job_id
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
    finally:
        # Clean up extraction directory
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.zip'):
        return jsonify({'error': 'Only ZIP files are supported'}), 400
    
    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the zip file
        result = process_zip_file(file_path)
        
        if result['success']:
            return jsonify({
                'success': True,
                'job_id': result['job_id'],
                'processed_files': result['processed_files'],
                'skipped_files': result['skipped_files']
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<job_id>')
def download_file(job_id):
    processed_zip = os.path.join(app.config['PROCESSED_FOLDER'], f"{job_id}_processed.zip")
    
    # Debug information
    print(f"Download requested for job_id: {job_id}")
    print(f"Looking for file at path: {processed_zip}")
    
    if not os.path.exists(processed_zip):
        print(f"Error: File not found at {processed_zip}")
        # Check if the processed folder exists and is writable
        if not os.path.exists(app.config['PROCESSED_FOLDER']):
            os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
            print(f"Created missing processed folder: {app.config['PROCESSED_FOLDER']}")
        
        return jsonify({'error': 'Processed file not found'}), 404
    
    try:
        return send_file(processed_zip, as_attachment=True, download_name="processed_code.zip")
    except Exception as e:
        print(f"Error sending file: {e}")
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500

if __name__ == '__main__':
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Cleaner Application')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    
    app.run(debug=True, host='0.0.0.0', port=args.port)