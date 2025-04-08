#!/usr/bin/env python3

from flask import Flask, request, render_template, send_file, jsonify
import os
import zipfile
import tempfile
import shutil
import re
import uuid
from werkzeug.utils import secure_filename
import sys
from pathlib import Path

# Import the processing functions from the CLI module
from code_cleaner.cli import process_file, detect_language, should_process_file

# Create Flask app
app = Flask(__name__)

# Default configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Try to import Ollama if available
try:
    from langchain.llms import Ollama
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    ollama_llm = Ollama(model="llama3.2")
except Exception as e:
    print(f"Warning: Could not initialize Ollama: {e}")
    ollama_llm = None


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
    
    # Create a unique ID for this processing job
    job_id = str(uuid.uuid4())
    
    # Create directories for this job
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], job_id)
    processed_dir = os.path.join(app.config['PROCESSED_FOLDER'], job_id)
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    # Save the uploaded ZIP file
    zip_path = os.path.join(upload_dir, secure_filename(file.filename))
    file.save(zip_path)
    
    # Extract the ZIP file
    extract_dir = os.path.join(upload_dir, 'extracted')
    os.makedirs(extract_dir, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Process the files
    process_files(extract_dir, processed_dir)
    
    # Create a ZIP file with the processed files
    processed_zip_path = os.path.join(processed_dir, 'processed.zip')
    create_zip(processed_dir, processed_zip_path)
    
    return jsonify({
        'success': True,
        'job_id': job_id,
        'download_url': f'/download/{job_id}'
    })


@app.route('/download/<job_id>')
def download(job_id):
    processed_zip_path = os.path.join(app.config['PROCESSED_FOLDER'], job_id, 'processed.zip')
    if not os.path.exists(processed_zip_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(processed_zip_path, as_attachment=True, download_name='processed_code.zip')


def process_files(input_dir, output_dir):
    """Process all files in the input directory and save to the output directory."""
    exclude_patterns = ['node_modules', '.git', '__pycache__', '.DS_Store']
    
    for root, dirs, files in os.walk(input_dir):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if not any(pattern in os.path.join(root, d) for pattern in exclude_patterns)]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Determine the relative path for the output file
            relative_path = os.path.relpath(file_path, input_dir)
            output_file = os.path.join(output_dir, relative_path)
            
            # Create the necessary directories in the output folder
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Process the file if it should be processed, otherwise just copy it
            if should_process_file(file_path, exclude_patterns, output_dir):
                process_file(file_path, output_file)
            else:
                shutil.copy2(file_path, output_file)


def create_zip(directory, zip_path):
    """Create a ZIP file from a directory."""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path != zip_path:  # Don't include the zip file itself
                    zipf.write(file_path, os.path.relpath(file_path, directory))


def main():
    """Main entry point for the web application."""
    # Create necessary directories if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    
    # Get the package directory to locate templates
    package_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(package_dir, 'templates')
    
    # If templates directory exists in the package, use it
    if os.path.exists(template_dir):
        app.template_folder = template_dir
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()