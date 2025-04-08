 #!/usr/bin/env python3

import os
import re
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

# Comment patterns for different languages
COMMENT_PATTERNS = {
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
LOG_PATTERNS = {
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


def detect_language(file_path: str) -> str:
    """Detect the programming language based on file extension."""
    extension = os.path.splitext(file_path)[1].lower()
    
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
    
    return language_map.get(extension, 'unknown')


def process_file(input_file: str, output_file: str) -> bool:
    """Process a file to remove comments and log statements."""
    try:
        language = detect_language(input_file)
        
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        # Remove comments
        for pattern in COMMENT_PATTERNS.get(language, COMMENT_PATTERNS['unknown']):
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # Remove log statements
        for pattern in LOG_PATTERNS.get(language, LOG_PATTERNS['unknown']):
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return True
    except Exception as e:
        print(f"Error processing file {input_file}: {e}", file=sys.stderr)
        return False


def should_process_file(file_path: str, exclude_patterns: List[str], output_dir: str) -> bool:
    """Check if a file should be processed."""
    filename = os.path.basename(file_path)
    
    # Skip hidden files and directories
    if filename.startswith('.'):
        return False
    
    # Skip the script itself and the output directory
    if os.path.abspath(file_path) == os.path.abspath(__file__) or file_path.startswith(output_dir):
        return False
    
    # Skip excluded patterns
    for pattern in exclude_patterns:
        if pattern in file_path:
            return False
    
    # Skip binary files and other non-text files
    try:
        # Use the 'file' command on Unix-like systems if available
        if sys.platform != 'win32' and subprocess.run(['file', '--mime', file_path], 
                                                    stdout=subprocess.PIPE, 
                                                    stderr=subprocess.PIPE).stdout.decode().find('text/') == -1:
            return False
    except (subprocess.SubprocessError, FileNotFoundError):
        # Fallback method: try to open and read the file
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.read(1024)  # Read a small chunk to check if it's text
        except UnicodeDecodeError:
            return False
    
    # Only process files with recognized extensions
    language = detect_language(file_path)
    if language == 'unknown':
        return False
    
    return True


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='Code Cleaner CLI Tool')
    parser.add_argument('-o', '--output', default='copy', help='Set output directory (default: "copy")')
    parser.add_argument('-n', '--no-subdirs', action='store_true', help="Don't process subdirectories")
    parser.add_argument('-e', '--exclude', default='node_modules,.git,__pycache__,.DS_Store',
                        help='Comma-separated list of patterns to exclude')
    
    args = parser.parse_args()
    
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, args.output)
    exclude_patterns = args.exclude.split(',')
    process_subdirs = not args.no_subdirs
    
    print("Code Cleaner CLI Tool")
    print("=====================")
    print(f"Scanning directory: {current_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Exclude patterns: {args.exclude}")
    print(f"Processing subdirectories: {'Yes' if process_subdirs else 'No'}")
    print()
    
    # Create the output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Count variables
    total_files = 0
    processed_files = 0
    skipped_files = 0
    
    # Walk through the directory
    for root, dirs, files in os.walk(current_dir):
        # Skip the output directory
        if os.path.abspath(root).startswith(os.path.abspath(output_dir)):
            continue
        
        # Skip excluded directories
        dirs[:] = [d for d in dirs if not any(pattern in os.path.join(root, d) for pattern in exclude_patterns)]
        
        # If not processing subdirectories and not in the current directory, skip
        if not process_subdirs and root != current_dir:
            continue
        
        for file in files:
            file_path = os.path.join(root, file)
            total_files += 1
            
            if should_process_file(file_path, exclude_patterns, output_dir):
                # Determine the relative path for the output file
                relative_path = os.path.relpath(file_path, current_dir)
                output_file = os.path.join(output_dir, relative_path)
                
                # Process the file
                print(f"Processing: {relative_path}")
                if process_file(file_path, output_file):
                    processed_files += 1
                else:
                    skipped_files += 1
                    print(f"  Skipped due to processing error")
            else:
                skipped_files += 1
    
    print()
    print("Processing complete!")
    print("------------------")
    print(f"Total files scanned: {total_files}")
    print(f"Files processed: {processed_files}")
    print(f"Files skipped: {skipped_files}")
    print()
    print(f"Processed files are saved in: {output_dir}")


if __name__ == "__main__":
    main()